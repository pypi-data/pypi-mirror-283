import fitz  # PyMuPDF
import os
import sys
import argparse

def extract_embedded_files(pdf_path, output_folder):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Iterate through embedded files
    for i in range(doc.embfile_count()):
        # Get the embedded file info
        file_info = doc.embfile_info(i)
        file_name = file_info["name"]
        
        # Extract the embedded file if it is an XML
        if file_name.endswith(".xml"):
            # Read the embedded file
            file_data = doc.embfile_get(i)
            
            # Ensure output directory exists
            os.makedirs(output_folder, exist_ok=True)
            
            # Save the extracted file
            output_path = os.path.join(output_folder, file_name)
            with open(output_path, "wb") as output_file:
                output_file.write(file_data)
                
            print(f"Extracted: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract embedded XML files from PDF/A-3 documents."
    )
    parser.add_argument("pdf_path", help="Path to the PDF/A-3 file.")
    parser.add_argument("output_folder", help="Folder to save the extracted XML files.")
    
    args = parser.parse_args()
    
    extract_embedded_files(args.pdf_path, args.output_folder)

if __name__ == "__main__":
    main()
