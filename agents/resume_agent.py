import re

class ResumeAgent:

    def process(self, resume_text):

        # Remove extra spaces but keep line breaks
        text = re.sub(r'[ \t]+', ' ', resume_text)

        return text


    def extract_email(self, text):

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

        match = re.search(pattern, text)

        if match:
            return match.group(0)

        return None


    def extract_name(self, text, email=None):

        lines = [l.strip() for l in text.split("\n") if l.strip()]

        blacklist = [
            "resume","curriculum","vitae","email","phone","contact",
            "linkedin","github","profile","summary","objective"
        ]

        # ---------- Rule 1: line above email ----------
        if email:
            for i, line in enumerate(lines):

                if email in line and i > 0:

                    candidate = lines[i-1]

                    words = candidate.split()

                    if 2 <= len(words) <= 4:
                        if all(w.replace(".","").isalpha() for w in words):
                            return " ".join(words)

        # ---------- Rule 2: check first 6 lines ----------
        for line in lines[:6]:

            lower_line = line.lower()

            if any(b in lower_line for b in blacklist):
                continue

            words = line.split()

            if 2 <= len(words) <= 4:
                if all(w.replace(".","").isalpha() for w in words):
                    return " ".join(words)

        # ---------- Rule 3: uppercase name ----------
        for line in lines[:6]:

            words = line.split()

            if 2 <= len(words) <= 4:
                if all(w[0].isupper() for w in words if w.replace(".","").isalpha()):
                    return " ".join(words)

        return "Candidate"
