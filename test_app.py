#!/usr/bin/env python3

import os
import sys
sys.path.append('/home/ubuntu/gradio_document_previewer')

from document_previewer import DocumentPreviewer

def test_document_loading():
    previewer = DocumentPreviewer()
    
    # Test file paths
    test_files = [
        "/home/ubuntu/gradio_document_previewer/sample_docs/sample_pdf.pdf",
        "/home/ubuntu/gradio_document_previewer/sample_docs/sample_docx.docx",
        "/home/ubuntu/gradio_document_previewer/sample_docs/sample_pptx.pptx",
        "/home/ubuntu/gradio_document_previewer/sample_docs/sample_excel.xlsx"
    ]
    
    for file_path in test_files:
        print(f"\nTesting: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            print(f"Supported: {previewer.is_supported(file_path)}")
            try:
                page_count = previewer.get_page_count(file_path)
                print(f"Page count: {page_count}")
                
                if page_count > 0:
                    preview = previewer.preview_page(file_path, 1)
                    print(f"Preview generated: {preview is not None}")
                    if preview:
                        print(f"Preview size: {preview.size}")
                else:
                    print("No pages found")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("File not found!")

if __name__ == "__main__":
    test_document_loading()

