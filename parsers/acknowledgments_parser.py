import re
from typing import Dict, List


class AcknowledgmentsParser:
    def extract_funding(self, ack_text: str) -> Dict[str, List[str]]:
        orgs = self.get_organizations(ack_text)
        grants = self.get_grants(ack_text)
        return {
            "organizations": orgs,
            "grants": grants,
        }

    @staticmethod
    def get_organizations(text: str) -> List[str]:
        funding_patterns = [
            r"(?:supported|funded|granted|sponsored)\s+by\s+(.*?)(?:\s+under|\s+through|\s+grant|\s+program|[\.\,])",
        ]

        matches = []
        for pattern in funding_patterns:
            for match in re.findall(pattern, text, flags=re.IGNORECASE):
                # Basic cleanup and filtering
                cleaned = match.strip()
                if 5 <= len(cleaned) <= 150:
                    matches.append(cleaned)

        return list(set(matches))  # Remove duplicates

    @staticmethod
    def get_grants(text: str) -> List[str]:
        grant_patterns = [
            r"\b(?:Grant|Program)?\s*No\.?\s*[\d\w\-]+",
            r"\b(?:Grant|Program)?\s*(?:number\s*)?#?\s*[\d]{4,}",
            r"\b[A-Z]{2,}-[A-Z]+\s*\(?[\d\-]+\)?",  # e.g., EFRI-PSBR (1332349)
            r"\bGrant\s+\d{4,}",
        ]

        matches = []
        for pattern in grant_patterns:
            matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))

        return list(set(matches))
