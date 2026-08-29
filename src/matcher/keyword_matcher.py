from typing import Optional, Tuple
from dataclasses import dataclass
from src.config import config

@dataclass
class MatchResult:
    is_match: bool
    category: Optional[str] = None
    matched_keyword: Optional[str] = None

class KeywordMatcher:
    def __init__(self):
        self.aeo_keywords = [k.lower() for k in config.keywords_aeo_geo]
        self.target_keywords = [k.lower() for k in config.keywords_target]

    def match(self, text: str) -> MatchResult:
        if not text:
            return MatchResult(is_match=False)

        text_lower = text.lower()

        # Check AEO / GEO
        for kw in self.aeo_keywords:
            if kw in text_lower:
                return MatchResult(is_match=True, category="AEO/GEO & AI SEO", matched_keyword=kw)

        # Check Target
        for kw in self.target_keywords:
            if kw in text_lower:
                return MatchResult(is_match=True, category="Target Ads (US/RU)", matched_keyword=kw)

        return MatchResult(is_match=False)
