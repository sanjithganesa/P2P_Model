# excel_utils.py
import openpyxl
import os
from datetime import datetime

# Path to the Excel file for tracking
EXCEL_FILE_PATH = 'file_transfer_tracking.xlsx'

def initialize_excel_file():
    """Initialize the Excel file with headers if it doesn't exist."""
    if not os.path.exists(EXCEL_FILE_PATH):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "File Transfers"
        ws.append(["Timestamp", "File Name", "Transfer Type", "Status"])
        wb.save(EXCEL_FILE_PATH)

def log_transfer(file_name, transfer_type, status):
    """Log file transfer details into the Excel sheet."""
    wb = openpyxl.load_workbook(EXCEL_FILE_PATH)
    ws = wb.active
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([timestamp, file_name, transfer_type, status])
    wb.save(EXCEL_FILE_PATH)
