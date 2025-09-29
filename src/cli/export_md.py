import os
import sys
import base64
import json
import requests
import fitz  # PyMuPDF library
from dotenv import load_dotenv

def get_text_from_image(image_data, api_key):
    """
    Sends image data to the Gemini API for text extraction (OCR).

    Args:
        image_data (bytes): The raw image data.
        api_key (str): Your Gemini API key.

    Returns:
        str: The extracted text or an error message.
    """
    # The API URL for the gemini-2.5-flash-preview-05-20 model
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # Convert the image data to a Base64 string
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    # Construct the API payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Extract all text from this scanned document page. Do not include any additional commentary, just the extracted text."
                    },
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": encoded_string
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_data = response.json()

        # Check for candidates and text
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

def main():
    """
    Main function to process all pages of a PDF file.
    """
    # --- Configuration ---
    # The name of the output Markdown file.
    output_markdown_file = "book_text.md"
    
    # Path to the .env file. Update this path if your .env file is in a different location.
    env_file_path = os.path.join(os.getcwd(), '../../.env')

    # Load environment variables from .env file
    load_dotenv(dotenv_path=env_file_path)

    # Get the API key from the environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please ensure it is set in your .env file.")
        print(f"Looked for .env file at: {env_file_path}")
        return

    # Get the PDF file path from the command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python scan_to_markdown.py <path_to_pdf_file>")
        return

    input_pdf_file = sys.argv[1]

    # Check if the PDF file exists
    if not os.path.exists(input_pdf_file):
        print(f"Error: PDF file not found at '{input_pdf_file}'.")
        return

    extracted_pages = []
    
    try:
        pdf_document = fitz.open(input_pdf_file)
        num_pages = pdf_document.page_count
        
        print(f"Found {num_pages} page(s) in the PDF file.")

        for i in range(4):
            print(f"Processing page {i+1}/{num_pages}...")
            
            # Render the page to a high-resolution image in memory
            page = pdf_document.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # Render at 300 DPI
            image_data = pix.tobytes("jpeg")
            
            text = get_text_from_image(image_data, api_key)
            
            if text.startswith(("HTTP error", "Error encoding")):
                print(f"Failed to process page {i+1}: {text}")
                # Nous arrêtons ici pour le débogage de la première page
                return
            else:
                print(f"Successfully extracted text from page {i+1}.")
                extracted_pages.append(text)

        pdf_document.close()

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return

    # Write all the extracted text to a single Markdown file
    with open(output_markdown_file, "w", encoding="utf-8") as f:
        f.write("# Extracted Text from Book Scans\n\n")
        for i, page_text in enumerate(extracted_pages):
            f.write(f"## Page {i + 1}\n\n")
            f.write(page_text)
            f.write("\n\n---\n\n")  # Separator for pages

    print("\nProcessing complete!")
    print(f"All extracted text has been saved to '{output_markdown_file}'.")

if __name__ == "__main__":
    main()
