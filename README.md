# Keylogger with Encryption and Google Drive Upload

A Python-based keylogger that captures keyboard input, encrypts it using Fernet encryption, and automatically uploads logs to Google Drive.

## Features

- **Real-time Keylogging**: Captures all keyboard input including letters, numbers, symbols, and special keys
- **Encryption**: Uses Fernet symmetric encryption to secure logged data
- **Google Drive Integration**: Automatically uploads encrypted logs to Google Drive at configurable intervals
- **Cross-platform**: Works on Windows systems
- **Stealth Operation**: Runs without admin privileges using polling-based input detection
- **Startup Integration**: Automatically adds itself to Windows startup folder

## Project Structure

```
Encryption/
├── Decrypt.py              # Decryption utility for encrypted logs
└── generate_key.py         # Key generation utility
main/
├── input_logger_no_admin_polling.py  # Main keylogger script
├── key.key                 # Encryption key file
├── run_script.bat          # Windows batch script for easy execution
├── creds/
│   ├── credentials.json    # Google Drive API credentials
│   └── token.json          # Google Drive API token
└── logs/
    ├── log_decrypted.txt   # Decrypted log output
    └── log.encrypted       # Encrypted log file
```

## Setup

### 1. Install Dependencies

The script will automatically install required packages, but you can also install them manually:

```bash
pip install cryptography google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Generate Encryption Key

Run the key generation script to create a new encryption key:

```bash
cd Encryption
python generate_key.py
```

This will create a `key.key` file in the Encryption directory.

### 3. Google Drive API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API
4. Create credentials (OAuth 2.0 Client ID) for a desktop application
5. Download the credentials JSON file and save it as [`main/creds/credentials.json`](main/creds/credentials.json)

### 4. Configuration

Update the credential files:

- Replace the content in [`main/creds/credentials.json`](main/creds/credentials.json) with your actual Google Drive API credentials
- The [`main/creds/token.json`](main/creds/token.json) will be automatically generated on first run

## Usage

### Running the Keylogger

#### Method 1: Using the Batch Script

```batch
cd main
run_script.bat path\to\key.key
```

#### Method 2: Direct Python Execution

```bash
cd main
pythonw input_logger_no_admin_polling.py --key path\to\key.key
```

### Command Line Arguments

The main script supports several command-line arguments:

- `--key` (required): Path to the encryption key file
- `--output` (optional): Path for the encrypted log file (default: `logs/log.encrypted`)
- `--credentials` (optional): Path to Google Drive credentials file (default: `creds/credentials.json`)
- `--token` (optional): Path to Google Drive token file (default: `creds/token.json`)
- `--upload-interval` (optional): Upload interval in seconds (default: 300)

### Decrypting Logs

To decrypt the captured logs:

```bash
cd Encryption
python Decrypt.py --key path\to\key.key --file path\to\encrypted\log --output path\to\decrypted\log
```

## Security Features

- **Fernet Encryption**: All captured keystrokes are encrypted using cryptographically secure Fernet encryption
- **Secure Key Storage**: Encryption keys are stored separately from the main application
- **No Admin Privileges**: Operates without requiring administrator privileges
- **Automatic Cleanup**: Regularly uploads and can be configured to clean local files

## Files Overview

### Main Components

- [`main/input_logger_no_admin_polling.py`](main/input_logger_no_admin_polling.py): Core keylogger with encryption and Google Drive upload
- [`Encryption/Decrypt.py`](Encryption/Decrypt.py): Utility to decrypt encrypted log files
- [`Encryption/generate_key.py`](Encryption/generate_key.py): Generates encryption keys
- [`main/run_script.bat`](main/run_script.bat): Windows batch script for easy deployment

### Configuration Files

- [`main/key.key`](main/key.key): Contains the Fernet encryption key
- [`main/creds/credentials.json`](main/creds/credentials.json): Google Drive API credentials
- [`main/creds/token.json`](main/creds/token.json): Google Drive API token (auto-generated)

### Log Files

- [`main/logs/log.encrypted`](main/logs/log.encrypted): Encrypted keystroke logs
- [`main/logs/log_decrypted.txt`](main/logs/log_decrypted.txt): Decrypted log output

## Important Notes

⚠️ **Legal Disclaimer**: This software is intended for educational and authorized testing purposes only. Always ensure you have proper authorization before monitoring any system. Unauthorized use may violate local, state, and federal laws.

⚠️ **Security**: Keep your encryption keys and Google Drive credentials secure. Anyone with access to these can decrypt your logs or access your Google Drive.

⚠️ **Privacy**: Be aware of privacy implications when logging keystrokes, especially on shared or work computers.

## License

This project is for educational purposes only. Use responsibly and in accordance with applicable laws and regulations.
