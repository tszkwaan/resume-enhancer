# CV Enhancer

A modern web application for uploading and extracting text from CV files (PDF, DOC, DOCX) using Next.js, Tailwind CSS, and Python with PyPDF2.

## Project Structure

```
resume-enhancer/
├── web-app/                 # Main application directory
│   ├── src/                 # Next.js source code
│   ├── public/              # Static assets
│   ├── scripts/             # Python text extraction scripts
│   ├── package.json         # Node.js dependencies
│   ├── requirements.txt     # Python dependencies
│   ├── setup.sh            # Setup script
│   └── README.md           # Detailed documentation
├── .git/                   # Git repository
└── .venv/                  # Python virtual environment
```

## Quick Start

1. **Navigate to the web-app directory:**
   ```bash
   cd web-app
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Tech Stack

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React Dropzone** for drag & drop functionality

### Backend
- **Python 3** with PyPDF2 for PDF text extraction
- **python-docx** for Word document processing
- **Next.js API Routes** for server-side integration

## Development

All development work should be done in the `web-app` directory. The main application files are located there, and the setup script will handle installing all dependencies.

For detailed documentation, see [web-app/README.md](web-app/README.md).
