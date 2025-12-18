"""Vector similarity retriever."""
import numpy as np
from numpy.typing import NDArray
from .protocols import Document, SearchResult, Retriever, Embedder


class VectorRetriever:
    """
    Vector similarity retrieval using cosine similarity.

    Simple and fast for moderate-sized indices (<100k documents).
    Uses normalized embeddings so dot product = cosine similarity.
    """

    name = "vector"

    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.documents: list[Document] = []
        self.embeddings: NDArray[np.float32] | None = None
        self._indexed = False

    def index(self, documents: list[Document]) -> None:
        """Build vector index from documents."""
        if not documents:
            raise ValueError("Cannot index empty document list")

        self.documents = documents

        # Generate embeddings
        texts = [doc.content for doc in documents]
        self.embeddings = self.embedder.embed_batch(texts)

        self._indexed = True

    def search(self, query: str, k: int = 10) -> list[SearchResult]:
        """Search for most similar documents."""
        if not self._indexed:
            raise RuntimeError("Index not built. Call index() first.")

        # Handle empty index
        if len(self.documents) == 0:
            return []

        # Embed query
        query_embedding = self.embedder.embed(query)

        # Compute similarities (dot product of normalized vectors = cosine)
        similarities = self.embeddings @ query_embedding

        # Get top-k indices
        k = min(k, len(self.documents))
        top_indices = np.argsort(similarities)[::-1][:k]

        # Build results
        results = []
        for idx in top_indices:
            results.append(SearchResult(
                document=self.documents[idx],
                score=float(similarities[idx]),
                metadata={'method': 'vector'}
            ))

        return results

    def set_index(self, documents: list[Document], embeddings: NDArray[np.float32]) -> None:
        """Set pre-computed index (for loading from disk)."""
        self.documents = documents
        self.embeddings = embeddings
        self._indexed = True


class HybridRetriever:
    """
    Hybrid retriever combining vector similarity with BM25.

    Uses Reciprocal Rank Fusion (RRF) to combine rankings:
    score(d) = sum(1 / (k + rank(d))) for each method

    This balances keyword exactness (BM25) with semantic similarity (vector).
    """

    name = "hybrid"

    def __init__(self, embedder: Embedder, rrf_k: int = 60, alpha: float = 0.5):
        self.embedder = embedder
        self.rrf_k = rrf_k  # RRF constant (higher = more weight to lower ranks)
        self.alpha = alpha   # Weight: alpha*BM25 + (1-alpha)*vector

        self.documents: list[Document] = []
        self.embeddings: NDArray[np.float32] | None = None
        self.tokenized_corpus: list[list[str]] | None = None
        self._indexed = False

    def index(self, documents: list[Document]) -> None:
        """Build both vector and BM25 indices."""
        if not documents:
            raise ValueError("Cannot index empty document list")

        self.documents = documents

        # Vector embeddings
        texts = [doc.content for doc in documents]
        self.embeddings = self.embedder.embed_batch(texts)

        # Tokenize for BM25
        self.tokenized_corpus = [self._tokenize(doc.content) for doc in documents]

        self._indexed = True

    def search(self, query: str, k: int = 10) -> list[SearchResult]:
        """Hybrid search with RRF fusion."""
        if not self._indexed:
            raise RuntimeError("Index not built. Call index() first.")

        # Handle empty index
        if len(self.documents) == 0:
            return []

        # Vector search
        query_emb = self.embedder.embed(query)
        vector_scores = self.embeddings @ query_emb
        vector_ranking = np.argsort(vector_scores)[::-1]

        # BM25 search
        query_tokens = self._tokenize(query)
        bm25_scores = self._bm25_score(query_tokens)
        bm25_ranking = np.argsort(bm25_scores)[::-1]

        # RRF fusion
        fused_scores = {}

        for rank, idx in enumerate(bm25_ranking[:k*2]):
            fused_scores[idx] = fused_scores.get(idx, 0) + \
                self.alpha / (self.rrf_k + rank + 1)

        for rank, idx in enumerate(vector_ranking[:k*2]):
            fused_scores[idx] = fused_scores.get(idx, 0) + \
                (1 - self.alpha) / (self.rrf_k + rank + 1)

        # Sort by fused score
        ranked = sorted(fused_scores.items(), key=lambda x: -x[1])[:k]

        # Build results
        results = []
        for idx, score in ranked:
            results.append(SearchResult(
                document=self.documents[idx],
                score=float(score),
                metadata={
                    'method': 'hybrid',
                    'vector_score': float(vector_scores[idx]),
                    'bm25_score': float(bm25_scores[idx])
                }
            ))

        return results

    def _tokenize(self, text: str) -> list[str]:
        """Simple tokenization for BM25."""
        import re
        # Split on non-alphanumeric, lowercase
        tokens = re.findall(r'\b[a-z0-9_]+\b', text.lower())

        # Remove common stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
                     'and', 'or', 'if', 'this', 'that', 'it', 'as', 'not'}

        return [t for t in tokens if t not in stopwords and len(t) > 1]

    def _bm25_score(self, query_tokens: list[str]) -> NDArray[np.float32]:
        """Calculate BM25 scores for all documents."""
        import math
        from collections import Counter

        k1, b = 1.5, 0.75
        n = len(self.documents)

        # Document frequencies
        df = Counter()
        for doc_tokens in self.tokenized_corpus:
            for token in set(doc_tokens):
                df[token] += 1

        # Average document length (guard against all-empty tokenizations)
        total_len = sum(len(t) for t in self.tokenized_corpus)
        avg_len = total_len / n if total_len > 0 else 1

        # IDF scores
        idf = {}
        for term, freq in df.items():
            idf[term] = math.log((n - freq + 0.5) / (freq + 0.5) + 1)

        # Score each document
        scores = np.zeros(n, dtype=np.float32)

        for i, doc_tokens in enumerate(self.tokenized_corpus):
            doc_len = len(doc_tokens)
            tf = Counter(doc_tokens)

            score = 0.0
            for term in query_tokens:
                if term in idf:
                    term_freq = tf.get(term, 0)
                    if term_freq > 0:
                        numerator = term_freq * (k1 + 1)
                        denominator = term_freq + k1 * (1 - b + b * doc_len / avg_len)
                        score += idf[term] * numerator / denominator

            scores[i] = score

        return scores

    def set_index(self, documents: list[Document], embeddings: NDArray[np.float32]) -> None:
        """Set pre-computed index (for loading from disk)."""
        self.documents = documents
        self.embeddings = embeddings
        self.tokenized_corpus = [self._tokenize(doc.content) for doc in documents]
        self._indexed = True
