# Keylogger with Encryption and Google Drive Upload

A Python-based keylogger that captures keyboard input, encrypts it using Fernet encryption, and automatically uploads logs to Google Drive.

## Features

- **Real-time Keylogging**: Captures all keyboard input including letters, numbers, symbols, and special keys
- **Encryption**: Uses Fernet symmetric encryption to secure logged data
- **Google Drive Integration**: Automatically uploads encrypted logs to Google Drive at configurable intervals
- **Cross-platform**: Works on Windows systems
- **Stealth Operation**: Runs without admin privileges using polling-based input detection
- **Automatic Dependencies**: Automatically installs required Python packages
- **Startup Integration**: Can be configured to run at system startup

## Project Structure

```
├── README.md
├── requirements.txt
├── Encryption/
│   ├── Decrypt.py              # Decryption utility for encrypted logs
│   ├── generate_key.py         # Key generation utility
│   └── key.key                 # Encryption key file
└── main/
    ├── input_logger_no_admin_polling.py  # Main keylogger script
    ├── run_script.bat          # Windows batch script for easy execution
    ├── creds/
    │   ├── credentials.json    # Google Drive API credentials (template)
    │   └── token.json          # Google Drive API token (template)
    └── logs/
        ├── log_decrypted.txt   # Decrypted log output
        └── log.encrypted       # Encrypted log file
```

## Setup

### 1. Install Dependencies

The script will automatically install required packages when run, but you can also install them manually using the provided requirements file:

```bash
pip install -r requirements.txt
```

**Required packages** (from [requirements.txt](requirements.txt)):

- cryptography
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

### 2. Generate Encryption Key

Run the key generation script to create a new encryption key:

```bash
cd Encryption
python generate_key.py
```

This will create a [`key.key`](Encryption/key.key) file in the Encryption directory.

### 3. Google Drive API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API
4. Create credentials (OAuth 2.0 Client ID) for a desktop application
5. Download the credentials JSON file and replace the template content in [`main/creds/credentials.json`](main/creds/credentials.json)

### 4. Configuration

Update the credential files:

- Replace the template content in [`main/creds/credentials.json`](main/creds/credentials.json) with your actual Google Drive API credentials
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
pythonw input_logger_no_admin_polling.py --key ../Encryption/key.key
```

### Command Line Arguments

The [`main script`](main/input_logger_no_admin_polling.py) supports several command-line arguments:

- `--key` (required): Path to the encryption key file
- `--output` (optional): Path for the encrypted log file (default: `logs/log.encrypted`)
- `--credentials` (optional): Path to Google Drive credentials file (default: `creds/credentials.json`)
- `--token` (optional): Path to Google Drive token file (default: `creds/token.json`)
- `--upload-interval` (optional): Upload interval in seconds (default: 300)

### Example Usage

```bash
# Basic usage with key file
python input_logger_no_admin_polling.py --key ../Encryption/key.key

# Custom output location and upload interval
python input_logger_no_admin_polling.py --key ../Encryption/key.key --output custom_logs/my_log.encrypted --upload-interval 600

# Custom credentials path
python input_logger_no_admin_polling.py --key ../Encryption/key.key --credentials custom_creds/my_credentials.json
```

### Decrypting Logs

To decrypt the captured logs using the [`Decrypt.py`](Encryption/Decrypt.py) script:

```bash
cd Encryption
python Decrypt.py --key key.key --file ../main/logs/log.encrypted --output ../main/logs/log_decrypted.txt
```

**Decryption Arguments:**

- `--key` (required): Path to the encryption key file
- `--file` (optional): Path to the encrypted log file
- `--output` (optional): Path for the decrypted output file

## Security Features

- **Fernet Encryption**: All captured keystrokes are encrypted using cryptographically secure Fernet encryption
- **Secure Key Storage**: Encryption keys are stored separately from the main application
- **No Admin Privileges**: Operates without requiring administrator privileges
- **Automatic Package Management**: Installs dependencies automatically for stealth deployment
- **Configurable Upload Intervals**: Regular uploads to Google Drive with customizable timing

## Log Format

The decrypted logs follow this format:

```
=== Input Log Started at 2025-09-22 18:46:19.912045 ===
[2025-09-22 18:46:46] Key pressed: a
[2025-09-22 18:46:46] Key pressed: s
[2025-09-22 18:47:28] Key pressed: [SPACE]
[2025-09-22 18:48:40] Key pressed: [ENTER]
=== Input Log Ended at 2025-09-22 18:59:48.105510 ===
```

## Files Overview

### Main Components

- [`main/input_logger_no_admin_polling.py`](main/input_logger_no_admin_polling.py): Core keylogger with encryption and Google Drive upload functionality
- [`Encryption/Decrypt.py`](Encryption/Decrypt.py): Utility to decrypt encrypted log files
- [`Encryption/generate_key.py`](Encryption/generate_key.py): Generates Fernet encryption keys
- [`main/run_script.bat`](main/run_script.bat): Windows batch script for easy deployment and startup integration

### Configuration Files

- [`Encryption/key.key`](Encryption/key.key): Contains the Fernet encryption key
- [`main/creds/credentials.json`](main/creds/credentials.json): Google Drive API credentials template
- [`main/creds/token.json`](main/creds/token.json): Google Drive API token template (auto-generated)
- [`requirements.txt`](requirements.txt): Python package dependencies

### Log Files

- [`main/logs/log.encrypted`](main/logs/log.encrypted): Encrypted keystroke logs
- [`main/logs/log_decrypted.txt`](main/logs/log_decrypted.txt): Sample decrypted log output

## Features in Detail

### Automatic Package Installation

The keylogger automatically installs missing Python packages on first run, making deployment easier.

### Polling-based Input Detection

Uses Windows API polling to detect keystrokes without requiring administrator privileges.

### Special Key Support

Captures and logs special keys including:

- Letters (with proper case handling based on Shift state)
- Numbers and symbols
- Special keys: `[SPACE]`, `[ENTER]`, `[BACKSPACE]`
- Email-specific characters: `@`, `.`, `-`, etc.

### Google Drive Integration

- Automatic authentication flow
- Periodic uploads every 5 minutes (configurable)
- Final upload on program termination
- Timestamped filenames for organization

## Important Notes

⚠️ **Legal Disclaimer**: This software is intended for educational and authorized testing purposes only. Always ensure you have proper authorization before monitoring any system. Unauthorized use may violate local, state, and federal laws.

⚠️ **Security**: Keep your encryption keys and Google Drive credentials secure. Anyone with access to these can decrypt your logs or access your Google Drive.

⚠️ **Privacy**: Be aware of privacy implications when logging keystrokes, especially on shared or work computers.

⚠️ **Dependencies**: The script automatically installs required packages. Ensure you have proper permissions for package installation.

## License

This project is for educational purposes only. Use responsibly and in accordance with applicable laws and regulations.
For more details, see the [LICENSE](LICENSE) file.
