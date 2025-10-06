import os
import sys
import base64
import json
import requests
import fitz  # PyMuPDF
import argparse
from dotenv import load_dotenv
from mistralai import Mistral


# ---------------------------
# 1. PROMPT
# ---------------------------
PROMPT = """
You are an OCR and text reconstruction assistant specialized in scanned books.

Your task:
- Extract ALL readable text from this scanned book page, even if partially blurry or incomplete.
- If the page has multiple columns, reconstruct the text in correct reading order.
- Ignore illustrations, captions, decorative text, or images.
- Only include the main printed text of the book.

Output format:
- Use clean **Markdown** structure.
- Titles, subtitles, chapter headings → use `#`, `##`, `###`.
- Authors → under a section called **Author(s)**.
- Publisher → under a section called **Publisher**.
- Keep page numbers (if visible) in a separate line, formatted as `**Page N**`.
- Keep paragraphs separated by blank lines.
- Do NOT add commentary, explanations, or guesses outside the text itself.

If some parts are unreadable, leave a placeholder `[unreadable]`.

Return only the Markdown text.
"""


# ---------------------------
# 2. GEMINI EXPORT FUNCTION
# ---------------------------
def get_text_from_image_gemini(image_data: bytes, api_key: str, model: str, prompt: str) -> str:
    """Send image data to Gemini API and return extracted text."""
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": "image/jpeg", "data": encoded_string}},
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()

        if "candidates" in response_data and response_data["candidates"]:
            candidate = response_data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    if "text" in part:
                        return part["text"]
        return "No text extracted."

    except requests.exceptions.HTTPError as err:
        return f"HTTP error occurred: {err}"
    except Exception as err:
        return f"An error occurred: {err}"


# ---------------------------
# 3. MISTRAL EXPORT FUNCTION
# ---------------------------
def get_text_from_image_mistral(image_data: bytes, api_key: str, model: str, prompt: str) -> str:
    """Send image data to Mistral API and return extracted text."""
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    try:
        client = Mistral(api_key=api_key)
        response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_string}"
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
    except Exception as err:
        return f"An error occurred: {err}"


# ---------------------------
# 4. EXPORT FUNCTIONS
# ---------------------------
def export_gemini(file_path: str, output_file: str, limit: int = None):
    """Extract text using Gemini API and export to Markdown."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key or not model:
        print("Error: Missing GEMINI_API_KEY or GEMINI_MODEL in .env file.")
        return

    extracted_pages = process_file(file_path, api_key, model, PROMPT, get_text_from_image_gemini, limit)

    write_markdown(output_file, extracted_pages)


def export_mistral(file_path: str, output_file: str, limit: int = None):
    """Extract text using Mistral API and export to Markdown."""
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    model = os.getenv("MISTRAL_MODEL")

    if not api_key or not model:
        print("Error: Missing MISTRAL_API_KEY or MISTRAL_MODEL in .env file.")
        return

    extracted_pages = process_file(file_path, api_key, model, PROMPT, get_text_from_image_mistral, limit)

    write_markdown(output_file, extracted_pages)


# ---------------------------
# 5. FILE PROCESSING FUNCTION
# ---------------------------
def process_file(file_path: str, api_key: str, model: str, prompt: str, extractor_func, limit: int = None):
    """Process a file (PDF or image) and extract text page by page."""
    extracted_pages = []

    file_ext = os.path.splitext(file_path)[1].lower()

    # Handle single image
    if file_ext in [".jpg", ".jpeg", ".png"]:
        with open(file_path, "rb") as img_file:
            image_data = img_file.read()
            text = extractor_func(image_data, api_key, model, prompt)
            extracted_pages.append(text)

    # Handle PDF
    elif file_ext == ".pdf":
        pdf_document = fitz.open(file_path)
        num_pages = pdf_document.page_count
        print(f"Found {num_pages} page(s) in the PDF file.")

        max_pages = limit if limit and limit < num_pages else num_pages

        for i in range(max_pages):
            print(f"Processing page {i + 1}/{max_pages}...")
            page = pdf_document.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # 300 DPI
            image_data = pix.tobytes("jpeg")
            text = extractor_func(image_data, api_key, model, prompt)
            extracted_pages.append(text)
        pdf_document.close()
    else:
        print("Error: Unsupported file type. Only PDF or image files are supported.")

    return extracted_pages

# ---------------------------
# 6. MARKDOWN WRITER
# ---------------------------
def write_markdown(output_file: str, extracted_pages: list):
    """Write extracted text into a Markdown file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Extracted Text\n\n")
        for i, page_text in enumerate(extracted_pages):
            f.write(f"## Page {i + 1}\n\n")
            f.write(page_text or "")
            f.write("\n\n---\n\n")
    print(f"\nAll extracted text saved to '{output_file}'.")


# ---------------------------
# 7. MAIN ENTRY POINT
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Export text from PDF or image using Gemini or Mistral API."
    )
    parser.add_argument("file", help="Path to the input file (PDF or image).")
    parser.add_argument(
        "--engine",
        choices=["gemini", "mistral"],
        default="gemini",
        help="Choose the LLM engine (default: gemini).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of pages to process (default: all pages).",
    )
    args = parser.parse_args()

    # --- Construct input file path ---
    file_path = args.file
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # --- Construct output folder path ---
    # Script is in biblioteko/src/CLI/, output goes to biblioteko/data/scans/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    output_folder = os.path.join(project_root, "data", "scans")
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    # Output Markdown file
    output_file = os.path.join(output_folder, f"{base_name}.md")

    # --- Call the appropriate export function ---
    if args.engine == "gemini":
        export_gemini(file_path, output_file, limit=args.limit)
    elif args.engine == "mistral":
        export_mistral(file_path, output_file, limit=args.limit)
    else:
        print("Error: Unsupported engine. Please use 'gemini' or 'mistral'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
