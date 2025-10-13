import os
import json
import requests
import base64
import argparse
from dotenv import load_dotenv
from mistralai import Mistral


class MarkdownFormatter:
    """
    Uses a language model to reformat OCR raw text into clean Markdown.
    """

    PROMPT = """
    You are a text formatting assistant.
    The input is raw text extracted from scanned book pages.
    
    Your task:
    - Reformat it into clean Markdown.
    - Detect titles, subtitles, and chapter headers (use #, ##, ###).
    - Authors → under **Author(s)** section.
    - Publisher → under **Publisher** section.
    - Keep page numbers visible as `**Page N**`.
    - Preserve paragraph structure with blank lines.
    - If words are missing, use [unreadable].
    - Do NOT include commentary or explanations.

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
        payload = {
            "contents": [{"parts": [{"text": f"{self.PROMPT}\n\n{text}"}]}]
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        if "candidates" in data:
            for part in data["candidates"][0].get("content", {}).get("parts", []):
                if "text" in part:
                    return part["text"]
        return ""

    def _format_mistral(self, text: str) -> str:
        client = Mistral(api_key=self.api_key)
        response = client.chat.complete(
            model=self.model,
            messages=[
                {"role": "user", "content": self.PROMPT},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

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

    def export(self, input_file: str):
        with open(input_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        formatted = self.formatter.format_text(raw_text)
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_path = os.path.join(self.output_folder, f"{base_name}.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"Formatted Markdown saved to {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="Format OCR text into Markdown.")
    parser.add_argument("file", help="Path to raw OCR text file.")
    parser.add_argument("--engine", choices=["gemini", "mistral"], default="gemini")
    args = parser.parse_args()

    exporter = MarkdownExporter(engine=args.engine)
    exporter.export(args.file)


if __name__ == "__main__":
    main()
