from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class LLMAgent:

    def get_skill_gap(self, resume, jd):

        models = [
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "mixtral-8x7b-32768"
        ]

        prompt = f"""
        You are an ATS system.

        STRICT RULES:
        - Return ONLY missing skills
        - Output must be comma separated
        - DO NOT explain anything
        - Max 6 skills

        Resume:
        {resume}

        Job Description:
        {jd}
        """

        for model in models:
            try:
                print(f"Trying model: {model}")

                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )

                output = response.choices[0].message.content.strip()
                print("LLM SUCCESS:", model)

                # ---------- CLEAN OUTPUT ----------
                output = output.strip()
                output = output.replace("\n", " ")

                bad_phrases = [
                    "missing:",
                    "based on",
                    "the resume",
                    "job description",
                    "skills are",
                    "following",
                    "here are",
                    "the following",
                    "required skills",
                    "resume:",
                    "jd:"
                ]

                for phrase in bad_phrases:
                    output = output.lower().replace(phrase, "")

                skills_list = [s.strip().title() for s in output.split(",")]

                skills_list = [
                    s for s in skills_list
                    if 2 < len(s) < 30 and not any(char.isdigit() for char in s)
                ]

                skills_list = list(dict.fromkeys(skills_list))
                skills_list = skills_list[:6]

                if skills_list:
                    return "Missing: " + ", ".join(skills_list)

                return ""

            except Exception as e:
                print(f"Model {model} failed:", e)

        return ""