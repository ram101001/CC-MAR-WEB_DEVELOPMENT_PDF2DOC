import streamlit as st
import io
from PyPDF2 import PdfReader, PdfFileWriter
from docx import Document


def convert_pdf_to_doc(file):
    # Load PDF file
    pdf_reader = PdfReader(file)

    # Create new Word document
    doc = Document()

    # Iterate through pages and add them to the document
    for page in range(len(pdf_reader.pages)):
        # Extract text from page
        page_text = pdf_reader.pages[page].extract_text()

        # Add text to document
        doc.add_paragraph(page_text)

    # Save document to memory buffer
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    output_buffer.seek(0)

    return output_buffer

# Set up Streamlit app
st.title("PDF to DOC Converter")

# File uploader
file = st.file_uploader("Upload a PDF file", type="pdf")

# Convert button
if st.button("Convert"):
    # Check if file was uploaded
    if file is not None:
        # Convert PDF to DOC
        output_buffer = convert_pdf_to_doc(file)

        # Download DOC file
        st.download_button(
            label="Download DOC file",
            data=output_buffer,
            file_name=f"{file.name.split('.')[0]}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    else:
        st.warning("Please upload a PDF file.")
