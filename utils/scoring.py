import re

def generate_abbreviation(skill):
    words = skill.split()
    return "".join([w[0] for w in words if len(w) > 1]).lower()


def expand_skills(skills):
    skill_map = {}

    for skill in skills:
        skill_lower = skill.lower().strip()
        abbr = generate_abbreviation(skill_lower)

        variants = {skill_lower}

        if abbr and abbr != skill_lower:
            variants.add(abbr)

        skill_map[skill_lower] = variants

    return skill_map

def keyword_match(resume_text, skills):
    text = resume_text.lower()
    expanded_skills = expand_skills(skills)

    score = 0
    important_skills = list(expanded_skills.keys())[:7]
    max_score = len(important_skills) * 10

    for skill in important_skills:
        variants = expanded_skills[skill]

        occurrences = max(
            len(re.findall(rf"\b{v}\b", text))
            for v in variants
        )

        if occurrences == 0:
            continue
        elif occurrences == 1:
            score += 2
        elif occurrences <= 4:
            score += 6
        else:
            score += 7   # controlled scoring (no inflation)

    return (score / max_score) * 100

def skill_context_score(resume_text, skills):
    sentences = re.split(r'[.!?]', resume_text.lower())
    expanded_skills = expand_skills(skills)

    score = 0

    context_words = [
        "project", "developed", "built", "implemented",
        "experience", "designed", "created",
        "worked", "internship", "certificate", "github", "tech stack"
    ]

    for skill, variants in expanded_skills.items():

        for sentence in sentences:

            if any(re.search(rf"\b{v}\b", sentence) for v in variants):

                if any(word in sentence for word in context_words):
                    score += 10
                else:
                    score += 5

                break

    max_score = min(len(expanded_skills), 10) * 10
    return (score / max_score) * 100

def extract_experience(resume_text):
    matches = re.findall(r'(\d+)\s*(years|yrs)', resume_text.lower())
    if matches:
        return max(int(m[0]) for m in matches)
    return 0

def formatting_score(resume_text):
    score = 100
    if len(resume_text) < 500:
        score -= 30
    if "project" not in resume_text.lower():
        score -= 20
    if "education" not in resume_text.lower():
        score -= 10
    if "skill" not in resume_text.lower():
        score -= 20
    return max(score, 0)