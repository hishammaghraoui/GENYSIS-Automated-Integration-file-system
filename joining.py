import os
from pathlib import Path


def join_chunks_in_folders(root_dir):
    root_path = Path(root_dir)
    
    for folder in root_path.iterdir():
        if folder.is_dir():
            print(f'Processing folder: {folder}')
            join_chunks_in_folder(folder)


def join_chunks_in_folder(folder_path):
    chunks = list(folder_path.glob('*.chk'))
    chunks.sort()
    unique_ids = set()

    for chunk in chunks:
        chunk_name = chunk.stem
        unique_id = chunk_name.split('_')[0]
        unique_ids.add(unique_id)

    for unique_id in unique_ids:
        output_file_path = folder_path / f'{unique_id}.fastq'
        with open(output_file_path, 'ab') as output_file:
            for chunk in chunks:
                chunk_name = chunk.stem
                if chunk_name.startswith(unique_id):
                    with open(chunk, 'rb') as piece:
                        while True:
                            bfr = piece.read()
                            if not bfr:
                                break
                            output_file.write(bfr)

        print(f'Files with ID {unique_id} in folder {folder_path} have been reassembled.')

        # Remove the joined chunks
        for chunk in chunks:
            chunk.unlink()

        print(f'Chunks have been removed from folder {folder_path}.')


source_directory = 'files'  # Root directory containing subfolders with chunks

join_chunks_in_folders(source_directory)
