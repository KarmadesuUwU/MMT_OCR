# MMT_OCR
Artificial Vision System to Metrology System Reports

## Description

This program allows extracting text and table data from PDF files using computer vision and OCR (Optical Character Recognition) techniques. It is ideal for processing PDF documents with specific structures and generating results in CSV format.

## Features

- **OCR with EasyOCR**: Uses EasyOCR for text recognition in images.
- **Image processing**: Converts PDF pages into high-resolution images to improve OCR accuracy.
- **Structured data extraction**: Identifies and extracts data from specific regions of PDF pages.
- **Support for multiple cases**: Handles PDF documents with varying numbers of pages and structures.
- **CSV export**: Saves extracted data into a CSV file for easy analysis.

## Requirements

- Python 3.8 or higher
- Required libraries (installable with `pip`):
    - `PyMuPDF` (fitz)
    - `EasyOCR`
    - `OpenCV` (cv2)
    - `NumPy`
    - `Matplotlib`
    - `Tkinter` (included with Python)
    - `csv`

## Installation

1. Clone this repository or download the `MMT_OCR.py` file.
2. Install the required dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```
     *(Create a `requirements.txt` file if it does not exist, listing the libraries mentioned above).*

## Usage

1. Run the program from the command line:
     ```bash
     python MMT_OCR.py <path_to_PDF_file>
     ```
     Or simply execute the script to open a dialog box and select a PDF file.

2. The program will process the PDF file and generate:
     - Preprocessed images of the regions of interest in the `output_images` folder.
     - A CSV file with the extracted data in the same location as the PDF.

## Example

```bash
python MMT_OCR.py "C:/Users/sm10244/Downloads/example.pdf"
```

Expected output:
- `output_images` folder with processed images.
- `example.pdf_extracted_text.csv` file with the extracted data.

## Notes

- Ensure that EasyOCR models are available in the path specified in the code.
- The program is designed to handle PDF documents with specific structures. If the PDF format varies, you may need to adjust the coordinates of the regions of interest in the code.

## Contribution

If you want to contribute to this project, you can submit a pull request or report issues in the repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
