# 📄 JavaScript Document Previewer

A comprehensive document viewing application built with **Gradio** and **JavaScript** that allows users to preview PDF, DOCX, PPTX, and Excel files directly in the browser without any server-side image conversion.

## ✨ Key Features

### 🚀 **Pure JavaScript Viewing**
- **No Server Processing**: All document parsing and rendering happens client-side
- **Fast Loading**: No waiting for server-side image conversion
- **Scalable**: No server resources consumed for document processing
- **Secure**: Documents never leave the user's browser

### 🧭 **Advanced Navigation**
- **Clickable Page Links**: Jump directly to any page/slide/sheet by clicking
- **Sequential Navigation**: Previous/Next buttons for step-by-step browsing
- **Direct Page Input**: Enter specific page numbers and press Enter or click "Go"
- **Visual Feedback**: Active page highlighting and real-time status updates

### 📁 **Multi-Format Support**
- **PDF Files**: Rendered using PDF.js with full page navigation
- **Word Documents (DOCX)**: Converted to HTML using Mammoth.js
- **PowerPoint (PPTX)**: Slide-by-slide viewing using JSZip parsing
- **Excel Spreadsheets (XLSX)**: Sheet tabs displayed as separate pages using SheetJS

### 📱 **Responsive Design**
- **Desktop & Mobile**: Optimized for all screen sizes
- **Touch Support**: Works with touch navigation on mobile devices
- **Bootstrap UI**: Professional, modern interface design

## 🎮 **Demo Examples**

The application includes 4 comprehensive demo examples:

1. **📄 Demo PDF (7 pages)**: Multi-page PDF document with clickable page navigation
2. **📝 Demo DOCX (2 pages)**: Word document with formatted text and tables
3. **📊 Demo PPTX (5 slides)**: PowerPoint presentation with slide-by-slide navigation
4. **📈 Demo Excel (5 sheets)**: Excel workbook with multiple worksheet tabs

## 🛠️ **Technical Implementation**

### JavaScript Libraries
- **PDF.js v3.11.174**: Mozilla's JavaScript PDF renderer
- **Mammoth.js v1.6.0**: DOCX to HTML converter
- **JSZip v3.10.1**: ZIP file processing for PPTX files
- **SheetJS v0.18.5**: Excel file parser and renderer
- **Bootstrap v5.3.0**: Responsive UI framework

### Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gradio App    │    │  HTML/JavaScript │    │  Browser APIs   │
│   (Python)      │───▶│     Viewer       │───▶│  (Client-side)  │
│                 │    │                  │    │                 │
│ - File handling │    │ - Document       │    │ - PDF.js        │
│ - UI framework  │    │   parsing        │    │ - Mammoth.js    │
│ - Web server    │    │ - Navigation     │    │ - JSZip         │
└─────────────────┘    │ - Rendering      │    │ - SheetJS       │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### Prerequisites
- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation
1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install gradio
   ```

### Running the Application

#### Option 1: Standalone HTML Viewer
```bash
# Open in browser directly
open demo_viewer.html
```

#### Option 2: Gradio Integration
```bash
# Run the Gradio app
python final_gradio_app.py
```

#### Option 3: Full Gradio App with Flask Backend
```bash
# Install additional dependencies
pip install flask

# Run the full application
python gradio_app.py
```

### Accessing the Application
- **Gradio App**: http://localhost:7864
- **Standalone**: Open `demo_viewer.html` in your browser

## 📖 **How to Use**

### 1. **Loading Documents**
- **Demo Examples**: Click any colored demo button (PDF, DOCX, PPTX, Excel)
- **File Upload**: Use the file input to upload your own documents
- **Supported Formats**: `.pdf`, `.docx`, `.pptx`, `.xlsx`

### 2. **Navigation Methods**
- **Clickable Links**: Click page numbers in the "Quick Navigation" section
- **Previous/Next**: Use arrow buttons for sequential navigation
- **Direct Input**: Type page number and press Enter or click "Go"
- **Keyboard**: Press Enter after typing in the page input field

### 3. **Testing the Demo**
1. Click "📄 Demo PDF (7 pages)"
2. Wait for the document to load
3. Click on "Page 5" in the navigation panel
4. Watch the document instantly jump to page 5!
5. Try other formats to see different navigation styles

## 🎯 **Use Cases**

### **Document Management Systems**
- Preview documents without downloading
- Quick navigation through large documents
- Client-side processing for security

### **Educational Platforms**
- Display course materials and presentations
- Navigate through lecture slides
- View spreadsheet data and reports

### **Business Applications**
- Review contracts and proposals
- Browse through presentation decks
- Analyze Excel reports and data

### **Content Management**
- Preview uploaded documents
- Quick document review workflows
- Multi-format document support

## 🔧 **Customization**

### **Adding New File Formats**
1. Find appropriate JavaScript library
2. Add parsing logic to `DocumentPreviewer` class
3. Implement navigation for the new format
4. Update UI to support the format

### **Styling and Themes**
- Modify CSS in the HTML files
- Update Bootstrap classes
- Customize color schemes and layouts

### **Integration with Other Frameworks**
- Extract JavaScript viewer for use in React/Vue/Angular
- Embed in existing web applications
- Customize for specific use cases

## 📁 **Project Structure**

```
gradio_document_previewer/
├── README.md                 # This documentation
├── requirements.txt          # Python dependencies
├── final_gradio_app.py      # Main Gradio application
├── gradio_app.py            # Full app with Flask backend
├── demo_viewer.html         # Standalone HTML viewer
├── standalone_viewer.html   # Alternative standalone version
├── sample_docs/             # Sample documents for testing
│   ├── create_pdf.py        # Script to generate sample PDF
│   ├── create_docx.py       # Script to generate sample DOCX
│   ├── create_pptx.py       # Script to generate sample PPTX
│   └── create_excel.py      # Script to generate sample Excel
├── static/                  # Static assets (if using Flask)
│   └── app.js              # JavaScript application logic
└── templates/               # HTML templates (if using Flask)
    └── index.html          # Main template
```

## 🤝 **Contributing**

### **Areas for Enhancement**
- **Additional File Formats**: Add support for more document types
- **Advanced PDF Features**: Zoom, search, annotations
- **PPTX Improvements**: Better slide content parsing and rendering
- **Performance Optimization**: Lazy loading, caching, compression
- **Accessibility**: Screen reader support, keyboard navigation

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is open source and available under the MIT License.

## 🙏 **Acknowledgments**

- **PDF.js Team**: For the excellent JavaScript PDF renderer
- **Mammoth.js**: For DOCX to HTML conversion
- **JSZip**: For ZIP file processing capabilities
- **SheetJS**: For comprehensive Excel file support
- **Bootstrap**: For responsive UI components
- **Gradio Team**: For the amazing Python web framework

## 📞 **Support**

For questions, issues, or feature requests:
1. Check the documentation above
2. Review the demo examples
3. Test with the provided sample files
4. Create an issue with detailed information

---

**Built with ❤️ using JavaScript, Python, and Gradio**

