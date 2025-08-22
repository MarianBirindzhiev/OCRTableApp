# OCRTableApp

A Python-based desktop application that combines Optical Character Recognition (OCR) with an interactive table interface for extracting and organizing text from images.

## Overview

OCRTableApp allows users to extract text from images and organize that text into spreadsheet-like tables through an intuitive point-and-click interface. The application features a sophisticated modular architecture with comprehensive GUI functionality and robust data management capabilities.

## Features

### 🔍 OCR Processing
- **Multiple Input Methods**: Load images from files or capture screenshots in real-time
- **Advanced Image Processing**: Automatic resizing, grayscale conversion, and contrast enhancement (CLAHE)
- **Multi-language Support**: Powered by EasyOCR with configurable language settings (default: English)
- **GPU Acceleration**: Optional GPU support for faster text recognition
- **Multi-monitor Support**: Enhanced screenshot functionality across multiple displays

### 📊 Interactive Table Interface
- **Visual Word Selection**: Click on detected words in images to insert them into tables
- **Dynamic Grid**: Customizable table dimensions with automatic expansion
- **Multiple Navigation Modes**:
  - **Horizontal (→)**: Move right after each entry
  - **Vertical (↓)**: Move down after each entry
  - **Wrap-around (⟳)**: Automatic grid expansion
- **Real-time Visual Feedback**: Color-coded bounding boxes and cell highlighting

### ⚡ Advanced Functionality
- **Undo/Redo System**: Full command history with comprehensive state management
- **Keyboard Navigation**: Arrow key support and smart Tab navigation
- **CSV Export**: Save table data with integrated file dialog
- **Direct Cell Editing**: Modify table contents with inline editing
- **Scrollable Interface**: Handle large tables with smooth scrolling

## Technology Stack

- **Language**: Python 100%
- **OCR Engine**: EasyOCR
- **Image Processing**: OpenCV (cv2)
- **GUI Framework**: Tkinter with Matplotlib integration
- **Additional Libraries**: NumPy, Pillow (PIL), MSS

## Installation

### Prerequisites
- Python 3.7+
- Git

### Setup
1. Clone the repository:
```bash
git clone https://github.com/MarianBirindzhiev/OCRTableApp.git
cd OCRTableApp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
```
opencv-python
easyocr
matplotlib
numpy
Pillow
mss
```

## Usage

### Basic Usage
```bash
python main.py [image_path]
```

### Command Line Options
```bash
python main.py --help

optional arguments:
  image_path            Path to the input image (optional)
  --scale_percent       Resize percent (default: 150)
  --output_csv         CSV output file (default: selected_words.csv)
  --lang               OCR language (default: en)
```

### Example
```bash
python main.py document.jpg --scale_percent 200 --lang en
```

## How It Works

1. **Load Image**: Provide an image file or capture a screenshot
2. **OCR Processing**: The application processes the image and detects text regions
3. **Visual Interface**: View the image with red bounding boxes around detected text
4. **Word Selection**: Click on any detected word to insert it into the table
5. **Table Navigation**: Use navigation modes and keyboard shortcuts to organize data
6. **Export**: Save your organized data as a CSV file

## Keyboard Shortcuts

- **Ctrl+Z**: Undo last action
- **Ctrl+Y**: Redo last undone action
- **Tab**: Smart navigation based on current mode
- **Ctrl+Shift+S**: Take screenshot and start OCR
- **Arrow Keys**: Navigate between table cells

## Project Structure

```
OCRTableApp/
├── app/                    # Application management layer
├── ocr/                    # OCR processing and image handling
├── table_controller/       # Table interaction handlers
├── table_core/            # Core table logic and state management
├── table_ui/              # User interface components
├── utilities/             # Helper functions and constants
├── assets/                # Application icons and resources
├── .github/workflows/     # CI/CD automation
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **OCR Module**: Handles image processing, text recognition, and visual feedback
- **Table System**: Manages grid state, navigation, and data operations
- **UI Layer**: Provides interactive components and user interface
- **Command System**: Implements undo/redo functionality with command pattern
- **Utilities**: Shared functionality including logging, export, and configuration

The project includes GitHub Actions workflows for automated building:

- **Windows**: Generates `.exe` executable
- **macOS**: Creates `.app` application bundle
