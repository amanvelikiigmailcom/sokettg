from typing import Optional, Tuple
from dataclasses import dataclass
from src.keywords import KEYWORDS

@dataclass
class MatchResult:
    is_match: bool
    category: Optional[str] = None
    matched_keyword: Optional[str] = None

class KeywordMatcher:
    def __init__(self):
        # Flatten and lowercase keywords for matching
        self.categories = {
            cat: [kw.lower() for kw in words]
            for cat, words in KEYWORDS.items()
        }

    def match(self, text: str) -> MatchResult:
        if not text:
            return MatchResult(is_match=False)

        text_lower = text.lower()

        for category_name, keywords in self.categories.items():
            for kw in keywords:
                if kw in text_lower:
                    return MatchResult(is_match=True, category=category_name, matched_keyword=kw)

        return MatchResult(is_match=False)
