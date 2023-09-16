import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import paramiko

def _chunk_file(file, extension, destination, unique_id, chunk_size):
    d = Path(destination)
    d.mkdir(parents=True, exist_ok=True)

    folder_path = d / unique_id
    folder_path.mkdir(parents=True, exist_ok=True)

    current_chunk_size = 0
    current_chunk = 1
    done_reading = False
    while not done_reading:
        with open(f'{folder_path}/{unique_id}_{current_chunk}{extension}.chk', 'ab') as chunk:
            while True:
                bfr = file.read(chunk_size)
                if not bfr:
                    done_reading = True
                    break

                chunk.write(bfr)
                current_chunk_size += len(bfr)
                if current_chunk_size >= chunk_size:
                    current_chunk += 1
                    current_chunk_size = 0
                    break

def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def split_file_and_upload():
    file_path = file_entry.get()
    user_id = user_id_entry.get()
    chunk_size = int(chunk_size_entry.get()) * 1024

    if not file_path or not Path(file_path).exists() or not user_id or chunk_size <= 0:
        status_label.config(text='File, User ID, and Chunk Size are required and should be positive')
        return

    fastq_type = fastq_type_var.get()
    if fastq_type == 'Single-End':
        user_id += 'S'
    elif fastq_type == 'Paired-End':
        user_id += 'R'

    with open(file_path, 'rb') as file_stream:
        _chunk_file(file_stream, Path(file_path).suffix, '.', user_id, chunk_size)
        status_label.config(text=f'File split with User ID: {user_id}')

    upload_chunks_to_vm(user_id)

def upload_chunks_to_vm(user_id):
    chunks_folder = Path(user_id)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('138.197.124.85', username='root', password='')

    sftp = ssh.open_sftp()

    # Create a new directory on the VM with the user_id
    remote_dir = f'/home/Genisys/upload/{user_id}'
    sftp.mkdir(remote_dir)

    for chunk_file in chunks_folder.glob('*.chk'):
        remote_path = f'{remote_dir}/{chunk_file.name}'
        sftp.put(str(chunk_file), remote_path)
        print(f'Chunk {chunk_file} uploaded to remote VM')

    sftp.close()
    ssh.close()

root = tk.Tk()
root.title('FASTQ File Splitter and Uploader')

style = ttk.Style()
style.theme_use('clam')

main_frame = ttk.Frame(root, padding=20)
main_frame.pack()

file_label = ttk.Label(main_frame, text='Select FASTQ File:')
file_label.grid(row=0, column=0, sticky='w')

file_entry = ttk.Entry(main_frame)
file_entry.grid(row=0, column=1, sticky='ew')

browse_button = ttk.Button(main_frame, text='Browse', command=browse_file)
browse_button.grid(row=0, column=2)

user_id_label = ttk.Label(main_frame, text='Enter User ID:')
user_id_label.grid(row=1, column=0, sticky='w')

user_id_entry = ttk.Entry(main_frame)
user_id_entry.grid(row=1, column=1, sticky='ew')

chunk_size_label = ttk.Label(main_frame, text='Enter Chunk Size (KB):')
chunk_size_label.grid(row=2, column=0, sticky='w')

chunk_size_entry = ttk.Entry(main_frame)
chunk_size_entry.grid(row=2, column=1, sticky='ew')

fastq_type_label = ttk.Label(main_frame, text='Select FASTQ Type:')
fastq_type_label.grid(row=3, column=0, sticky='w')

fastq_type_var = tk.StringVar(value='Single-End')

fastq_type_frame = ttk.Frame(main_frame)
single_end_radio = ttk.Radiobutton(fastq_type_frame, text='Single-End', variable=fastq_type_var, value='Single-End')
paired_end_radio = ttk.Radiobutton(fastq_type_frame, text='Paired-End', variable=fastq_type_var, value='Paired-End')
single_end_radio.pack(side=tk.LEFT)
paired_end_radio.pack(side=tk.LEFT)
fastq_type_frame.grid(row=3, column=1, sticky='w')

split_button = ttk.Button(main_frame, text='Split and Upload FASTQ File', command=split_file_and_upload)
split_button.grid(row=4, columnspan=3)

status_label = ttk.Label(main_frame, text='', font=('Helvetica', 12, 'bold'))
status_label.grid(row=5, columnspan=3)

root.mainloop()
