from agents.resume_agent import ResumeAgent
from agents.fraud_agent import FraudAgent
from agents.scoring_agent import ScoringAgent
from agents.decision_agent import DecisionAgent
from agents.email_agent import EmailAgent
from agents.llm_agent import LLMAgent

# -----------------------------
# Initialize Agents
# -----------------------------
resume_agent = ResumeAgent()
fraud_agent = FraudAgent()
scoring_agent = ScoringAgent()
decision_agent = DecisionAgent()
email_agent = EmailAgent()
llm_agent = LLMAgent()


def evaluate_candidate(resume_text, jd, skills, file_path=None):

    # =========================================================
    # STEP 1: Resume Preprocessing
    # =========================================================
    processed_resume = resume_agent.process(resume_text)

    # =========================================================
    # STEP 2: Candidate Information Extraction
    # =========================================================
    candidate_email = resume_agent.extract_email(processed_resume)
    candidate_name = resume_agent.extract_name(processed_resume, candidate_email)

    # =========================================================
    # STEP 3: Fraud Detection
    # =========================================================
    fraud, fraud_reason = fraud_agent.detect(
        processed_resume,
        skills,
        file_path
    )

    # =========================================================
    # STEP 4: Scoring (Hybrid: Keyword + Context + RAG + Semantic)
    # =========================================================
    score, experience = scoring_agent.calculate_score(
        processed_resume,
        jd,
        skills
    )

    # =========================================================
    # STEP 5: Rule-Based Decision
    # =========================================================
    status, reason = decision_agent.decide(score, fraud, fraud_reason)

    # =========================================================
    # STEP 6: LLM Override (Borderline Intelligence Layer)
    # =========================================================
    if not fraud and 50 <= score < 60:

        llm_decision = llm_agent.get_final_decision(processed_resume, jd)

        # Apply override ONLY if clearly SELECT
        if llm_decision and llm_decision.strip().upper() == "SELECT":
            status = "Shortlisted"
            reason = "LLM override (borderline candidate selected)"

    # =========================================================
    # STEP 7: Skill Gap Generation (GenAI Layer)
    # =========================================================
    if not fraud and status == "Rejected":
        skill_gap = "Insufficient skill match"  # fallback placeholder

    else:
        skill_gap = reason

    # =========================================================
    # STEP 8: Email Notification
    # =========================================================
    email_agent.notify(candidate_email, candidate_name, status, skill_gap)

    # =========================================================
    # FINAL OUTPUT
    # =========================================================
    return score, fraud, status, skill_gap, experience