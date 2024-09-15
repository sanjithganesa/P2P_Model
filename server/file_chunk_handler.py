import socket
import os

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to localhost (127.0.0.1) and a port (e.g., 5000)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(1)
print("Server is listening on 127.0.0.1:5000")

def search_file(directory, file_name):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

while True:
    # Accept the client connection
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # Receive the mode of operation (REQUEST or SEND) from the client
    mode = conn.recv(1024).decode()
    print(f"Mode of operation: {mode}")

    if mode == 'REQUEST':
        # Directory where the files are stored
        storage_path = 'storage_system'
        
        # Client is requesting a file from the server
        file_name = conn.recv(1024).decode()
        print(f"Client requested file: {file_name}")
        
        # Search for the file in the entire directory structure
        file_path = search_file(storage_path, file_name)
        
        if file_path:
            conn.sendall(b'File found, ready to send.')
            
            # Send the file in chunks
            with open(file_path, 'rb') as f:
                while True:
                    chunk_data = f.read(4096)
                    if not chunk_data:
                        break
                    conn.sendall(chunk_data)
                    print(f"Sent chunk")

            # Send the end marker to indicate completion
            conn.sendall(b'end_the_loop_here')
            print("Sent end marker.")
            
            # Close the connection
            conn.close()
            # Exit after sending the file
            break

        else:
            conn.sendall(b'File not found')
            conn.close()

    elif mode == 'SEND':
        # The client wants to send a file to the server
        file_name = conn.recv(1024).decode()
        print(f"Client wants to send file: {file_name}")

        # Directory where the chunks will be stored
        chunk_storage_path = 'storage_system'
        os.makedirs(chunk_storage_path, exist_ok=True)

        reassembled_file_path = os.path.join(chunk_storage_path, file_name)

        # Create or overwrite the file in one go
        with open(reassembled_file_path, 'wb') as f:
            while True:
                chunk_data = conn.recv(4096)
                
                # Check if the received chunk contains the end marker
                if b'end_the_loop_here' in chunk_data:
                    # Write the data up to the end marker
                    end_marker_index = chunk_data.index(b'end_the_loop_here')
                    f.write(chunk_data[:end_marker_index])
                    print("End of file marker received.")
                    break
                else:
                    f.write(chunk_data)
                    print("Received and wrote chunk to file")

        print(f"Received and saved file: {file_name}")
        conn.close()
        # Exit after receiving the file
        break

    else:
        print("Unknown mode received.")
        conn.close()

# Close the server socket
server_socket.close()
print("Server has been shut down.")
