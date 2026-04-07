"""Financial situation memory using BM25 for lexical similarity matching.

Uses BM25 (Best Matching 25) algorithm for retrieval - no API calls,
no token limits, works offline with any LLM provider.
"""

from rank_bm25 import BM25Okapi
from typing import List, Tuple
import re


class FinancialSituationMemory:
    """Memory system for storing and retrieving financial situations using BM25."""

    def __init__(self, name: str, config: dict = None):
        self.name = name
        self.documents: List[str] = []
        self.recommendations: List[str] = []
        self.bm25 = None

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def _rebuild_index(self):
        if self.documents:
            tokenized = [self._tokenize(doc) for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized)
        else:
            self.bm25 = None

    def add_situations(self, situations_and_advice: List[Tuple[str, str]]):
        for situation, recommendation in situations_and_advice:
            self.documents.append(situation)
            self.recommendations.append(recommendation)
        self._rebuild_index()

    def get_memories(self, current_situation: str, n_matches: int = 1) -> List[dict]:
        if not self.documents or self.bm25 is None:
            return []

        query_tokens = self._tokenize(current_situation)
        scores = self.bm25.get_scores(query_tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_matches]

        max_score = max(scores) if max(scores) > 0 else 1
        return [
            {
                "matched_situation": self.documents[idx],
                "recommendation": self.recommendations[idx],
                "similarity_score": scores[idx] / max_score if max_score > 0 else 0,
            }
            for idx in top_indices
        ]

    def clear(self):
        self.documents = []
        self.recommendations = []
        self.bm25 = None
