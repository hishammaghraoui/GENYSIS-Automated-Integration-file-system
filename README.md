# GENYSIS-Automated-Integration-file-system
Automated Integration of NGS Data into Cloud-Based Analysis Pipeline for gynisis platform 
Automation Code Readme
# FASTQ File Splitter and Uploader

## Overview
This automation code simplifies the process of splitting FASTQ files and uploading the resulting chunks to a remote server. It is particularly useful for handling large FASTQ files commonly used in bioinformatics.

## Usage Instructions
1. **Select FASTQ Files**: Click the "Browse Files" button to select one or more FASTQ files for splitting. You can select multiple files by holding down the Ctrl key while clicking.

2. **Enter User ID**: Provide a unique User ID to identify the uploaded files. If you upload multiple files, "R" will be added to the User ID to indicate paired-end files.

3. **Enter Chunk Size (KB)**: Specify the size (in kilobytes) of each chunk that the FASTQ files will be split into.

4. **Select FASTQ Type**: Choose whether the FASTQ files are "Single-End" or "Paired-End."

5. **Split and Upload**: Click the "Split and Upload FASTQ Files" button to start the process. The code will split the selected FASTQ files, create chunks, and upload them to a remote server.

## Dependencies
- Python (>=3.6)
- Tkinter (for the graphical user interface)
- Paramiko (for SSH/SFTP communication)

## Configuration
- Replace `'your-vm-ip-address'`, `'your-vm-username'`, `'your-vm-password'`, and `'/path/on/remote/vm/'` in the code with your actual VM and path information.

## Notes
- This code assumes that the remote server uses SSH/SFTP for file transfer.

---

*Please adjust the configuration settings to match your specific environment.*
File Handling System Readme
# File Handling System

## Overview
The file handling system provides a set of Python scripts to split and join files efficiently.

## Splitting Files
- The `split` command splits a file into smaller chunks.
- Usage: `python split.py --file <input_file> --destination <output_directory> --size <chunk_size>`

## Joining Files
- The `join` command joins split files to recreate the original file.
- Usage: `python join.py --source-dir <directory_with_chunks> --output <output_file>`

## Dependencies
- Python (>=3.6)

---

*Please ensure you have Python installed and follow the provided usage instructions.*

Split and Join Code Readme
# Split and Join Code

## Overview
The provided Python code includes two commands: `split` and `join`, which are used for splitting and joining files.

## Splitting Files (`split` command)
- The `split` command is used to split a large file into smaller chunks.
- Usage: `python split.py --file <input_file> --destination <output_directory> --size <chunk_size>`

## Joining Files (`join` command)
- The `join` command is used to join previously split files to reconstruct the original file.
- Usage: `python join.py --source-dir <directory_with_chunks> --output <output_file>`

## Dependencies
- Python (>=3.6)
- pathlib (for handling file paths)
- click (for creating command-line interfaces)

## Notes
- You can customize the `--size` parameter when splitting files to specify the maximum chunk size.

---

*Please adjust the code as needed and follow the provided usage instructions.*
