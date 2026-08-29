import re
from typing import Optional
from dataclasses import dataclass
from src.keywords import KEYWORDS

@dataclass
class MatchResult:
    is_match: bool
    category: Optional[str] = None
    matched_keyword: Optional[str] = None

class KeywordMatcher:
    def __init__(self):
        # Build regex patterns for exact word boundaries to avoid matching "geo" in "Pigeon"
        self.categories = {}
        for cat, words in KEYWORDS.items():
            patterns = []
            for kw in words:
                kw = kw.lower()
                # (?<![\w\-]) means no letter/number/dash before
                # (?![\w\-]) means no letter/number/dash after
                patterns.append((kw, re.compile(rf"(?<![\w\-]){re.escape(kw)}(?![\w\-])", re.IGNORECASE)))
            self.categories[cat] = patterns

    def match(self, text: str) -> MatchResult:
        if not text:
            return MatchResult(is_match=False)

        for category_name, patterns in self.categories.items():
            for kw, pattern in patterns:
                if pattern.search(text):
                    return MatchResult(is_match=True, category=category_name, matched_keyword=kw)

        return MatchResult(is_match=False)
