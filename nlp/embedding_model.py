from sentence_transformers import SentenceTransformer, util

# Load model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(resume, jd):

    emb1 = model.encode(resume, convert_to_tensor=True)
    emb2 = model.encode(jd, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2)

    return round(float(score) * 100, 2)

