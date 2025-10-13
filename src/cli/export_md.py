import os
import json
import requests
import argparse
from dotenv import load_dotenv
from mistralai import Mistral


class MarkdownFormatter:
    """
    Uses a language model to reformat OCR raw text into clean Markdown.
    """

    PROMPT = """
    You are a text normalization and formatting assistant.

    Input: raw text extracted from scanned book pages (with metadata).

    Your goal is to transform it into **clean, structured Markdown**.

    Follow these strict rules:

    1. **Metadata**
    - Convert `[METADATA]` section into a YAML-style header at the top:
        ```
        ---
        page: N
        language: [detected_language]
        text_quality: [value]
        missing_parts: [value]
        ---
        ```

    2. **Page numbering**
    - Add a visible marker at the top:  
        `**Page N**`

    3. **Formatting rules**
    - Detect and format:
        - Titles → `#`
        - Subtitles or sections → `##` or `###`
        - Author names → under a `**Author(s):**` line
        - Publisher info → under a `**Publisher:**` line
    - Preserve the original paragraph structure (one blank line between paragraphs).
    - Keep any `[unreadable]` tokens exactly as they appear.
    - Normalize spacing and punctuation, but **do not rewrite or interpret**.

    4. **Completion logic**
    - If lists or sequences (e.g., numbered TOCs) are truncated, continue them **only when clearly implied** (e.g., “1 … 3 … 5” → complete as 1–5).
    - Mark all completions with square brackets, e.g. `[4]`, `[continued section]`.
    - Never invent content that is not structurally or logically implied.

    5. **Output rules**
    - Output pure Markdown only (no code fences, no explanations, no commentary).
    - Be deterministic — identical input yields identical output.

    Output only the Markdown text.

    """

    def __init__(self, engine="gemini"):
        load_dotenv()
        self.engine = engine.lower()
        self.api_key = os.getenv(f"{engine.upper()}_API_KEY")
        self.model = os.getenv(f"{engine.upper()}_MODEL")

        if not self.api_key or not self.model:
            raise ValueError(f"Missing {engine.upper()}_API_KEY or {engine.upper()}_MODEL in .env")

    def _format_gemini(self, text: str) -> str:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": f"{self.PROMPT}\n\n{text}"}]}]}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=90)
            response.raise_for_status()
            data = response.json()
            if "candidates" in data:
                for part in data["candidates"][0].get("content", {}).get("parts", []):
                    if "text" in part:
                        return part["text"]
            return ""
        except Exception as e:
            print(f"[ERROR Gemini] {e}")
            return f"[ERROR Gemini] {e}"

    def _format_mistral(self, text: str) -> str:
        try:
            client = Mistral(api_key=self.api_key)
            response = client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "user", "content": self.PROMPT},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[ERROR Mistral] {e}")
            return f"[ERROR Mistral] {e}"

    def format_text(self, text: str) -> str:
        if self.engine == "gemini":
            return self._format_gemini(text)
        elif self.engine == "mistral":
            return self._format_mistral(text)
        else:
            raise ValueError("Unsupported engine.")


class MarkdownExporter:
    """Loads raw OCR files and exports formatted Markdown files."""

    def __init__(self, engine="gemini"):
        self.formatter = MarkdownFormatter(engine)
        self.output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/scans"))
        os.makedirs(self.output_folder, exist_ok=True)

    def export_file(self, input_file: str):
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                raw_text = f.read()

            formatted = self.formatter.format_text(raw_text)
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_path = os.path.join(self.output_folder, f"{base_name}.md")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(formatted)

            print(f"[OK] Formatted Markdown saved to {output_path}")
            return output_path

        except Exception as e:
            print(f"[ERROR] Failed to export {input_file}: {e}")
            return None

    def export_folder(self, folder_path: str):
        if not os.path.isdir(folder_path):
            print(f"[ERROR] Folder not found: {folder_path}")
            return

        files = [f for f in os.listdir(folder_path) if f.lower().endswith(".txt")]
        if not files:
            print(f"[INFO] No .txt files found in {folder_path}")
            return

        print(f"Processing {len(files)} file(s) from folder: {folder_path}")
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            self.export_file(file_path)


def main():
    parser = argparse.ArgumentParser(description="Format OCR text into Markdown.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to a single raw OCR text file.")
    group.add_argument("--folder", help="Path to a folder containing raw OCR text files.")
    parser.add_argument("--engine", choices=["gemini", "mistral"], default="gemini", help="LLM engine to use.")
    args = parser.parse_args()

    exporter = MarkdownExporter(engine=args.engine)

    if args.file:
        exporter.export_file(args.file)
    elif args.folder:
        exporter.export_folder(args.folder)


if __name__ == "__main__":
    main()
