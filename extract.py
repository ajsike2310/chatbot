import os
import json
from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned_text = "\n".join(line for line in lines if line)
    return cleaned_text

def extract_and_save(input_dir="output", txt_dir="clean_text", json_dir="json_text"):
    os.makedirs(txt_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".html")]

    for file in files:
        input_path = os.path.join(input_dir, file)
        text = extract_text_from_html(input_path)

        # Save as .txt
        txt_path = os.path.join(txt_dir, file.replace(".html", ".txt"))
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Save as JSON
        json_path = os.path.join(json_dir, file.replace(".html", ".json"))
        data = {
            "filename": file,
            "content": text
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Processed {file} -> {txt_path} and {json_path}")

if __name__ == "__main__":
    extract_and_save()
