# src/engine/normalizer.py
import re

class DataNormalizer:
    def __init__(self, rules_catalog: dict = None):
        self.rules = rules_catalog or {
            "manga_aliases": ["manga art", "manga rare", "sec-parallel"],
            "set_pattern": r"OP\d{2}-\d{3}"
        }

    def normalize_card_code(self, raw_code: str) -> str:
        """Extracts canonical set code like OP05-119 from messy input strings."""
        match = re.search(self.rules["set_pattern"], raw_code.upper())
        if match:
            return match.group(0)
        return raw_code.strip().upper()

    def categorize_rarity(self, raw_rarity: str) -> str:
        """Standardizes rarity tags across sources (TCGPlayer, Cardmarket, etc)."""
        clean_tag = raw_rarity.lower().strip()
        if any(alias in clean_tag for alias in self.rules["manga_aliases"]):
            return "SEC-Parallel (Manga)"
        if "alt" in clean_tag or "parallel" in clean_tag:
            return "Parallel Art"
        return raw_rarity.upper()