'use client';

import { useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';

export default function Home() {
  const [isDragActive, setIsDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [extractedText, setExtractedText] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      handleFileUpload(file);
    }
  };

  const { getRootProps, getInputProps, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false
  });

  const handleFileUpload = async (file: File) => {
    setIsProcessing(true);
    setExtractedText('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/extract-text', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setExtractedText(data.text);
      } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="min-h-screen bg-amber-50 flex flex-col">

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 relative overflow-hidden">
        {/* Decorative Elements */}
        {/* Circle with dot - top right - moved 40px to the right (towards center) */}
        <div className="absolute top-8 right-16 md:top-12 md:right-120 md:visible invisible w-32 h-32 md:w-40 md:h-40 border-2 border-black rounded-full flex items-center justify-center z-10">
          <div className="w-8 h-8 md:w-12 md:h-12 bg-black rounded-full"></div>
        </div>
        
        {/* Rotated square - bottom left - moved 15px right and 20px up (towards center) */}
        <div className="absolute bottom-24 left-20 md:bottom-28 md:left-120 md:visible invisible w-28 h-28 md:w-36 md:h-36 border-2 border-black transform rotate-45 z-10"></div>
        
        {/* Additional geometric elements for better visual balance - much larger */}
        <div className="absolute top-1/3 left-2 w-16 h-16 border border-gray-300 rounded-full opacity-15"></div>
        <div className="absolute bottom-1/3 right-2 w-20 h-20 border border-gray-300 transform rotate-12 opacity-15"></div>
        
        {/* Mobile responsive positioning - much larger */}
        <div className="md:hidden absolute top-4 right-4 w-16 h-16 border border-gray-400 rounded-full opacity-30"></div>
        <div className="md:hidden absolute bottom-12 left-4 w-14 h-14 border border-gray-400 transform rotate-45 opacity-30"></div>

        {/* Main Headline */}
        <div className="text-center mb-8">
          <h1 className="text-6xl md:text-8xl font-bold text-black font-serif mb-4">
            Resume
          </h1>
          <h1 className="text-6xl md:text-8xl font-bold text-black font-serif">
            Reinvent.
          </h1>
        </div>

        {/* Descriptive Text */}
        <p className="text-center text-gray-700 font-sans text-lg max-w-2xl mb-12 leading-relaxed">
          Your curriculum vitae is a reflection of your professional story. We help you tell it with clarity and impact. Upload your document to begin the transformation.
        </p>

        {/* CV Upload Area */}
        <div className="w-full max-w-2xl">
          <div
            {...getRootProps()}
            onClick={handleClick}
            className={`
              border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-200
              ${isDragActive ? 'border-cyan-400 bg-cyan-50' : 'border-cyan-300 hover:border-cyan-400 hover:bg-cyan-50'}
              ${isDragReject ? 'border-red-400 bg-red-50' : ''}
              ${isProcessing ? 'pointer-events-none opacity-50' : ''}
            `}
          >
            <input {...getInputProps()} ref={fileInputRef} />
            
            {isProcessing ? (
              <div className="space-y-4">
                <div className="animate-spin w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full mx-auto"></div>
                <p className="text-gray-600 font-sans">Processing your CV...</p>
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-xl font-bold text-gray-800 font-sans">Upload Your CV</p>
                <p className="text-sm text-gray-500 font-sans">DRAG & DROP OR CLICK</p>
              </div>
            )}
          </div>

          {/* Upload Specifications */}
          <p className="text-center text-sm text-gray-600 font-sans mt-4">
            PDF up to 5MB
          </p>

          {/* Uploaded File Info */}
          {uploadedFile && (
            <div className="mt-6 p-4 bg-white rounded-lg shadow-sm border">
              <p className="text-sm text-gray-600 font-sans">
                <span className="font-semibold">File:</span> {uploadedFile.name}
              </p>
              <p className="text-sm text-gray-600 font-sans">
                <span className="font-semibold">Size:</span> {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          )}

          {/* Extracted Text Display */}
          {extractedText && (
            <div className="mt-8 p-6 bg-white rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-800 font-sans mb-4">Extracted Text:</h3>
              <div className="max-h-96 overflow-y-auto">
                <pre className="text-sm text-gray-700 font-sans whitespace-pre-wrap">{extractedText}</pre>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-6">
        <p className="text-sm text-gray-600 font-sans">
          © 2025 RESUME REINVENT. ALL RIGHTS RESERVED.
        </p>
      </footer>
    </div>
  );
}