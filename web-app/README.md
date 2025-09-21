# CV Enhancer

A modern web application for uploading and extracting text from CV files (PDF, DOC, DOCX) using Next.js, Tailwind CSS, and Python with PyMuPDF.

## Features

- 🎨 **Modern UI**: Clean, professional design with drag & drop file upload
- 📄 **Multi-format Support**: Upload PDF, DOC, and DOCX files up to 5MB
- 🔄 **Real-time Processing**: Extract text from uploaded files instantly
- 🛡️ **File Validation**: Comprehensive file type and size validation
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React Dropzone** for drag & drop functionality

### Backend
- **Python 3** with PyMuPDF for PDF text extraction
- **python-docx** for Word document processing
- **Next.js API Routes** for server-side integration

## Prerequisites

- Node.js 18+ 
- Python 3.7+
- npm or yarn

## Quick Start

1. **Clone and setup the project:**
   ```bash
   git clone <your-repo-url>
   cd resume-enhancer
   ./setup.sh
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Manual Setup

If you prefer to set up manually:

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Make the Python script executable:**
   ```bash
   chmod +x scripts/extract_text.py
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

## Usage

1. **Upload a CV**: Drag and drop a PDF, DOC, or DOCX file onto the upload area, or click to select a file
2. **Wait for Processing**: The application will extract text from your file
3. **View Results**: The extracted text will be displayed below the upload area

## Supported File Types

- **PDF** (.pdf) - Extracted using PyMuPDF
- **Word Documents** (.docx) - Extracted using python-docx
- **Legacy Word Documents** (.doc) - Extracted using PyMuPDF

## File Size Limit

- Maximum file size: **5MB**

## Project Structure

```
resume-enhancer/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── extract-text/
│   │   │       └── route.ts          # API endpoint for text extraction
│   │   ├── globals.css               # Global styles
│   │   ├── layout.tsx                # Root layout
│   │   └── page.tsx                  # Main upload page
│   └── components/                   # Reusable components
├── scripts/
│   └── extract_text.py              # Python text extraction script
├── requirements.txt                 # Python dependencies
├── setup.sh                        # Setup script
└── README.md
```

## API Endpoints

### POST /api/extract-text

Extracts text from uploaded files.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF, DOC, or DOCX)

**Response:**
```json
{
  "text": "Extracted text content...",
  "filename": "resume.pdf",
  "size": 1024000
}
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File size limits
- Python script execution errors
- Network connectivity issues

## Development

### Running Tests
```bash
npm run test
```

### Building for Production
```bash
npm run build
npm start
```

### Linting
```bash
npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Python Dependencies Issues
If you encounter issues with Python dependencies:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### File Upload Issues
- Ensure your file is under 5MB
- Check that the file type is supported (PDF, DOC, DOCX)
- Verify Python 3 is installed and accessible

### Development Server Issues
- Make sure port 3000 is available
- Check that all dependencies are installed
- Verify the Python script is executable