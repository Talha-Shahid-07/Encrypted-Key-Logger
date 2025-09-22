from cryptography.fernet import Fernet
from pathlib import Path
import os
import argparse


def decrypt_log(LOG_FILE,KEY_FILE,DECRYPTED_LOG):
    # Load the encryption key
    # Accept key as a file path or as direct text
    if os.path.isfile(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    else:
        key = KEY_FILE.encode()
    fernet = Fernet(key)
    
    # Read and decrypt the log file
    with open(LOG_FILE, "rb") as f:
        lines = f.readlines()
    
    # Write decrypted content to a new file
    # Ensure the output directory exists
    output_dir = os.path.dirname(DECRYPTED_LOG)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Write decrypted content to a new file (create if not exists)
    with open(DECRYPTED_LOG, "w") as f:
        for line in lines:
            if line.strip():  # Skip empty lines
                decrypted_line = fernet.decrypt(line.strip()).decode()
                f.write(decrypted_line)

if __name__ == "__main__":
    default_log_file = str(Path(__file__).parent / "logs" / "input_log.encrypted")
    default_output_file = str(Path(__file__).parent.parent / "main" / "logs" / "input_log_decrypted.txt")

    parser = argparse.ArgumentParser(description="Input Logger with Encryption")
    parser.add_argument("--key", type=str, required=True, help="Path to the encryption key file")
    parser.add_argument("--file", type=str, required=False, help="Path to the Encrypted File", default=default_log_file)
    parser.add_argument("--output", type=str, required=False, help="Save decrypted file to the specified path", default=default_output_file)
    args = parser.parse_args()

    # Update the KEY_FILE variable to use the provided key path
    LOG_FILE = args.file
    KEY_FILE = args.key
    DECRYPTED_LOG = args.output 

    decrypt_log(LOG_FILE,KEY_FILE,DECRYPTED_LOG)

    print(f"Decrypted log saved to {DECRYPTED_LOG}")