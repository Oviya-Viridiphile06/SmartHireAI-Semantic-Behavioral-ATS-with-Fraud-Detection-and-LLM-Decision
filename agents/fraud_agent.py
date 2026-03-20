import re
from utils.pdf_fraud_detector import detect_hidden_text
from utils.scoring import expand_skills

class FraudAgent:

    def detect(self, resume_text, skills, file_path=None):

        text = resume_text.lower()

        expanded_skills = expand_skills(skills)

        # Flatten all variants (AI + artificial intelligence + ml etc.)
        all_variants = set()
        for variants in expanded_skills.values():
            all_variants.update(variants)

        # -----------------------------
        # RULE 1: TRUE CONSECUTIVE REPETITION
        # -----------------------------
        for variant in all_variants:

            pattern = r"(?:\b" + re.escape(variant) + r"\b[\s,]*){6,}"

            if re.search(pattern, text):
                return True, f"Extreme consecutive repetition detected: {variant}"

        # -----------------------------
        # RULE 2: CONTINUOUS KEYWORD BLOCK
        # -----------------------------
        if all_variants:

            pattern = r"(?:\b(" + "|".join(map(re.escape, all_variants)) + r")\b[\s,]*){8,}"

            if re.search(pattern, text):
                return True, "Suspicious continuous keyword block detected"

        # -----------------------------
        # RULE 3: HIDDEN TEXT (PDF)
        # -----------------------------
        if file_path:
            try:
                filename = getattr(file_path, "name", "")

                if filename.endswith(".pdf"):

                    fraud, reason = detect_hidden_text(file_path)

                    if fraud:
                        return True, reason

            except Exception as e:
                print("PDF fraud detection error:", e)

        return False, ""