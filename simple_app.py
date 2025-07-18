import gradio as gr
import os
from document_previewer import DocumentPreviewer

# Initialize the previewer
previewer = DocumentPreviewer()

# Sample documents
sample_docs = {
    "Sample PDF (5 pages)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_pdf.pdf",
    "Sample DOCX (5 pages)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_docx.docx", 
    "Sample PPTX (5 slides)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_pptx.pptx",
    "Sample Excel (5 sheets)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_excel.xlsx"
}

# Global state
current_file = None
current_page = 1
total_pages = 0

def load_sample_document(sample_name):
    global current_file, current_page, total_pages
    
    if sample_name == "Select a sample document...":
        return None, "Please select a document", "", gr.update(visible=False)
    
    file_path = sample_docs[sample_name]
    
    if not os.path.exists(file_path):
        return None, f"File not found: {file_path}", "", gr.update(visible=False)
    
    current_file = file_path
    total_pages = previewer.get_page_count(file_path)
    current_page = 1
    
    if total_pages == 0:
        return None, "Could not read the document.", "", gr.update(visible=False)
    
    # Generate preview for first page
    preview_image = previewer.preview_page(file_path, current_page)
    
    # Generate navigation info
    file_name = os.path.basename(file_path)
    nav_info = f"📄 {file_name} | Page {current_page} of {total_pages}"
    
    # Generate page links HTML
    page_links_html = generate_page_links()
    
    return preview_image, f"Document loaded! Total pages: {total_pages}", nav_info, gr.update(visible=True, value=page_links_html)

def navigate_to_page(page_number):
    global current_page
    
    if not current_file:
        return None, "No document loaded.", ""
    
    if page_number < 1 or page_number > total_pages:
        return None, f"Invalid page number. Please enter a number between 1 and {total_pages}.", ""
    
    current_page = int(page_number)
    preview_image = previewer.preview_page(current_file, current_page)
    
    file_name = os.path.basename(current_file)
    nav_info = f"📄 {file_name} | Page {current_page} of {total_pages}"
    
    return preview_image, f"Navigated to page {current_page}", nav_info

def generate_page_links():
    if not current_file or total_pages == 0:
        return ""
    
    html = f"""
    <div style="padding: 15px; background-color: #f8f9fa; border-radius: 8px; margin: 10px 0;">
        <h3 style="margin-top: 0; color: #333;">Quick Navigation</h3>
        <p style="margin-bottom: 15px; color: #666;">Click on any page number to jump directly to it:</p>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """
    
    for i in range(1, total_pages + 1):
        if i == current_page:
            # Current page - highlighted
            html += f"""
            <span style="
                padding: 8px 12px; 
                background-color: #007bff; 
                color: white; 
                border-radius: 4px; 
                font-weight: bold;
                min-width: 40px;
                text-align: center;
                display: inline-block;
            ">Page {i}</span>
            """
        else:
            # Other pages - clickable buttons
            html += f"""
            <button onclick="
                document.querySelector('input[placeholder=\\"Enter page number\\"]').value = '{i}';
                document.querySelector('input[placeholder=\\"Enter page number\\"]').dispatchEvent(new Event('input'));
                setTimeout(() => {{
                    const buttons = document.querySelectorAll('button');
                    for(let btn of buttons) {{
                        if(btn.textContent.trim() === 'Go to Page') {{
                            btn.click();
                            break;
                        }}
                    }}
                }}, 100);
            " style="
                padding: 8px 12px; 
                background-color: #e9ecef; 
                color: #495057; 
                border: 1px solid #ced4da; 
                border-radius: 4px; 
                cursor: pointer;
                min-width: 40px;
                text-align: center;
                transition: all 0.2s;
            " onmouseover="this.style.backgroundColor='#dee2e6'" 
               onmouseout="this.style.backgroundColor='#e9ecef'">Page {i}</button>
            """
    
    html += """
        </div>
    </div>
    """
    
    return html

# Create the Gradio interface
with gr.Blocks(title="Document Previewer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 Document Previewer")
    gr.Markdown("Select a sample document to preview its contents. Click on page numbers to navigate!")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Sample document selector
            sample_dropdown = gr.Dropdown(
                choices=["Select a sample document..."] + list(sample_docs.keys()),
                value="Select a sample document...",
                label="Try a Sample Document"
            )
            
            # Navigation info
            nav_info = gr.Textbox(
                label="Current Document",
                interactive=False,
                value="No document loaded"
            )
            
            # Page navigation
            with gr.Row():
                page_input = gr.Number(
                    label="Go to Page",
                    placeholder="Enter page number",
                    minimum=1,
                    precision=0
                )
                go_btn = gr.Button("Go to Page", variant="primary")
        
        with gr.Column(scale=2):
            # Preview image
            preview_image = gr.Image(
                label="Document Preview",
                height=600
            )
            
            # Status message
            status_msg = gr.Textbox(
                label="Status",
                value="Select a sample document to get started",
                interactive=False
            )
    
    # Page navigation links
    page_links = gr.HTML(visible=False)
    
    # Event handlers
    sample_dropdown.change(
        fn=load_sample_document,
        inputs=[sample_dropdown],
        outputs=[preview_image, status_msg, nav_info, page_links]
    )
    
    go_btn.click(
        fn=lambda x: navigate_to_page(x) if x else (None, "Please enter a page number", ""),
        inputs=[page_input],
        outputs=[preview_image, status_msg, nav_info]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)

