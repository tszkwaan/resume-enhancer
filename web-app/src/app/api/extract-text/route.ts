import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { writeFile, unlink } from 'fs/promises';
import { join } from 'path';
import { tmpdir } from 'os';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ message: 'No file provided' }, { status: 400 });
    }

    // Validate file type - only PDF files supported with PyMuPDF
    if (file.type !== 'application/pdf') {
      return NextResponse.json({ 
        message: 'Invalid file type. Only PDF files are allowed.' 
      }, { status: 400 });
    }

    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      return NextResponse.json({ 
        message: 'File too large. Maximum size is 5MB.' 
      }, { status: 400 });
    }

    // Create temporary file
    const buffer = Buffer.from(await file.arrayBuffer());
    const tempFilePath = join(tmpdir(), `temp_${Date.now()}_${file.name}`);
    await writeFile(tempFilePath, buffer);

    try {
      // Extract text using Python script
      const extractedText = await extractTextFromFile(tempFilePath);
      
      // Optional: Preprocess the extracted text
      const preprocessedText = await preprocessText(extractedText);
      
      // Debug: Print anonymized text to console
      console.log('=== RAW EXTRACTED TEXT ===');
      console.log(extractedText);
      console.log('\n=== ANONYMIZED TEXT ===');
      console.log(preprocessedText);
      console.log('========================\n');
      
      // Clean up temporary file
      await unlink(tempFilePath);

      return NextResponse.json({ 
        text: preprocessedText,
        rawText: extractedText, // Include raw text for comparison
        filename: file.name,
        size: file.size
      });

    } catch (error) {
      // Clean up temporary file on error
      await unlink(tempFilePath);
      throw error;
    }

  } catch (error) {
    console.error('Error processing file:', error);
    return NextResponse.json({ 
      message: 'Error processing file. Please try again.' 
    }, { status: 500 });
  }
}

function extractTextFromFile(filePath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    // Use direct Python call with Tesseract OCR
    const pythonScript = join(process.cwd(), 'scripts', 'extract_text.py');
    const python = spawn('python3', [pythonScript, filePath]);

    let output = '';
    let error = '';

    python.stdout.on('data', (data) => {
      output += data.toString();
    });

    python.stderr.on('data', (data) => {
      error += data.toString();
    });

    python.on('close', (code) => {
      if (code === 0) {
        resolve(output.trim());
      } else {
        reject(new Error(`Python script failed: ${error}`));
      }
    });

    python.on('error', (err) => {
      reject(new Error(`Failed to start Python process: ${err.message}`));
    });
  });
}

function preprocessText(text: string): Promise<string> {
  return new Promise((resolve, reject) => {
    console.log('Starting preprocessing...');
    
    // Use the personal information anonymization Python script
    const pythonScript = join(process.cwd(), 'scripts', 'anonymize_personal_info.py');
    const python = spawn('python3', [pythonScript, text]);

    let output = '';
    let error = '';

    python.stdout.on('data', (data) => {
      output += data.toString();
    });

    python.stderr.on('data', (data) => {
      const stderrData = data.toString();
      error += stderrData;
      // Also log stderr to console for debugging
      console.log('Python stderr:', stderrData);
    });

    python.on('close', (code) => {
      console.log(`Preprocessing completed with code: ${code}`);
      if (code === 0) {
        console.log('Preprocessing successful');
        resolve(output.trim());
      } else {
        // If preprocessing fails, return original text
        console.warn('Preprocessing failed, using original text:', error);
        resolve(text);
      }
    });

    python.on('error', (err) => {
      // If preprocessing fails, return original text
      console.warn('Preprocessing error, using original text:', err.message);
      resolve(text);
    });
  });
}
