# 🔁 Client-Server P2P File Transfer System

This project implements a **Peer-to-Peer (P2P) File Transfer Model** using a **Client-Server architecture**, developed entirely by **Sanjith Ganesa P**. The model enables efficient file sharing between peers in a decentralized manner, with server support for connection management and coordination.

---

## 📌 Project Overview

In this system:
- A **central server** keeps track of active peers and their available files.
- **Clients** register themselves with the server and share or request files from other peers.
- **File transfers** occur directly between peers using socket communication, bypassing the server after discovery.

This setup is ideal for:
- Simulating decentralized file sharing (like BitTorrent)
- Understanding network protocols
- Demonstrating basic P2P concepts

---

## ⚙️ Technologies Used

- 🖥️ Python (or Java/C/C++) for client-server socket programming
- 📡 TCP/IP protocol for reliable data transfer
- 📂 File I/O for upload/download operations
- 📶 Optional threading or multiprocessing for concurrent connections

---

## 📁 Project Structure

```bash
p2p-file-transfer/
├── server.py            # Main server that manages peer connections
├── client.py            # Peer client to send/receive files
├── README.md
└── /screenshots/        # Add screenshots here
````

---

## 🚀 Getting Started

### 1. Start the Server

```bash
python server.py
```

### 2. Start Clients (In separate terminals or machines)

```bash
python client.py
```

Each client can:

* Register with the server
* Share files
* View list of available peers/files
* Request and download files from other clients

---

## 🧪 Features

* ✅ Centralized registration and peer discovery
* 🔁 Decentralized file transfer (P2P)
* 📥 Download files from other peers directly
* 📤 Upload or serve files to others
* 🧵 Supports concurrent requests (if multithreaded)

---

## 📸 Screenshots

--Performance Analysis ScreenShots

<img width="944" height="465" alt="image" src="https://github.com/user-attachments/assets/96a3ff2c-bf15-432a-bdd7-71f032e237c2" />

<img width="933" height="467" alt="image" src="https://github.com/user-attachments/assets/61d7d396-1421-4d89-b7b0-b44616ccb59b" />

<img width="941" height="471" alt="image" src="https://github.com/user-attachments/assets/fb65d645-9081-4793-a4c0-f0031cf673eb" />

<img width="937" height="469" alt="image" src="https://github.com/user-attachments/assets/cfc21513-6917-4ae0-948e-84806ca5ccd6" />

<img width="938" height="469" alt="image" src="https://github.com/user-attachments/assets/79c76def-e634-4891-9295-9ce7aef75d85" />

<img width="938" height="469" alt="image" src="https://github.com/user-attachments/assets/4e8b6ea7-397c-4165-aaed-116d32998b7f" />

---

## 💡 Future Improvements

* 🌐 Add GUI using Tkinter or PyQt
* 🔐 Add basic encryption/authentication
* 🌍 Support file chunking for large file handling
* 📊 Track transfer status and bandwidth

---

---

## 📄 License

This project is intended for educational and demonstration purposes. Contact the author for reuse or collaboration.

---
