"""RAG infrastructure for repository search with test harness."""
from .protocols import Chunker, Embedder, Retriever, Reranker, Document, Chunk, SearchResult
from .chunker import RecursiveTextSplitter
from .contextual_chunker import ContextualChunker
from .embedder import OllamaEmbedder
from .ollama_generator import OllamaGenerator
from .retriever import VectorRetriever, HybridRetriever, RerankingRetriever
from .reranker import CrossEncoderReranker
from .index import FileIndex
from .judge import RelevanceJudge, RelevanceJudgment, GroundTruthBuilder
from .metrics import MetricsCalculator, EvaluationMetrics, AggregateMetrics, format_metrics, format_comparison
from .evaluation import Evaluator, EvaluationResult, save_evaluation, load_ground_truth

__all__ = [
    # Protocols
    'Chunker', 'Embedder', 'Retriever', 'Reranker',
    # Data structures
    'Document', 'Chunk', 'SearchResult',
    # Chunking
    'RecursiveTextSplitter', 'ContextualChunker',
    # Embedding & Generation
    'OllamaEmbedder', 'OllamaGenerator',
    # Retrieval
    'VectorRetriever', 'HybridRetriever', 'RerankingRetriever',
    'CrossEncoderReranker',
    # Storage
    'FileIndex',
    # Evaluation
    'RelevanceJudge', 'RelevanceJudgment', 'GroundTruthBuilder',
    'MetricsCalculator', 'EvaluationMetrics', 'AggregateMetrics',
    'format_metrics', 'format_comparison',
    'Evaluator', 'EvaluationResult', 'save_evaluation', 'load_ground_truth'
]
