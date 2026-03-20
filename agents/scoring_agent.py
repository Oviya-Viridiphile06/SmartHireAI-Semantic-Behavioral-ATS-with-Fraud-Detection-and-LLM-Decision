from utils.scoring import keyword_match, skill_context_score
from nlp.embedding_model import semantic_similarity
from nlp.vector_store import get_relevant_chunks
import re

class ScoringAgent:

    def calculate_score(self, resume_text, jd, skills):

        # Skill keyword score
        keyword_score = keyword_match(resume_text, skills)

        # Context skill score
        context_score = skill_context_score(resume_text, skills)

        # Semantic JD similarity

        relevant_text = get_relevant_chunks(resume_text, jd)

        semantic_score = semantic_similarity(relevant_text, jd)
        
        # Experience extraction
        experience = self.extract_experience(resume_text)

        # Weighted scoring formula
        final_score = (
            keyword_score * 0.45 +
            context_score * 0.35 +
            semantic_score * 0.20
        )

        return round(final_score, 2), experience

    def extract_experience(self, text):

        match = re.search(r'(\d+)\+?\s*(years|year|yrs|yr)', text.lower())

        if match:
            return int(match.group(1))

        return 0
