import socket
import os

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server running on localhost (127.0.0.1) and port 5000
server_ip = '127.0.0.1'
server_port = 5000
client_socket.connect((server_ip, server_port))

# Ask the user what they want to do: request or send a file
mode = input("Enter mode of operation (REQUEST or SEND): ").strip().upper()

# Send the mode to the server
client_socket.sendall(mode.encode())

if mode == 'REQUEST':
    # Request the file from the server
    file_name = input("Enter the file name to request from the server: ")
    client_socket.sendall(file_name.encode())
    
    # Receive the server's response
    response = client_socket.recv(1024).decode()
    if response == 'File found, ready to send.':
        print(f"Server is sending file: {file_name}")
        
        # Prepare to receive the file in chunks
        chunk_storage_path = 'receiver_end'  # Directory to store the received chunks
        os.makedirs(chunk_storage_path, exist_ok=True)
        
        with open(os.path.join(chunk_storage_path, file_name), 'wb') as f:
            while True:
                chunk_data = client_socket.recv(4096)
                if chunk_data.endswith(b'end_the_loop_here'):
                    # Write the chunk data excluding the end marker
                    f.write(chunk_data[:-len(b'end_the_loop_here')])
                    print("Received end marker and final chunk.")
                    break
                f.write(chunk_data)
                print("Received chunk")

        print(f"Received and saved file: {file_name}")

    else:
        print(response)

elif mode == 'SEND':
    # Send a file to the server
    file_path = input("Enter the path of the file to send to the server: ")
    file_name = os.path.basename(file_path)
    client_socket.sendall(file_name.encode())
    
    # Read and send the file in chunks
    with open(file_path, 'rb') as f:
        while True:
            chunk_data = f.read(4096)
            if not chunk_data:
                break
            client_socket.sendall(chunk_data)
            print("Sent chunk")
    
    # Notify server that the file has been sent
    client_socket.sendall(b'end_the_loop_here')

else:
    print("Unknown mode selected.")

# Close the connection
client_socket.close()
