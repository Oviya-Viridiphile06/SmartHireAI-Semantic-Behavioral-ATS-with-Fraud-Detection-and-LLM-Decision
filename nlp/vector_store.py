from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_relevant_chunks(resume, jd):

    sentences = resume.split(".")
    jd_embedding = model.encode(jd, convert_to_tensor=True)

    scored = []

    for s in sentences:
        emb = model.encode(s, convert_to_tensor=True)
        score = util.cos_sim(emb, jd_embedding)
        scored.append((s, score.item()))

    # Top 5 relevant lines
    top_chunks = sorted(scored, key=lambda x: x[1], reverse=True)[:5]

    return " ".join([c[0] for c in top_chunks])