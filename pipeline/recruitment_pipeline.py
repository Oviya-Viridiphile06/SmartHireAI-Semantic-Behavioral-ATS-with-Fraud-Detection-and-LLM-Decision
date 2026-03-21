from agents.resume_agent import ResumeAgent
from agents.fraud_agent import FraudAgent
from agents.scoring_agent import ScoringAgent
from agents.decision_agent import DecisionAgent
from agents.email_agent import EmailAgent
from agents.llm_agent import LLMAgent

# Initialize Agents
resume_agent = ResumeAgent()
fraud_agent = FraudAgent()
scoring_agent = ScoringAgent()
decision_agent = DecisionAgent()
email_agent = EmailAgent()
llm_agent = LLMAgent()


def evaluate_candidate(resume_text, jd, skills, file_path=None):

    # STEP 1: Resume Preprocessing
    processed_resume = resume_agent.process(resume_text)

    # STEP 2: Candidate Info Extraction
    candidate_email = resume_agent.extract_email(processed_resume)
    candidate_name = resume_agent.extract_name(processed_resume, candidate_email)

    # STEP 3: Fraud Detection
    fraud, fraud_reason = fraud_agent.detect(processed_resume, skills, file_path)

    # STEP 4: Scoring
    score, experience = scoring_agent.calculate_score(processed_resume, jd, skills)

    # STEP 5: Rule-Based Decision
    status, reason = decision_agent.decide(score, fraud, fraud_reason)

    # STEP 6: LLM Override (Borderline 50-60)
    llm_output = ""
    if not fraud and 50 <= score < 60:
        llm_decision = llm_agent.get_final_decision(processed_resume, jd)
        if llm_decision and llm_decision.strip().upper() == "SELECT":
            status = "Shortlisted"
            reason = "LLM override (borderline candidate selected)"

    # STEP 7: Skill Gap / AI Insights
    if fraud:
        final_reason = fraud_reason
        llm_output = ""
    elif status == "Rejected":
        llm_output = llm_agent.get_skill_gap(processed_resume[:2000], jd[:1000])
        if not llm_output or "Missing:" not in llm_output:
            llm_output = ""
        final_reason = "Insufficient skill match"
    elif status == "Shortlisted":
        final_reason = "Qualified"
    else:
        final_reason = reason

    # STEP 8: Email Notification
    email_agent.notify(candidate_email, candidate_name, status, final_reason)

    # FINAL RETURN
    return score, fraud, status, final_reason, experience, llm_output