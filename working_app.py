import gradio as gr
import os
from document_previewer import DocumentPreviewer

class DocumentPreviewApp:
    def __init__(self):
        self.previewer = DocumentPreviewer()
        self.current_file = None
        self.current_page = 1
        self.total_pages = 0
        
        # Sample documents for demo
        self.sample_docs = {
            "Sample PDF (7 pages)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_pdf.pdf",
            "Sample DOCX (2 pages)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_docx.docx", 
            "Sample PPTX (5 slides)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_pptx.pptx",
            "Sample Excel (5 sheets)": "/home/ubuntu/gradio_document_previewer/sample_docs/sample_excel.xlsx"
        }
    
    def load_document(self, sample_doc):
        """Load a document and return the first page preview with navigation."""
        try:
            if sample_doc == "Select a sample document...":
                return None, "Please select a document", "", gr.update(visible=False)
            
            file_path = self.sample_docs[sample_doc]
            self.current_file = file_path
            
            if not os.path.exists(self.current_file):
                return None, f"File not found: {self.current_file}", "", gr.update(visible=False)
            
            if not self.previewer.is_supported(self.current_file):
                return None, "Unsupported file format.", "", gr.update(visible=False)
            
            # Get total pages and load first page
            self.total_pages = self.previewer.get_page_count(self.current_file)
            self.current_page = 1
            
            if self.total_pages == 0:
                return None, "Could not read the document.", "", gr.update(visible=False)
            
            # Generate preview for first page
            preview_image = self.previewer.preview_page(self.current_file, self.current_page)
            
            # Generate navigation info
            nav_info = self.generate_navigation_info()
            
            # Generate page links
            page_links = self.generate_page_links()
            
            return preview_image, f"Document loaded successfully! Total pages: {self.total_pages}", nav_info, gr.update(visible=True, value=page_links)
            
        except Exception as e:
            return None, f"Error loading document: {str(e)}", "", gr.update(visible=False)
    
    def navigate_to_page(self, page_number):
        """Navigate to a specific page."""
        try:
            if not self.current_file:
                return None, "No document loaded.", ""
            
            if page_number is None or page_number < 1 or page_number > self.total_pages:
                return None, f"Invalid page number. Please enter a number between 1 and {self.total_pages}.", ""
            
            self.current_page = int(page_number)
            preview_image = self.previewer.preview_page(self.current_file, self.current_page)
            nav_info = self.generate_navigation_info()
            
            return preview_image, f"Navigated to page {self.current_page}", nav_info
            
        except Exception as e:
            return None, f"Error navigating to page: {str(e)}", ""
    
    def navigate_prev(self):
        """Navigate to previous page."""
        if self.current_page > 1:
            return self.navigate_to_page(self.current_page - 1)
        return None, "Already at the first page.", self.generate_navigation_info()
    
    def navigate_next(self):
        """Navigate to next page."""
        if self.current_page < self.total_pages:
            return self.navigate_to_page(self.current_page + 1)
        return None, "Already at the last page.", self.generate_navigation_info()
    
    def generate_navigation_info(self):
        """Generate navigation information text."""
        if not self.current_file:
            return ""
        
        file_name = os.path.basename(self.current_file)
        file_ext = os.path.splitext(file_name)[1].upper()
        
        if file_ext == '.PDF':
            page_type = "Page"
        elif file_ext == '.PPTX':
            page_type = "Slide"
        elif file_ext == '.XLSX':
            page_type = "Sheet"
        else:
            page_type = "Page"
        
        return f"📄 {file_name} | {page_type} {self.current_page} of {self.total_pages}"
    
    def generate_page_links(self):
        """Generate HTML with clickable page links."""
        if not self.current_file or self.total_pages == 0:
            return ""
        
        file_ext = os.path.splitext(self.current_file)[1].upper()
        
        if file_ext == '.PDF':
            page_type = "Page"
        elif file_ext == '.PPTX':
            page_type = "Slide"
        elif file_ext == '.XLSX':
            page_type = "Sheet"
        else:
            page_type = "Page"
        
        html = f"""
        <div style="padding: 15px; background-color: #f8f9fa; border-radius: 8px; margin: 10px 0;">
            <h3 style="margin-top: 0; color: #333;">Quick Navigation - Click any {page_type.lower()} to jump to it!</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;">
        """
        
        for i in range(1, self.total_pages + 1):
            if i == self.current_page:
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
                ">{page_type} {i}</span>
                """
            else:
                # Other pages - clickable links
                html += f"""
                <button onclick="
                    document.querySelector('input[placeholder=\\"Enter page number\\"]').value = '{i}';
                    document.querySelector('input[placeholder=\\"Enter page number\\"]').dispatchEvent(new Event('input', {{bubbles: true}}));
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
                   onmouseout="this.style.backgroundColor='#e9ecef'">{page_type} {i}</button>
                """
        
        html += """
            </div>
            <p style="margin-top: 15px; margin-bottom: 0; color: #666; font-size: 0.9em;">
                💡 <strong>Tip:</strong> You can also use the Previous/Next buttons or enter a page number manually.
            </p>
        </div>
        """
        
        return html
    
    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title="Document Previewer", theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            # 📄 Document Previewer
            
            Select a sample document to preview its contents. Supports **PDF**, **DOCX**, **PPTX**, and **Excel** files.
            Click on page numbers to navigate directly to specific pages!
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📁 Load Document")
                    
                    # Sample document selector
                    sample_dropdown = gr.Dropdown(
                        choices=["Select a sample document..."] + list(self.sample_docs.keys()),
                        value="Select a sample document...",
                        label="Try a Sample Document"
                    )
                    
                    # Navigation controls
                    gr.Markdown("### 🧭 Navigation")
                    
                    nav_info = gr.Textbox(
                        label="Current Document",
                        interactive=False,
                        value="No document loaded"
                    )
                    
                    with gr.Row():
                        prev_btn = gr.Button("⬅️ Previous", variant="secondary")
                        next_btn = gr.Button("Next ➡️", variant="secondary")
                    
                    with gr.Row():
                        page_input = gr.Number(
                            label="Go to Page",
                            placeholder="Enter page number",
                            minimum=1,
                            precision=0
                        )
                        go_btn = gr.Button("Go to Page", variant="primary")
                
                with gr.Column(scale=2):
                    gr.Markdown("### 👁️ Document Preview")
                    
                    # Preview image
                    preview_image = gr.Image(
                        label="Document Preview",
                        height=600,
                        show_label=False
                    )
                    
                    # Status message
                    status_msg = gr.Textbox(
                        label="Status",
                        value="Select a sample document to get started",
                        interactive=False
                    )
            
            # Page navigation links (initially hidden)
            page_links = gr.HTML(visible=False)
            
            # Event handlers
            sample_dropdown.change(
                fn=self.load_document,
                inputs=[sample_dropdown],
                outputs=[preview_image, status_msg, nav_info, page_links]
            )
            
            prev_btn.click(
                fn=self.navigate_prev,
                outputs=[preview_image, status_msg, nav_info]
            )
            
            next_btn.click(
                fn=self.navigate_next,
                outputs=[preview_image, status_msg, nav_info]
            )
            
            go_btn.click(
                fn=self.navigate_to_page,
                inputs=[page_input],
                outputs=[preview_image, status_msg, nav_info]
            )
            
            # Add demo section
            with gr.Accordion("📚 Demo Examples & Features", open=True):
                gr.Markdown("""
                ### Try these examples to see the document previewer in action:
                
                1. **PDF Example**: Select "Sample PDF (7 pages)" - Navigate through a multi-page PDF document
                2. **Word Document**: Select "Sample DOCX (2 pages)" - Preview Word document pages
                3. **PowerPoint**: Select "Sample PPTX (5 slides)" - Browse through presentation slides  
                4. **Excel Spreadsheet**: Select "Sample Excel (5 sheets)" - View different worksheet tabs
                
                **Key Features:**
                - ✅ **Clickable Page Navigation**: Click on page numbers to jump directly to any page
                - ✅ **Sequential Navigation**: Use Previous/Next buttons for step-by-step browsing
                - ✅ **Direct Page Input**: Enter a specific page number and click "Go to Page"
                - ✅ **Multiple File Formats**: Supports PDF, DOCX, PPTX, and Excel files
                - ✅ **Visual Preview**: See actual document content rendered as images
                - ✅ **Responsive Interface**: Works on both desktop and mobile devices
                
                **How to test the clickable navigation:**
                1. Select any sample document from the dropdown
                2. Wait for the document to load and the navigation panel to appear
                3. Click on any page number in the "Quick Navigation" section
                4. Watch as the preview instantly jumps to that page!
                """)
        
        return interface

def main():
    app = DocumentPreviewApp()
    interface = app.create_interface()
    
    # Launch the app
    interface.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()

