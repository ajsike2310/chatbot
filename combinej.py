import os
import json
from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned_text = "\n".join(line for line in lines if line)
    return cleaned_text

def create_combined_json(input_dir="output", output_file="all_pages.json"):
    files = [f for f in os.listdir(input_dir) if f.endswith(".html")]

    combined_data = []

    for file in files:
        input_path = os.path.join(input_dir, file)
        text = extract_text_from_html(input_path)
        combined_data.append({
            "filename": file,
            "content": text
        })
        print(f"Processed {file}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)

    print(f"Combined JSON saved to {output_file}")

if __name__ == "__main__":
    create_combined_json()
