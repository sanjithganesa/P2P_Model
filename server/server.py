import socket
import os
from excel_utils import initialize_excel_file, log_transfer
import signal
import sys
import threading

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to localhost (127.0.0.1) and port 5000
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(1)
print("Server is listening on 127.0.0.1:5000")

# Initialize the Excel file for tracking
initialize_excel_file()

# Flag to indicate server shutdown
shutdown_flag = threading.Event()

def search_file(directory, file_name):
    """Search for a file in the specified directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def handle_client(conn):
    """Handle communication with a single client."""
    try:
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
                log_transfer(file_name, 'REQUEST', 'Started')

                # Send the file in chunks
                with open(file_path, 'rb') as f:
                    chunk_number = 0
                    while True:
                        chunk_data = f.read(4096)
                        if not chunk_data:
                            break
                        conn.sendall(chunk_data)
                        print(f"Sent chunk {chunk_number}")
                        chunk_number += 1

                # Send the end marker to indicate completion
                conn.sendall(b'end_the_loop_here')
                print("Sent end marker.")
                
                # Log completion
                log_transfer(file_name, 'REQUEST', 'Completed')

            else:
                conn.sendall(b'File not found')
                log_transfer(file_name, 'REQUEST', 'File Not Found')

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
                    if not chunk_data:
                        break
                    if b'end_the_loop_here' in chunk_data:
                        # Write the chunk data excluding the end marker
                        end_marker_pos = chunk_data.find(b'end_the_loop_here')
                        f.write(chunk_data[:end_marker_pos])
                        print("Received end marker and final chunk.")
                        break
                    f.write(chunk_data)
                    print("Received chunk")

            print(f"Received and saved file: {file_name}")
            log_transfer(file_name, 'SEND', 'Completed')

            # Set shutdown flag to stop accepting new connections and exit
            shutdown_flag.set()

        else:
            print("Unknown mode received.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()
        print("Connection closed.")

def signal_handler(sig, frame):
    """Handle shutdown signals."""
    print("Shutdown signal received. Closing server...")
    shutdown_flag.set()

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def accept_connections():
    """Accept connections in a loop."""
    try:
        while not shutdown_flag.is_set():
            try:
                # Accept the client connection
                conn, addr = server_socket.accept()
                print(f"Connected to {addr}")

                # Handle the client in a separate thread
                client_thread = threading.Thread(target=handle_client, args=(conn,))
                client_thread.start()

            except Exception as e:
                print(f"Connection handling error: {e}")

    finally:
        # Ensure the server socket is closed
        if server_socket.fileno() != -1:
            server_socket.shutdown(socket.SHUT_RDWR)  # Ensure all operations are completed
            server_socket.close()
        print("Server has been shut down.")

        # Exit the script immediately
        sys.exit(0)

# Start accepting connections
accept_connections()
