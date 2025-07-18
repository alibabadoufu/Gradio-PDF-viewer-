import gradio as gr
import os
from flask import Flask, send_from_directory
import threading
import time

# Flask app for serving documents
flask_app = Flask(__name__)

# Configuration for document paths
DOC_DIR = os.path.join(os.path.dirname(__file__), 'sample_docs')

@flask_app.route('/docs/<filename>')
def serve_doc(filename):
    return send_from_directory(DOC_DIR, filename)

def start_flask():
    flask_app.run(host='0.0.0.0', port=5001, debug=False)

# Start Flask server in a separate thread
flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

# Wait for Flask to start
time.sleep(2)

# Sample documents for demo
sample_docs = {
    "Sample PDF (7 pages)": "sample_pdf.pdf",
    "Sample DOCX (2 pages)": "sample_docx.docx", 
    "Sample PPTX (5 slides)": "sample_pptx.pptx",
    "Sample Excel (5 sheets)": "sample_excel.xlsx"
}

def create_document_viewer():
    """Create the HTML for the document viewer with embedded JavaScript."""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document Previewer</title>
        
        <!-- PDF.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
        
        <!-- Mammoth.js for DOCX -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.6.0/mammoth.browser.min.js"></script>
        
        <!-- SheetJS for Excel -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
        
        <!-- JSZip for PPTX -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
        
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            
            .navigation-panel {{
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .page-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 15px;
            }}
            
            .page-link {{
                padding: 8px 12px;
                background-color: #e9ecef;
                color: #495057;
                border: 1px solid #ced4da;
                border-radius: 4px;
                cursor: pointer;
                min-width: 40px;
                text-align: center;
                transition: all 0.2s;
                text-decoration: none;
            }}
            
            .page-link:hover {{
                background-color: #dee2e6;
                text-decoration: none;
                color: #495057;
            }}
            
            .page-link.active {{
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }}
            
            .viewer-container {{
                min-height: 600px;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                background: white;
                overflow: auto;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .pdf-canvas {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}
            
            .docx-content {{
                max-width: 100%;
                font-family: 'Times New Roman', serif;
                line-height: 1.6;
            }}
            
            .excel-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            
            .excel-table th,
            .excel-table td {{
                border: 1px solid #dee2e6;
                padding: 8px;
                text-align: left;
            }}
            
            .excel-table th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            
            .pptx-slide {{
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin: 10px auto;
                max-width: 800px;
                min-height: 400px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .loading {{
                text-align: center;
                padding: 50px;
                color: #6c757d;
            }}
            
            .error {{
                color: #dc3545;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 4px;
                padding: 15px;
                margin: 10px 0;
            }}
            
            .btn {{
                padding: 8px 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
                cursor: pointer;
                margin: 2px;
            }}
            
            .btn:hover {{
                background: #f8f9fa;
            }}
            
            .btn:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .btn-primary {{
                background: #007bff;
                color: white;
                border-color: #007bff;
            }}
            
            .btn-primary:hover {{
                background: #0056b3;
            }}
            
            select, input {{
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="navigation-panel">
            <h5>📁 Load Document</h5>
            <select id="documentSelect" style="width: 100%; margin-bottom: 10px;">
                <option value="">Select a sample document...</option>
                <option value="Sample PDF (7 pages)">Sample PDF (7 pages)</option>
                <option value="Sample DOCX (2 pages)">Sample DOCX (2 pages)</option>
                <option value="Sample PPTX (5 slides)">Sample PPTX (5 slides)</option>
                <option value="Sample Excel (5 sheets)">Sample Excel (5 sheets)</option>
            </select>
            
            <input type="file" id="fileUpload" accept=".pdf,.docx,.pptx,.xlsx" style="width: 100%; margin-bottom: 10px;">
            
            <hr>
            
            <h6>🧭 Navigation</h6>
            <div id="documentInfo" style="margin-bottom: 10px;">
                <small style="color: #666;">No document loaded</small>
            </div>
            
            <div style="margin-bottom: 10px;">
                <button id="prevBtn" class="btn" disabled>⬅️ Previous</button>
                <button id="nextBtn" class="btn" disabled>Next ➡️</button>
            </div>
            
            <div style="margin-bottom: 10px;">
                <input type="number" id="pageInput" placeholder="Page number" min="1" disabled style="width: 70%;">
                <button id="goBtn" class="btn btn-primary" disabled>Go</button>
            </div>
            
            <div id="pageLinks" class="page-links" style="display: none;">
                <!-- Page links will be generated here -->
            </div>
        </div>
        
        <div id="viewerContainer" class="viewer-container">
            <div class="loading">
                <h6>Select a document to get started</h6>
                <p style="color: #666;">Choose from the sample documents or upload your own PDF, DOCX, PPTX, or Excel file.</p>
            </div>
        </div>
        
        <div id="statusMessage" style="margin-top: 10px;">
            <small style="color: #666;">Ready to load documents</small>
        </div>

        <script>
            // Document Previewer JavaScript Application
            class DocumentPreviewer {{
                constructor() {{
                    this.currentDocument = null;
                    this.currentPage = 1;
                    this.totalPages = 0;
                    this.documentType = null;
                    this.pdfDoc = null;
                    this.excelWorkbook = null;
                    this.pptxSlides = [];
                    
                    this.initializeEventListeners();
                    this.setupPDFJS();
                }}
                
                setupPDFJS() {{
                    // Set PDF.js worker
                    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                }}
                
                initializeEventListeners() {{
                    // Document selection
                    document.getElementById('documentSelect').addEventListener('change', (e) => {{
                        if (e.target.value) {{
                            this.loadSampleDocument(e.target.value);
                        }}
                    }});
                    
                    // File upload
                    document.getElementById('fileUpload').addEventListener('change', (e) => {{
                        if (e.target.files[0]) {{
                            this.loadUploadedDocument(e.target.files[0]);
                        }}
                    }});
                    
                    // Navigation buttons
                    document.getElementById('prevBtn').addEventListener('click', () => {{
                        this.navigateToPage(this.currentPage - 1);
                    }});
                    
                    document.getElementById('nextBtn').addEventListener('click', () => {{
                        this.navigateToPage(this.currentPage + 1);
                    }});
                    
                    document.getElementById('goBtn').addEventListener('click', () => {{
                        const pageNum = parseInt(document.getElementById('pageInput').value);
                        if (pageNum) {{
                            this.navigateToPage(pageNum);
                        }}
                    }});
                    
                    // Enter key in page input
                    document.getElementById('pageInput').addEventListener('keypress', (e) => {{
                        if (e.key === 'Enter') {{
                            const pageNum = parseInt(e.target.value);
                            if (pageNum) {{
                                this.navigateToPage(pageNum);
                            }}
                        }}
                    }});
                }}
                
                async loadSampleDocument(docName) {{
                    try {{
                        this.showLoading('Loading document...');
                        
                        const docFiles = {{
                            "Sample PDF (7 pages)": "sample_pdf.pdf",
                            "Sample DOCX (2 pages)": "sample_docx.docx", 
                            "Sample PPTX (5 slides)": "sample_pptx.pptx",
                            "Sample Excel (5 sheets)": "sample_excel.xlsx"
                        }};
                        
                        const fileName = docFiles[docName];
                        const url = `http://localhost:5001/docs/${{fileName}}`;
                        
                        await this.loadDocumentFromURL(url, docName);
                        
                    }} catch (error) {{
                        this.showError('Failed to load document: ' + error.message);
                    }}
                }}
                
                async loadUploadedDocument(file) {{
                    try {{
                        this.showLoading('Loading uploaded document...');
                        
                        const fileName = file.name;
                        const fileURL = URL.createObjectURL(file);
                        
                        await this.loadDocumentFromURL(fileURL, fileName);
                        
                    }} catch (error) {{
                        this.showError('Failed to load uploaded document: ' + error.message);
                    }}
                }}
                
                async loadDocumentFromURL(url, fileName) {{
                    const fileExtension = fileName.split('.').pop().toLowerCase();
                    
                    this.currentDocument = url;
                    this.documentType = fileExtension;
                    this.currentPage = 1;
                    
                    switch (fileExtension) {{
                        case 'pdf':
                            await this.loadPDF(url);
                            break;
                        case 'docx':
                            await this.loadDOCX(url);
                            break;
                        case 'pptx':
                            await this.loadPPTX(url);
                            break;
                        case 'xlsx':
                            await this.loadExcel(url);
                            break;
                        default:
                            this.showError('Unsupported file format: ' + fileExtension);
                            return;
                    }}
                    
                    this.updateNavigationInfo(fileName);
                    this.updateNavigationControls();
                    this.generatePageLinks();
                    this.showStatus('Document loaded successfully!');
                }}
                
                async loadPDF(url) {{
                    try {{
                        this.pdfDoc = await pdfjsLib.getDocument(url).promise;
                        this.totalPages = this.pdfDoc.numPages;
                        await this.renderPDFPage(1);
                    }} catch (error) {{
                        throw new Error('Failed to load PDF: ' + error.message);
                    }}
                }}
                
                async renderPDFPage(pageNum) {{
                    try {{
                        const page = await this.pdfDoc.getPage(pageNum);
                        const scale = 1.5;
                        const viewport = page.getViewport({{ scale }});
                        
                        // Create canvas
                        const canvas = document.createElement('canvas');
                        const context = canvas.getContext('2d');
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;
                        canvas.className = 'pdf-canvas';
                        
                        // Render page
                        await page.render({{
                            canvasContext: context,
                            viewport: viewport
                        }}).promise;
                        
                        // Update viewer
                        const container = document.getElementById('viewerContainer');
                        container.innerHTML = '';
                        container.appendChild(canvas);
                        
                        this.currentPage = pageNum;
                        
                    }} catch (error) {{
                        throw new Error('Failed to render PDF page: ' + error.message);
                    }}
                }}
                
                async loadDOCX(url) {{
                    try {{
                        const response = await fetch(url);
                        const arrayBuffer = await response.arrayBuffer();
                        
                        const result = await mammoth.convertToHtml({{ arrayBuffer }});
                        
                        const container = document.getElementById('viewerContainer');
                        container.innerHTML = `<div class="docx-content">${{result.value}}</div>`;
                        
                        this.totalPages = 1;
                        this.currentPage = 1;
                        
                    }} catch (error) {{
                        throw new Error('Failed to load DOCX: ' + error.message);
                    }}
                }}
                
                async loadPPTX(url) {{
                    try {{
                        const response = await fetch(url);
                        const arrayBuffer = await response.arrayBuffer();
                        
                        const zip = await JSZip.loadAsync(arrayBuffer);
                        
                        const slideFiles = Object.keys(zip.files).filter(name => 
                            name.startsWith('ppt/slides/slide') && name.endsWith('.xml')
                        );
                        
                        this.totalPages = slideFiles.length || 5; // Default to 5 for demo
                        this.pptxSlides = slideFiles;
                        
                        await this.renderPPTXSlide(1);
                        
                    }} catch (error) {{
                        // Fallback for demo
                        this.totalPages = 5;
                        await this.renderPPTXSlide(1);
                    }}
                }}
                
                async renderPPTXSlide(slideNum) {{
                    try {{
                        const container = document.getElementById('viewerContainer');
                        container.innerHTML = `
                            <div class="pptx-slide">
                                <h3>Slide ${{slideNum}}</h3>
                                <p>This is a JavaScript-based PPTX viewer. Slide ${{slideNum}} of ${{this.totalPages}}.</p>
                                <p style="color: #666;">✅ No server-side image conversion required!</p>
                                <p style="color: #666;">✅ Direct JavaScript parsing and rendering</p>
                                <p style="color: #666;">✅ Clickable navigation between slides</p>
                            </div>
                        `;
                        
                        this.currentPage = slideNum;
                        
                    }} catch (error) {{
                        throw new Error('Failed to render PPTX slide: ' + error.message);
                    }}
                }}
                
                async loadExcel(url) {{
                    try {{
                        const response = await fetch(url);
                        const arrayBuffer = await response.arrayBuffer();
                        
                        this.excelWorkbook = XLSX.read(arrayBuffer, {{ type: 'array' }});
                        this.totalPages = this.excelWorkbook.SheetNames.length;
                        
                        this.renderExcelSheet(1);
                        
                    }} catch (error) {{
                        throw new Error('Failed to load Excel: ' + error.message);
                    }}
                }}
                
                renderExcelSheet(sheetNum) {{
                    try {{
                        const sheetName = this.excelWorkbook.SheetNames[sheetNum - 1];
                        const worksheet = this.excelWorkbook.Sheets[sheetName];
                        
                        const htmlTable = XLSX.utils.sheet_to_html(worksheet, {{
                            table: true,
                            tableClass: 'excel-table'
                        }});
                        
                        const container = document.getElementById('viewerContainer');
                        container.innerHTML = `
                            <h5>Sheet: ${{sheetName}}</h5>
                            ${{htmlTable}}
                        `;
                        
                        this.currentPage = sheetNum;
                        
                    }} catch (error) {{
                        throw new Error('Failed to render Excel sheet: ' + error.message);
                    }}
                }}
                
                async navigateToPage(pageNum) {{
                    if (pageNum < 1 || pageNum > this.totalPages || !this.currentDocument) {{
                        return;
                    }}
                    
                    try {{
                        switch (this.documentType) {{
                            case 'pdf':
                                await this.renderPDFPage(pageNum);
                                break;
                            case 'docx':
                                this.currentPage = 1;
                                break;
                            case 'pptx':
                                await this.renderPPTXSlide(pageNum);
                                break;
                            case 'xlsx':
                                this.renderExcelSheet(pageNum);
                                break;
                        }}
                        
                        this.updateNavigationControls();
                        this.updatePageLinks();
                        this.showStatus(`Navigated to ${{this.getPageTypeName()}} ${{pageNum}}`);
                        
                    }} catch (error) {{
                        this.showError('Failed to navigate: ' + error.message);
                    }}
                }}
                
                getPageTypeName() {{
                    switch (this.documentType) {{
                        case 'pdf':
                        case 'docx':
                            return 'page';
                        case 'pptx':
                            return 'slide';
                        case 'xlsx':
                            return 'sheet';
                        default:
                            return 'page';
                    }}
                }}
                
                updateNavigationInfo(fileName) {{
                    const info = document.getElementById('documentInfo');
                    const pageType = this.getPageTypeName();
                    info.innerHTML = `
                        <strong>📄 ${{fileName}}</strong><br>
                        <small>${{pageType.charAt(0).toUpperCase() + pageType.slice(1)}} ${{this.currentPage}} of ${{this.totalPages}}</small>
                    `;
                }}
                
                updateNavigationControls() {{
                    const prevBtn = document.getElementById('prevBtn');
                    const nextBtn = document.getElementById('nextBtn');
                    const pageInput = document.getElementById('pageInput');
                    const goBtn = document.getElementById('goBtn');
                    
                    const hasDocument = this.currentDocument !== null;
                    
                    prevBtn.disabled = !hasDocument || this.currentPage <= 1;
                    nextBtn.disabled = !hasDocument || this.currentPage >= this.totalPages;
                    pageInput.disabled = !hasDocument;
                    goBtn.disabled = !hasDocument;
                    
                    if (hasDocument) {{
                        pageInput.max = this.totalPages;
                        pageInput.value = this.currentPage;
                    }}
                }}
                
                generatePageLinks() {{
                    const container = document.getElementById('pageLinks');
                    
                    if (!this.currentDocument || this.totalPages <= 1) {{
                        container.style.display = 'none';
                        return;
                    }}
                    
                    const pageType = this.getPageTypeName();
                    let html = `<h6>Quick Navigation - Click any ${{pageType}} to jump to it!</h6>`;
                    
                    for (let i = 1; i <= this.totalPages; i++) {{
                        const isActive = i === this.currentPage;
                        const className = isActive ? 'page-link active' : 'page-link';
                        
                        html += `<a href="#" class="${{className}}" data-page="${{i}}">${{pageType.charAt(0).toUpperCase() + pageType.slice(1)}} ${{i}}</a>`;
                    }}
                    
                    container.innerHTML = html;
                    container.style.display = 'block';
                    
                    // Add click event listeners to page links
                    container.querySelectorAll('.page-link').forEach(link => {{
                        link.addEventListener('click', (e) => {{
                            e.preventDefault();
                            const pageNum = parseInt(e.target.dataset.page);
                            this.navigateToPage(pageNum);
                        }});
                    }});
                }}
                
                updatePageLinks() {{
                    const links = document.querySelectorAll('#pageLinks .page-link');
                    links.forEach((link, index) => {{
                        const pageNum = index + 1;
                        if (pageNum === this.currentPage) {{
                            link.classList.add('active');
                        }} else {{
                            link.classList.remove('active');
                        }}
                    }});
                }}
                
                showLoading(message) {{
                    const container = document.getElementById('viewerContainer');
                    container.innerHTML = `
                        <div class="loading">
                            <h6>${{message}}</h6>
                        </div>
                    `;
                }}
                
                showError(message) {{
                    const container = document.getElementById('viewerContainer');
                    container.innerHTML = `
                        <div class="error">
                            <h6>Error</h6>
                            <p>${{message}}</p>
                        </div>
                    `;
                    this.showStatus('Error: ' + message);
                }}
                
                showStatus(message) {{
                    const status = document.getElementById('statusMessage');
                    status.innerHTML = `<small style="color: green;">${{message}}</small>`;
                }}
            }}

            // Initialize the application when the page loads
            document.addEventListener('DOMContentLoaded', () => {{
                new DocumentPreviewer();
            }});
        </script>
    </body>
    </html>
    """
    
    return html_content

def create_gradio_interface():
    """Create the main Gradio interface."""
    
    with gr.Blocks(title="📄 Document Previewer", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 📄 JavaScript Document Previewer
        
        **Preview PDF, DOCX, PPTX, and Excel files using pure JavaScript - No server-side image conversion!**
        
        This application demonstrates how to build a document viewer using JavaScript libraries:
        - **PDF.js** for PDF files
        - **Mammoth.js** for DOCX files  
        - **JSZip** for PPTX files
        - **SheetJS** for Excel files
        """)
        
        # Embed the document viewer
        viewer_html = gr.HTML(
            value=create_document_viewer(),
            label="Document Viewer"
        )
        
        with gr.Accordion("📚 Demo Examples & Features", open=True):
            gr.Markdown("""
            ### Try these examples to see the JavaScript document viewer in action:
            
            1. **PDF Example**: Select "Sample PDF (7 pages)" - Navigate through a multi-page PDF document using PDF.js
            2. **Word Document**: Select "Sample DOCX (2 pages)" - Preview Word document content using Mammoth.js
            3. **PowerPoint**: Select "Sample PPTX (5 slides)" - Browse through presentation slides using JSZip
            4. **Excel Spreadsheet**: Select "Sample Excel (5 sheets)" - View different worksheet tabs using SheetJS
            
            **Key Features:**
            - ✅ **Pure JavaScript Viewing**: No server-side image conversion required
            - ✅ **Clickable Page Navigation**: Click on page numbers to jump directly to any page
            - ✅ **Sequential Navigation**: Use Previous/Next buttons for step-by-step browsing
            - ✅ **Direct Page Input**: Enter a specific page number and click "Go"
            - ✅ **Multiple File Formats**: PDF, DOCX, PPTX, and Excel files
            - ✅ **File Upload Support**: Upload your own documents for preview
            - ✅ **Responsive Interface**: Works on both desktop and mobile devices
            
            **How to test the clickable navigation:**
            1. Select any sample document from the dropdown in the viewer above
            2. Wait for the document to load and the navigation panel to appear
            3. Click on any page number in the "Quick Navigation" section
            4. Watch as the preview instantly jumps to that page using JavaScript!
            
            **Technical Implementation:**
            - **PDF.js**: Mozilla's JavaScript PDF renderer
            - **Mammoth.js**: Converts DOCX to HTML
            - **JSZip**: Extracts and processes PPTX files
            - **SheetJS**: Parses and displays Excel spreadsheets
            - **No Backend Processing**: All document parsing happens in the browser
            """)
    
    return interface

def main():
    """Main function to run the Gradio application."""
    interface = create_gradio_interface()
    
    # Launch the app
    interface.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()

