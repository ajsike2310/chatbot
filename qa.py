import json
import time
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="your api")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_qna_from_text(text, section_name):
    prompt = f"""
You are reading a section from a college website. Based **only on the given content below**, generate possible student-style questions and their exact answers. 
Avoid general knowledge or unrelated questions.

Format the result strictly as a JSON array of all the possible question-answer pairs like this:
[
  {{ "question": "...", "answer": "..." }},
  ...
]

CONTENT STARTS BELOW:
{text[:12000]}
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text

        # Attempt to parse JSON from model response
        try:
            qna_list = json.loads(raw)
        except:
            qna_list = json.loads(raw[raw.find("["): raw.rfind("]")+1])
        return {
            "section": section_name,
            "qa": qna_list
        }

    except Exception as e:
        print(f"⚠️ Error generating Q&A for section '{section_name}': {e}")
        return None

def process_all_pages(input_path="all_pages.json", output_path="labeled_qa.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    all_qna = []
    for i, page in enumerate(pages):
        section = page["filename"]
        text = page["content"]

        if not text.strip():
            continue

        print(f"🔄 Processing [{i+1}/{len(pages)}]: {section}")
        result = generate_qna_from_text(text, section)
        if result:
            all_qna.append(result)
            print(f"✅ Added {len(result['qa'])} Q&A pairs from: {section}")
        time.sleep(1.5)  # Avoid rate limit

    # Save to output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_qna, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 All Q&A data saved to {output_path}")

if __name__ == "__main__":
    process_all_pages()
