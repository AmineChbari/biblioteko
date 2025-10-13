import os
import sys
import base64
import json
import requests
import fitz  # PyMuPDF
import argparse
from dotenv import load_dotenv
from mistralai import Mistral

import time


class OCRExtractor:
    """
    OCR text extractor for scanned book pages.
    Produces raw, unformatted text to avoid prompt poisoning.
    """

    RAW_PROMPT = """
    You are a highly reliable OCR extraction assistant.

    Your goal is to extract **all readable text** from the provided book page image.

    Follow these strict rules:

    1. **Output format**
    - Use the following structure:
        ```
        [METADATA]
        page_number: N
        language: [detected_language]
        text_quality: [good | partial | poor]
        missing_parts: [none | minor | major]
        ```

        [TEXT]
        (extracted text in reading order)
        ```

    2. **Extraction rules**
    - Extract all readable text exactly as it appears.
    - Keep the natural reading order:
        - Columns → left to right.
        - Top to bottom.
    - Preserve paragraph breaks with a blank line between paragraphs.
    - Ignore:
        - Decorative or non-text elements (borders, ornaments, backgrounds)
        - Captions under images or tables unless they are part of the main text.

    3. **Completion and normalization**
    - If small gaps or missing words are clearly predictable (e.g., in numbered lists, tables of contents, or page headers), fill them **logically** and mark them in brackets, e.g. `[50]`, `[continued text]`.
    - If text is unreadable or missing entirely, write `[unreadable]`.
    - Always prefer `[unreadable]` over guessing words.
    - If page number is visible, extract it. If not, estimate it logically (e.g., based on sequence continuity).

    4. **Consistency**
    - Do not rephrase, interpret, or translate.
    - Do not use markdown or additional formatting.
    - Be deterministic — for the same input, always return the same structure.

    Output only the final structured text (no commentary or explanations).

    """

    def __init__(self, engine="gemini", max_retries=3, cooldown=5):
        load_dotenv()
        self.engine = engine.lower()
        self.api_key = os.getenv(f"{engine.upper()}_API_KEY")
        self.model = os.getenv(f"{engine.upper()}_MODEL")
        self.max_retries = max_retries
        self.cooldown = cooldown

        if not self.api_key or not self.model:
            raise ValueError(f"Missing {engine.upper()}_API_KEY or {engine.upper()}_MODEL in .env")

    # --- Gemini request ---
    def _extract_gemini(self, image_data: bytes, page_number: int = None) -> str:
        encoded = base64.b64encode(image_data).decode("utf-8")
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": self.RAW_PROMPT},
                    {"inlineData": {"mimeType": "image/jpeg", "data": encoded}}
                ]
            }]
        }
        headers = {"Content-Type": "application/json"}

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=90)
                response.raise_for_status()
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    for part in candidates[0].get("content", {}).get("parts", []):
                        if "text" in part:
                            return part["text"]
                return ""
            except Exception as e:
                if attempt < self.max_retries:
                    print(
                        f"[Retry {attempt}/{self.max_retries}] Gemini failed on "
                        f"page {page_number or '?'}: {e}. Retrying in {self.cooldown}s..."
                    )
                    time.sleep(self.cooldown)
                else:
                    print(
                        f"[ERROR Gemini] Failed after {self.max_retries} attempts "
                        f"on page {page_number or '?'}: {e}"
                    )
                    return f"[ERROR Gemini page {page_number or '?'}] {e}"

    # --- Mistral request ---
    def _extract_mistral(self, image_data: bytes, page_number: int = None) -> str:
        encoded = base64.b64encode(image_data).decode("utf-8")

        for attempt in range(1, self.max_retries + 1):
            try:
                client = Mistral(api_key=self.api_key)
                response = client.chat.complete(
                    model=self.model,
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.RAW_PROMPT},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}
                        ]
                    }]
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < self.max_retries:
                    print(
                        f"[Retry {attempt}/{self.max_retries}] Mistral failed on "
                        f"page {page_number or '?'}: {e}. Retrying in {self.cooldown}s..."
                    )
                    time.sleep(self.cooldown)
                else:
                    print(
                        f"[ERROR Mistral] Failed after {self.max_retries} attempts "
                        f"on page {page_number or '?'}: {e}"
                    )
                    return f"[ERROR Mistral page {page_number or '?'}] {e}"

    # --- Unified extractor ---
    def extract_text(self, image_data: bytes, page_number: int = None) -> str:
        if self.engine == "gemini":
            return self._extract_gemini(image_data, page_number)
        elif self.engine == "mistral":
            return self._extract_mistral(image_data, page_number)
        else:
            raise ValueError("Unsupported engine. Use 'gemini' or 'mistral'.")


class OCRProcessor:
    """Handles file loading, page iteration, and saving raw text outputs."""

    def __init__(self, engine="gemini"):
        self.extractor = OCRExtractor(engine)
        self.temp_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/temp"))
        os.makedirs(self.temp_folder, exist_ok=True)

    def process(self, file_path: str, limit: int = None):
        ext = os.path.splitext(file_path)[1].lower()
        output_files = []

        if ext in [".jpg", ".jpeg", ".png"]:
            with open(file_path, "rb") as img:
                text = self.extractor.extract_text(img.read())
            out_path = os.path.join(self.temp_folder, f"{os.path.basename(file_path)}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            output_files.append(out_path)

        elif ext == ".pdf":
            pdf = fitz.open(file_path)
            num_pages = pdf.page_count
            limit = min(limit or num_pages, num_pages)
            print(f"Processing {limit} of {num_pages} pages...")

            for i in range(limit):
                page = pdf.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(600 / 72, 600 / 72))
                print(f"Processing page {i + 1}/{limit}...")
                text = self.extractor.extract_text(pix.tobytes("jpeg"), page_number=i + 1)
                out_path = os.path.join(self.temp_folder, f"{os.path.basename(file_path)}_p{i+1}.txt")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(text)
                output_files.append(out_path)
            pdf.close()
        else:
            raise ValueError("Unsupported file type (only PDF or image).")

        print(f"Saved {len(output_files)} raw OCR text files to {self.temp_folder}")
        return output_files


def main():
    parser = argparse.ArgumentParser(description="Run OCR extraction and export raw text.")
    parser.add_argument("file", help="Path to input PDF or image.")
    parser.add_argument("--engine", choices=["gemini", "mistral"], default="gemini")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    processor = OCRProcessor(engine=args.engine)
    processor.process(args.file, args.limit)


if __name__ == "__main__":
    main()
