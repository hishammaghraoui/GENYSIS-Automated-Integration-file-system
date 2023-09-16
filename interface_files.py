import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def _chunk_file(file, extension, destination, unique_id):

    d = Path(destination)
    d.mkdir(parents=True, exist_ok=True)

    current_chunk = 1
    done_reading = False
    while not done_reading:
        with open(f'{destination}/{unique_id}_{current_chunk}{extension}.chk', 'ab') as chunk:
            bfr = file.read(read_buffer_size)
            if not bfr:
                done_reading = True
                break

            chunk.write(bfr)
            current_chunk += 1


def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)


def detect_fastq_type(file_path):
    with open(file_path, 'r') as file:
        line_count = 0
        read1_identifiers = set()
        read2_identifiers = set()

        for line in file:
            line_count += 1
            if line_count % 4 == 1:  # Read identifier line
                identifier = line.strip()
                if identifier.endswith('/1'):
                    read1_identifiers.add(identifier[:-2])  # Remove /1 suffix
                elif identifier.endswith('/2'):
                    read2_identifiers.add(identifier[:-2])  # Remove /2 suffix

            if line_count >= 4000:  # Stop after reading a reasonable number of lines
                break

    if read1_identifiers and read2_identifiers:
        return 'Paired-End'
    elif read1_identifiers:
        return 'Single-End (Read 1)'
    elif read2_identifiers:
        return 'Single-End (Read 2)'
    else:
        return 'Unknown'


def split_file():
    file_path = file_entry.get()
    user_id = user_id_entry.get()

    if not file_path or not Path(file_path).exists() or not user_id:
        status_label.config(text='File and User ID are required')
        return

    fastq_type = detect_fastq_type(file_path)
    if fastq_type == 'Single-End (Read 1)' or fastq_type == 'Single-End (Read 2)':
        user_id += 'S'
    elif fastq_type == 'Paired-End':
        user_id += 'R'

    with open(file_path, 'rb') as file_stream:
        _chunk_file(file_stream, Path(file_path).suffix, '.', user_id)
        status_label.config(text=f'File split with User ID: {user_id}')


read_buffer_size = 1024

root = tk.Tk()
root.title('File Splitter')

file_label = tk.Label(root, text='Select File:')
file_label.pack()

file_entry = tk.Entry(root)
file_entry.pack()

browse_button = tk.Button(root, text='Browse', command=browse_file)
browse_button.pack()

user_id_label = tk.Label(root, text='Enter User ID:')
user_id_label.pack()

user_id_entry = tk.Entry(root)
user_id_entry.pack()

split_button = tk.Button(root, text='Split File', command=split_file)
split_button.pack()

status_label = tk.Label(root, text='')
status_label.pack()

root.mainloop()
