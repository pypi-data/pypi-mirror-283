import fitz
import os
import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pdfa3extractor <pdf_path> <output_folder>")
    else:
        extract_embedded_files(sys.argv[1], sys.argv[2])
