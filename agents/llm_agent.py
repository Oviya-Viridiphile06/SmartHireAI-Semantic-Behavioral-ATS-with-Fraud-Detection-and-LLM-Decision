from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class LLMAgent:

    def get_final_decision(self, resume, jd):
        try:
            prompt = f"""
            You are an expert recruiter.

            Decide if the candidate should be SELECTED or REJECTED.

            Rules:
            - If most key skills match → SELECT
            - If major skills missing → REJECT

            Answer ONLY one word:
            SELECT or REJECT

            Resume:
            {resume}

            Job Description:
            {jd}
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("LLM decision error:", e)
            return None