import gradio as gr
import os

def create_document_viewer_interface():
    """Create the main Gradio interface with embedded JavaScript document viewer."""
    
    # Read the demo viewer HTML content
    demo_viewer_path = os.path.join(os.path.dirname(__file__), 'demo_viewer.html')
    
    with open(demo_viewer_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create the Gradio interface
    with gr.Blocks(
        title="📄 JavaScript Document Previewer",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: none !important;
        }
        .main-content {
            padding: 0 !important;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 📄 JavaScript Document Previewer - Gradio Integration
        
        **Preview PDF, DOCX, PPTX, and Excel files using pure JavaScript - No server-side image conversion!**
        
        This Gradio application demonstrates how to integrate JavaScript-based document viewers that can:
        - Load and display multiple document formats directly in the browser
        - Provide clickable navigation between pages/slides/sheets
        - Support file uploads and demo examples
        - Work entirely client-side without server processing
        """)
        
        # Embed the JavaScript document viewer
        viewer_component = gr.HTML(
            value=html_content,
            label="JavaScript Document Viewer",
            elem_classes=["main-content"]
        )
        
        with gr.Accordion("📚 How to Use This Application", open=False):
            gr.Markdown("""
            ### Getting Started:
            
            1. **Try Demo Examples**: Click any of the colored demo buttons (PDF, DOCX, PPTX, Excel) to load sample documents
            2. **Upload Your Own Files**: Use the file upload input to load your own documents
            3. **Navigate Documents**: Use the navigation controls and clickable page/slide/sheet links
            
            ### Navigation Methods:
            
            - **Clickable Links**: Click on any page number in the "Quick Navigation" section
            - **Previous/Next Buttons**: Step through documents sequentially  
            - **Direct Input**: Enter a specific page number and click "Go"
            - **Keyboard**: Press Enter after typing a page number
            
            ### Supported Formats:
            
            - **PDF**: Rendered using PDF.js - supports multi-page navigation
            - **DOCX**: Converted to HTML using Mammoth.js - displays formatted text
            - **PPTX**: Parsed using JSZip - shows slide-by-slide content
            - **Excel**: Processed using SheetJS - displays sheet tabs as separate pages
            
            ### Technical Features:
            
            ✅ **Pure JavaScript**: No server-side image conversion required  
            ✅ **Client-Side Processing**: All document parsing happens in the browser  
            ✅ **Responsive Design**: Works on desktop and mobile devices  
            ✅ **Real-Time Navigation**: Instant page switching with visual feedback  
            ✅ **File Upload Support**: Load your own documents for testing  
            ✅ **Multiple Formats**: Comprehensive support for common office documents  
            
            ### Demo Instructions:
            
            1. Click "📄 Demo PDF (7 pages)" to load a sample PDF
            2. Wait for the document to load and navigation links to appear
            3. Click on any page number (e.g., "Page 5") in the navigation panel
            4. Watch the document instantly jump to that page!
            5. Try other demo formats to see different navigation styles
            """)
        
        with gr.Accordion("🔧 Technical Implementation", open=False):
            gr.Markdown("""
            ### JavaScript Libraries Used:
            
            - **PDF.js (v3.11.174)**: Mozilla's JavaScript PDF renderer
            - **Mammoth.js (v1.6.0)**: Converts DOCX files to HTML
            - **JSZip (v3.10.1)**: Extracts and processes PPTX files  
            - **SheetJS (v0.18.5)**: Parses and displays Excel spreadsheets
            - **Bootstrap (v5.3.0)**: Responsive UI framework
            
            ### Architecture:
            
            1. **Gradio Frontend**: Provides the Python web interface and file handling
            2. **HTML/JavaScript Viewer**: Embedded component that handles document rendering
            3. **Client-Side Processing**: All document parsing and navigation happens in the browser
            4. **No Server Dependencies**: No need for external document conversion services
            
            ### Key Benefits:
            
            - **Fast Loading**: No server-side processing delays
            - **Scalable**: No server resources used for document conversion
            - **Secure**: Documents processed entirely client-side
            - **Offline Capable**: Works without internet after initial load
            - **Cross-Platform**: Runs in any modern web browser
            """)
    
    return interface

def main():
    """Main function to launch the Gradio application."""
    
    # Create and launch the interface
    interface = create_document_viewer_interface()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()

