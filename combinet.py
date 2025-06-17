import os

def combine_text_files(input_dir="clean_text", output_file="combined_text.txt"):
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    files.sort()  # optional: sort filenames alphabetically

    with open(output_file, "w", encoding="utf-8") as outfile:
        for file in files:
            file_path = os.path.join(input_dir, file)
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(f"----- Start of {file} -----\n\n")
                outfile.write(content)
                outfile.write(f"\n\n----- End of {file} -----\n\n")

            print(f"Added {file}")

    print(f"All text files combined into {output_file}")

if __name__ == "__main__":
    combine_text_files()
