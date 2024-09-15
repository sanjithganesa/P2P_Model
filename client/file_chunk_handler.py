# file_chunk_handler.py
import os
import hashlib

# Function to receive a file chunk from the client and store it
def receive_chunk(conn, chunk_number, chunk_storage_path, chunk_size):
    chunk_data = conn.recv(chunk_size)
    if not chunk_data:
        return False  # No more data
    
    chunk_file_path = os.path.join(chunk_storage_path, f'chunk_{chunk_number}')
    
    with open(chunk_file_path, 'wb') as chunk_file:
        chunk_file.write(chunk_data)
    
    return True

# Function to reassemble the file from the received chunks
def reassemble_file(chunk_storage_path, output_file_path, total_chunks):
    with open(output_file_path, 'wb') as output_file:
        for chunk_number in range(total_chunks):
            chunk_file_path = os.path.join(chunk_storage_path, f'chunk_{chunk_number}')
            with open(chunk_file_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
            os.remove(chunk_file_path)  # Delete the chunk file after writing it
            print(f"Deleted {chunk_file_path}")
    print(f"File reassembled and saved as {output_file_path}")
    
# Function to compute the hash of a file for integrity check
def compute_file_hash(file_path, hash_algo='sha256'):
    hasher = hashlib.new(hash_algo)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to compare hashes of original and received file for integrity
def verify_file_integrity(original_file_path, reassembled_file_path):
    original_hash = compute_file_hash(original_file_path)
    reassembled_hash = compute_file_hash(reassembled_file_path)
    
    if original_hash == reassembled_hash:
        print("File integrity verified: Hashes match!")
        return True
    else:
        print("File integrity check failed: Hashes do not match.")
        return False
