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
        self.categories = {
            "Таргет (Target Ads)": [k.lower() for k in config.keywords_target],
            "AEO (AI Search)": [k.lower() for k in config.keywords_aeo],
            "GEO (Generative Engine)": [k.lower() for k in config.keywords_geo],
            "SEO (Search Engine)": [k.lower() for k in config.keywords_seo],
            "Создание Сайтов (Web Dev)": [k.lower() for k in config.keywords_sites],
        }

    def match(self, text: str) -> MatchResult:
        if not text:
            return MatchResult(is_match=False)

        text_lower = text.lower()

        for category_name, keywords in self.categories.items():
            for kw in keywords:
                # Add word boundary check or just substring. Since the keywords can be multiple words, substring is fine.
                # However, to avoid 'seo' matching 'caseomatic', we could pad with spaces or use regex.
                # For simplicity, standard substring matching as originally implemented.
                if kw in text_lower:
                    return MatchResult(is_match=True, category=category_name, matched_keyword=kw)

        return MatchResult(is_match=False)
