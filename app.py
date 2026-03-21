import streamlit as st
import pandas as pd
import plotly.express as px

from utils.file_parser import extract_text
from pipeline.recruitment_pipeline import evaluate_candidate

# ---------- UI THEME ----------
st.markdown("""
<style>
/* APP BACKGROUND */
.stApp{
    background: linear-gradient(135deg,#121417,#1C1F26);
    color:#F8FAFC;
}

/* INPUT BOXES */
textarea, input, .stNumberInput input{
    background:#1C1F26 !important;
    color:#F8FAFC !important;
    border-radius:8px !important;
    border:1px solid #2A2E37 !important;
}

/* BUTTON STYLE */
div.stButton > button,
[data-testid="stFileUploader"] button{
    background: linear-gradient(135deg,#4F46E5,#06B6D4) !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:0.6em 1.7em !important;
    font-weight:600 !important;
    transition: all 0.25s ease;
}

div.stButton > button:hover,
[data-testid="stFileUploader"] button:hover{
    transform: translateY(-3px);
    box-shadow:0px 8px 18px rgba(79,70,229,0.45);
}

/* METRIC CARDS */
[data-testid="stMetric"]{
    background:#1C1F26;
    padding:18px;
    border-radius:12px;
    border:1px solid #2A2E37;
}

/* DATA TABLE */
[data-testid="stDataFrame"]{
    background:#1C1F26;
    border-radius:12px;
    border:1px solid #2A2E37;
}

h1,h2,h3{
    color:#E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# ---------- APP TITLE ----------
st.title("SmartHire AI - Semantic & Behavioral ATS")

# ---------- INPUTS ----------
jd = st.text_area("Paste Job Description")

skills = st.text_input("Required Skills (comma separated)")
skills = [s.strip() for s in skills.split(",") if s]

required_years = st.number_input("Required Experience (Years)", 0, 20, 0)

files = st.file_uploader(
    "Upload Candidate Resumes",
    accept_multiple_files=True
)

# ---------- RUN ATS ----------
if st.button("Run ATS Evaluation"):

    if not files:
        st.warning("Please upload at least one resume.")
        st.stop()

    results = []

    for file in files:
        text = extract_text(file)

        score, fraud, status, reason, exp, llm_output = evaluate_candidate(
            text,
            jd,
            skills,
            file_path=file
        )

        # Clean candidate name
        name = file.name.replace("_Resume", "").replace(".pdf","").replace(".docx","")

        # ---------- LLM SKILL EXTRACTION ----------
        llm_skills = ""
        if llm_output and "Missing:" in llm_output:
            llm_skills = llm_output.replace("Missing:", "").strip()

        results.append({
            "Candidate": name,
            "Score": round(score, 2),
            "Experience": exp,
            "Fraud": fraud,
            "Status": status,
            "Reason": reason,
            "LLM Skills": llm_skills
        })

    df = pd.DataFrame(results)

    # ---------- TABS ----------
    tab1, tab2 = st.tabs(["📊 ATS Results", "🧠 AI Insights"])

    # 📊 TAB 1 — ATS RESULTS
    with tab1:
        st.subheader("Candidate Evaluation Table")
        df.index = df.index + 1
        st.dataframe(df.drop(columns=["LLM Skills"]), use_container_width=True)

        # ---------- METRICS ----------
        total = len(df)
        shortlisted = len(df[df.Status == "Shortlisted"])
        fraud_count = len(df[df["Fraud"] == True])
        fraud_rejected = len(df[(df.Status == "Rejected") & (df.Fraud == True)])
        skill_rejected = len(df[(df.Status == "Rejected") & (df.Fraud == False)])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Candidates", total)
        col2.metric("Shortlisted", shortlisted)
        col3.metric("Rejected (Skill)", skill_rejected)
        col4.metric("Fraud Detected", fraud_count)

        # ---------- DONUT CHART ----------
        st.subheader("Candidate Distribution")
        donut = px.pie(
            values=[shortlisted, skill_rejected, fraud_rejected],
            names=["Shortlisted","Skill Gap","Fraud"],
            hole=0.55,
            color_discrete_sequence=["#2563EB","#D97706","#B45309"]
        )
        donut.update_layout(paper_bgcolor="#1C1F26", font_color="#E2E8F0")
        st.plotly_chart(donut, use_container_width=True)

        # ---------- BAR CHART ----------
        st.subheader("Candidate Score Comparison")
        df_sorted = df.sort_values(by="Score")
        df_sorted["Category"] = df_sorted["Score"].apply(
            lambda x: "Selected (>=60)" if x >= 60 else "Below Threshold"
        )

        fig = px.bar(
            df_sorted,
            x="Candidate",
            y="Score",
            color="Category",
            text="Score",
            range_y=[0,100],
            color_discrete_map={
                "Selected (>=60)": "#2563EB",
                "Below Threshold": "#D97706"
            }
        )
        fig.update_traces(textposition="outside")
        fig.add_hline(
            y=60,
            line_dash="dash",
            line_color="green",
            annotation_text="Selection Threshold (60%)"
        )
        fig.update_layout(
            xaxis_title="Candidates",
            yaxis_title="Score (%)",
            paper_bgcolor="#1C1F26",
            plot_bgcolor="#1C1F26",
            font_color="#E2E8F0"
        )
        st.plotly_chart(fig, use_container_width=True)

        # ---------- SCORE DISTRIBUTION ----------
        st.subheader("Score Distribution")
        bins = [0,20,40,60,80,100]
        labels = ["0-20","21-40","41-60","61-80","81-100"]
        temp_df = df.copy()
        temp_df["Score Range"] = pd.cut(
            temp_df["Score"],
            bins=bins,
            labels=labels,
            include_lowest=True
        )
        dist = temp_df["Score Range"].value_counts().sort_index().reset_index()
        dist.columns = ["Score Range","Candidates"]
        fig = px.bar(
            dist,
            x="Score Range",
            y="Candidates",
            text="Candidates",
            color="Score Range",
            color_discrete_sequence=["#2563EB","#3B82F6","#60A5FA","#93C5FD","#BFDBFE"]
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_title="Score Range",
            yaxis_title="Number of Candidates",
            plot_bgcolor="#1C1F26",
            paper_bgcolor="#1C1F26",
            font_color="#E2E8F0",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # 🧠 TAB 2 — AI INSIGHTS
    with tab2:
        st.subheader("AI Skill Gap Analysis")
        llm_df = df[["Candidate", "LLM Skills"]]
        llm_df = llm_df[llm_df["LLM Skills"] != ""]

        if not llm_df.empty:
            llm_df["LLM Skills"] = llm_df["LLM Skills"].apply(
                lambda x: "\n• " + "\n• ".join([s.strip() for s in x.split(",")])
            )
            st.dataframe(llm_df, use_container_width=True)
        else:
            st.info("No AI insights available")