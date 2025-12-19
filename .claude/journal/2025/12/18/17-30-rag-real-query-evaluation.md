---
created: 2025-12-18T17:30:00-08:00
parent_daily: "[[2025-12-18]]"
tags:
  - search
  - rag
  - evaluation
  - methodology
  - lessons-learned
---

# RAG Evaluation: Real Queries vs Templated Queries

A sobering comparison revealing significant overestimation in our initial evaluation.

## The Problem: Templated Queries Are Too Easy

Initial evaluation used template-generated queries like:
- "What is the {agent_name} agent and what does it do?"
- "What does the {plugin_name} plugin do?"

These achieved MRR 1.000 - perfect retrieval. But they're unrealistic because:
1. They mirror the exact phrasing in source documents
2. They contain the exact entity names being searched for
3. They don't require understanding context or intent

## Real User Query Analysis

Extracted 82 ecosystem-related queries from 482 session logs:

| Query Type | Example | Count |
|------------|---------|-------|
| Contextual | "Where is it documented?" | Many |
| Compound | "Are you aware of agentnet? How does that work?" | Many |
| Action-oriented | "Can you change the default agent name from..." | Many |
| Vague | "How do I interact with it?" | Some |
| Session-specific | "What does this imply for our repository?" | Some |

Key observation: Real queries often reference **prior conversation context** that retrieval cannot access.

## Results Comparison

### Templated Queries (n=122)
| Config | MRR | P@5 |
|--------|-----|-----|
| vector | 1.000 | 0.997 |
| hybrid | 0.801 | 0.521 |

### Real User Queries (n=40)
| Config | MRR | P@5 |
|--------|-----|-----|
| vector | 0.182 | 0.135 |
| hybrid | 0.171 | 0.070 |

**Drop: 82% lower MRR on real queries**

## Why Real Queries Fail

### 1. Context-Dependent Queries
```
"Where is it documented?"
"How do I interact with it?"
"What does this imply for our repository?"
```
These require conversational context to resolve "it" and "this".

### 2. Compound Questions
```
"Are you aware of agentnet? How does that work in terms of agent IDs?"
```
Multiple sub-questions; retrieval finds partial matches.

### 3. Action Requests Disguised as Questions
```
"Can you make the oneline summaries in the statusline white and bold?"
```
Not actually information-seeking; asks for action.

### 4. Session-Specific Debugging
```
"Why is agent renaming not working for the statusline right now?"
"Why are autocommit commands not showing up in this instance?"
```
Refers to transient runtime state, not indexed knowledge.

## Implications

### RAG Scope is Narrower Than Expected

Many "questions" in Claude Code sessions are:
- Action requests (not info retrieval)
- Context-dependent follow-ups
- Runtime debugging (not docable)

RAG works well for **standalone knowledge queries** but poorly for conversational continuation.

### Evaluation Must Match Reality

| Evaluation Type | MRR | Validity |
|-----------------|-----|----------|
| Templated | 1.000 | Low - unrealistic |
| Real queries | 0.182 | High - actual usage |

The 5x difference suggests templated evaluation gives false confidence.

### Query Classification Matters

Future work should classify queries before routing:
1. **Knowledge queries** → RAG retrieval
2. **Context queries** → Conversation history
3. **Action queries** → Tool use directly
4. **Debugging queries** → Runtime introspection

## Artifacts Created

- `ecosystem_user_queries.json` - 82 real ecosystem queries
- `human_labeling_sample.json` - 30 queries with results for human verification
- `human_labeling.md` - Markdown format for manual labeling
- `eval_real_queries.py` - Real query evaluation script
- `real_queries_eval.json` - Detailed evaluation results

## Lessons Learned

1. **Template-based evaluation severely overestimates quality**
2. **Real queries are often not answerable by static retrieval**
3. **LLM judge threshold matters** (fixed 0-2 scale bug)
4. **Human labeling sample is essential for validation**

---

*Parent: [[2025-12-18]] → [[2025-12]] → [[2025]]*
