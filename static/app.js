// Document Previewer JavaScript Application

class DocumentPreviewer {
    constructor() {
        this.currentDocument = null;
        this.currentPage = 1;
        this.totalPages = 0;
        this.documentType = null;
        this.pdfDoc = null;
        this.excelWorkbook = null;
        this.pptxSlides = [];
        
        this.initializeEventListeners();
        this.setupPDFJS();
    }
    
    setupPDFJS() {
        // Set PDF.js worker
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    }
    
    initializeEventListeners() {
        // Document selection
        document.getElementById('documentSelect').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadSampleDocument(e.target.value);
            }
        });
        
        // File upload
        document.getElementById('fileUpload').addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.loadUploadedDocument(e.target.files[0]);
            }
        });
        
        // Navigation buttons
        document.getElementById('prevBtn').addEventListener('click', () => {
            this.navigateToPage(this.currentPage - 1);
        });
        
        document.getElementById('nextBtn').addEventListener('click', () => {
            this.navigateToPage(this.currentPage + 1);
        });
        
        document.getElementById('goBtn').addEventListener('click', () => {
            const pageNum = parseInt(document.getElementById('pageInput').value);
            if (pageNum) {
                this.navigateToPage(pageNum);
            }
        });
        
        // Enter key in page input
        document.getElementById('pageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const pageNum = parseInt(e.target.value);
                if (pageNum) {
                    this.navigateToPage(pageNum);
                }
            }
        });
    }
    
    async loadSampleDocument(docName) {
        try {
            this.showLoading('Loading document...');
            
            // Get document info from server
            const response = await fetch('/get_doc_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ doc_name: docName })
            });
            
            const docInfo = await response.json();
            
            if (docInfo.error) {
                this.showError(docInfo.error);
                return;
            }
            
            // Load the document
            await this.loadDocumentFromURL(docInfo.file_path, docName);
            
        } catch (error) {
            this.showError('Failed to load document: ' + error.message);
        }
    }
    
    async loadUploadedDocument(file) {
        try {
            this.showLoading('Loading uploaded document...');
            
            const fileName = file.name;
            const fileExtension = fileName.split('.').pop().toLowerCase();
            
            // Create object URL for the file
            const fileURL = URL.createObjectURL(file);
            
            await this.loadDocumentFromURL(fileURL, fileName);
            
        } catch (error) {
            this.showError('Failed to load uploaded document: ' + error.message);
        }
    }
    
    async loadDocumentFromURL(url, fileName) {
        const fileExtension = fileName.split('.').pop().toLowerCase();
        
        this.currentDocument = url;
        this.documentType = fileExtension;
        this.currentPage = 1;
        
        switch (fileExtension) {
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
        }
        
        this.updateNavigationInfo(fileName);
        this.updateNavigationControls();
        this.generatePageLinks();
        this.showStatus('Document loaded successfully!');
    }
    
    async loadPDF(url) {
        try {
            this.pdfDoc = await pdfjsLib.getDocument(url).promise;
            this.totalPages = this.pdfDoc.numPages;
            await this.renderPDFPage(1);
        } catch (error) {
            throw new Error('Failed to load PDF: ' + error.message);
        }
    }
    
    async renderPDFPage(pageNum) {
        try {
            const page = await this.pdfDoc.getPage(pageNum);
            const scale = 1.5;
            const viewport = page.getViewport({ scale });
            
            // Create canvas
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            canvas.className = 'pdf-canvas';
            
            // Render page
            await page.render({
                canvasContext: context,
                viewport: viewport
            }).promise;
            
            // Update viewer
            const container = document.getElementById('viewerContainer');
            container.innerHTML = '';
            container.appendChild(canvas);
            
            this.currentPage = pageNum;
            
        } catch (error) {
            throw new Error('Failed to render PDF page: ' + error.message);
        }
    }
    
    async loadDOCX(url) {
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            
            const result = await mammoth.convertToHtml({ arrayBuffer });
            
            const container = document.getElementById('viewerContainer');
            container.innerHTML = `<div class="docx-content">${result.value}</div>`;
            
            // For DOCX, we'll treat it as a single "page" for simplicity
            // In a real implementation, you might want to implement pagination
            this.totalPages = 1;
            this.currentPage = 1;
            
        } catch (error) {
            throw new Error('Failed to load DOCX: ' + error.message);
        }
    }
    
    async loadPPTX(url) {
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            
            // For PPTX, we'll create a simple slide viewer
            // This is a basic implementation - a full PPTX viewer would be more complex
            const zip = await JSZip.loadAsync(arrayBuffer);
            
            // Extract slide information (simplified)
            const slideFiles = Object.keys(zip.files).filter(name => 
                name.startsWith('ppt/slides/slide') && name.endsWith('.xml')
            );
            
            this.totalPages = slideFiles.length;
            this.pptxSlides = slideFiles;
            
            if (this.totalPages > 0) {
                await this.renderPPTXSlide(1);
            } else {
                throw new Error('No slides found in PPTX file');
            }
            
        } catch (error) {
            throw new Error('Failed to load PPTX: ' + error.message);
        }
    }
    
    async renderPPTXSlide(slideNum) {
        try {
            // This is a simplified PPTX renderer
            // In a real implementation, you would parse the XML and render the slide content
            const container = document.getElementById('viewerContainer');
            container.innerHTML = `
                <div class="pptx-slide">
                    <h3>Slide ${slideNum}</h3>
                    <p>This is a simplified PPTX viewer. Slide ${slideNum} of ${this.totalPages}.</p>
                    <p class="text-muted">A full PPTX implementation would parse the slide XML and render the actual content, including text, images, shapes, and formatting.</p>
                </div>
            `;
            
            this.currentPage = slideNum;
            
        } catch (error) {
            throw new Error('Failed to render PPTX slide: ' + error.message);
        }
    }
    
    async loadExcel(url) {
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            
            this.excelWorkbook = XLSX.read(arrayBuffer, { type: 'array' });
            this.totalPages = this.excelWorkbook.SheetNames.length;
            
            if (this.totalPages > 0) {
                this.renderExcelSheet(1);
            } else {
                throw new Error('No sheets found in Excel file');
            }
            
        } catch (error) {
            throw new Error('Failed to load Excel: ' + error.message);
        }
    }
    
    renderExcelSheet(sheetNum) {
        try {
            const sheetName = this.excelWorkbook.SheetNames[sheetNum - 1];
            const worksheet = this.excelWorkbook.Sheets[sheetName];
            
            // Convert to HTML table
            const htmlTable = XLSX.utils.sheet_to_html(worksheet, {
                table: true,
                tableClass: 'excel-table table table-striped'
            });
            
            const container = document.getElementById('viewerContainer');
            container.innerHTML = `
                <h5>Sheet: ${sheetName}</h5>
                ${htmlTable}
            `;
            
            this.currentPage = sheetNum;
            
        } catch (error) {
            throw new Error('Failed to render Excel sheet: ' + error.message);
        }
    }
    
    async navigateToPage(pageNum) {
        if (pageNum < 1 || pageNum > this.totalPages || !this.currentDocument) {
            return;
        }
        
        try {
            switch (this.documentType) {
                case 'pdf':
                    await this.renderPDFPage(pageNum);
                    break;
                case 'docx':
                    // DOCX is single page in our implementation
                    this.currentPage = 1;
                    break;
                case 'pptx':
                    await this.renderPPTXSlide(pageNum);
                    break;
                case 'xlsx':
                    this.renderExcelSheet(pageNum);
                    break;
            }
            
            this.updateNavigationControls();
            this.updatePageLinks();
            this.showStatus(`Navigated to ${this.getPageTypeName()} ${pageNum}`);
            
        } catch (error) {
            this.showError('Failed to navigate: ' + error.message);
        }
    }
    
    getPageTypeName() {
        switch (this.documentType) {
            case 'pdf':
            case 'docx':
                return 'page';
            case 'pptx':
                return 'slide';
            case 'xlsx':
                return 'sheet';
            default:
                return 'page';
        }
    }
    
    updateNavigationInfo(fileName) {
        const info = document.getElementById('documentInfo');
        const pageType = this.getPageTypeName();
        info.innerHTML = `
            <strong>📄 ${fileName}</strong><br>
            <small>${pageType.charAt(0).toUpperCase() + pageType.slice(1)} ${this.currentPage} of ${this.totalPages}</small>
        `;
    }
    
    updateNavigationControls() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const pageInput = document.getElementById('pageInput');
        const goBtn = document.getElementById('goBtn');
        
        const hasDocument = this.currentDocument !== null;
        
        prevBtn.disabled = !hasDocument || this.currentPage <= 1;
        nextBtn.disabled = !hasDocument || this.currentPage >= this.totalPages;
        pageInput.disabled = !hasDocument;
        goBtn.disabled = !hasDocument;
        
        if (hasDocument) {
            pageInput.max = this.totalPages;
            pageInput.value = this.currentPage;
        }
    }
    
    generatePageLinks() {
        const container = document.getElementById('pageLinks');
        
        if (!this.currentDocument || this.totalPages <= 1) {
            container.style.display = 'none';
            return;
        }
        
        const pageType = this.getPageTypeName();
        let html = `<h6>Quick Navigation - Click any ${pageType} to jump to it!</h6>`;
        
        for (let i = 1; i <= this.totalPages; i++) {
            const isActive = i === this.currentPage;
            const className = isActive ? 'page-link active' : 'page-link';
            
            html += `<a href="#" class="${className}" data-page="${i}">${pageType.charAt(0).toUpperCase() + pageType.slice(1)} ${i}</a>`;
        }
        
        container.innerHTML = html;
        container.style.display = 'block';
        
        // Add click event listeners to page links
        container.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageNum = parseInt(e.target.dataset.page);
                this.navigateToPage(pageNum);
            });
        });
    }
    
    updatePageLinks() {
        const links = document.querySelectorAll('#pageLinks .page-link');
        links.forEach((link, index) => {
            const pageNum = index + 1;
            if (pageNum === this.currentPage) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    
    showLoading(message) {
        const container = document.getElementById('viewerContainer');
        container.innerHTML = `
            <div class="loading">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h6 class="mt-3">${message}</h6>
            </div>
        `;
    }
    
    showError(message) {
        const container = document.getElementById('viewerContainer');
        container.innerHTML = `
            <div class="error">
                <h6>Error</h6>
                <p>${message}</p>
            </div>
        `;
        this.showStatus('Error: ' + message);
    }
    
    showStatus(message) {
        const status = document.getElementById('statusMessage');
        status.innerHTML = `<small class="text-success">${message}</small>`;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DocumentPreviewer();
});

