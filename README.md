# 🖼️ PicMatrix Studio - Batch Image Processor

> **A High-Performance Desktop Image Processing Utility Built with Python, CustomTkinter, and Pillow.**

PicMatrix Studio is an intuitive, dopamine-themed desktop application designed for researchers, designers, and students to effortlessly handle bulk imaging tasks. Whether you are dealing with hundreds of medical imaging slices (such as dMRI scans, histological slices) or daily photography, this tool automates resizing, format conversion, and sequential renaming in a single click—saving you hours of tedious manual labor.

---

## ✨ Key Features

* **⚙️ Multi-Operation Batch Processing**: Run single or complex combinational pipelines simultaneously (e.g., Resize 50% + Convert to PNG + Auto Rename) without creating messy intermediate files.
* **🛡️ Fail-Safe Alpha Channel Prevention**: Smart internal routing that automatically converts transparent alpha channels (`RGBA` / `P`) to pure `RGB` when saving as JPEG, eliminating potential runtime crashes during bulk operations.
* **📂 Automated Non-Destructive Outputs**: Automatically generates an isolated `PicMatrix_Output` directory inside your target folder. Your precious source images remain completely untouched and safe.
* **🎨 Macaron Progress Animation**: Features a smooth-rendering, macaron-green dynamic progress bar with precise real-time file-counter text (`Processed: X / Y images...`) to eliminate UI freezing.

---

## 🛠️ Tech Stack & Dependencies

* **GUI Framework**: `CustomTkinter` (Python 3.10+) - Lightweight, modern look-and-feel.
* **Image Core Engine**: `Pillow` (PIL Fork) - Handles pixel-perfect resampling, filtering, and cross-format IO encoding.
* **File I/O Pipelines**: Built-in `os` and `glob` patterns supporting cross-platform path compatibility and case-insensitive extension matching (e.g., matches both `.png` and `.PNG`).

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python installed, then set up the required graphical and imaging libraries:

```bash
pip install customtkinter Pillow
```

## 介面
<img width="772" height="672" alt="image" src="https://github.com/user-attachments/assets/4a4268c2-32ab-44ae-907b-80361dd673c7" />
