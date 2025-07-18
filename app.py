from flask import Flask, render_template, send_from_directory, request
import os
import json

app = Flask(__name__, static_folder=\'static\', template_folder=\'templates\')

# Configuration for document paths
DOC_DIR = os.path.join(os.path.dirname(__file__), \'sample_docs\')

# Sample documents for demo
sample_docs = {
    "Sample PDF (7 pages)": "sample_pdf.pdf",
    "Sample DOCX (2 pages)": "sample_docx.docx", 
    "Sample PPTX (5 slides)": "sample_pptx.pptx",
    "Sample Excel (5 sheets)": "sample_excel.xlsx"
}

@app.route(\'/\')
def index():
    return render_template(\'index.html\', sample_docs=sample_docs)

@app.route(\'/docs/<filename>\')
def serve_doc(filename):
    return send_from_directory(DOC_DIR, filename)

@app.route(\'/get_doc_info\', methods=[\'POST\'])
def get_doc_info():
    data = request.get_json()
    doc_name = data.get(\'doc_name\')
    
    if doc_name not in sample_docs:
        return json.dumps({\'error\': \'Document not found\'}), 404
    
    file_path = os.path.join(DOC_DIR, sample_docs[doc_name])
    
    # In a real application, you would implement logic here to get page count
    # for each document type. For this demo, we\'ll use hardcoded values
    # based on the sample documents we generated.
    
    if "PDF" in doc_name:
        page_count = 7
    elif "DOCX" in doc_name:
        page_count = 2
    elif "PPTX" in doc_name:
        page_count = 5
    elif "Excel" in doc_name:
        page_count = 5
    else:
        page_count = 1 # Default

    return json.dumps({
        \'file_path\': f\'/docs/{sample_docs[doc_name]}\\'",
        \'page_count\': page_count
    })

if __name__ == \'__main__\':
    app.run(host=\'0.0.0.0\', port=5000, debug=True)


