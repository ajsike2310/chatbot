import json
from sentence_transformers import SentenceTransformer, util

# Load your Q&A data
with open("labeled_qa.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten all Q&A pairs
qa_list = []
questions = []
for section in data:
    for pair in section.get("qa", []):
        question = pair["question"]
        answer = pair["answer"]
        source = section["section"]
        questions.append(question)
        qa_list.append({
            "question": question,
            "answer": answer,
            "section": source
        })

# Load sentence transformer (local, fast model)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings for all questions
question_embeddings = model.encode(questions, convert_to_tensor=True)

# Chat loop
print("🤖 MBCET Semantic Chatbot (Offline)\nType 'exit' to quit.\n")
while True:
    query = input("You: ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Bye!")
        break

    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, question_embeddings)[0]
    best_match_idx = scores.argmax().item()
    best_match_score = scores[best_match_idx].item()

    if best_match_score < 0.5:
        print("❌ Sorry, I couldn't find a good match for that.")
    else:
        matched = qa_list[best_match_idx]
        print(f"\n📌 Matched Question: {matched['question']}")
        print(f"📖 Answer: {matched['answer']}")
        print(f"📂 Source Section: {matched['section']}")

