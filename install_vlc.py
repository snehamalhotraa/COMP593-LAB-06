
import hashlib
import os
import subprocess
import requests

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    
    response = requests.get("http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256")
    response.raise_for_status()
    expected_sha256 = response.text.strip()
    return expected_sha256
    

def download_installer():
    
    response = requests.get("http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe")
    response.raise_for_status()
    return response.content

def installer_ok(installer_data, expected_sha256):
    
    actual_sha256 = hashlib.sha256(installer_data).hexdigest()
    return actual_sha256 == expected_sha256

def save_installer(installer_data):
    
    installer_path = os.path.join(os.getenv("TEMP"), "vlc-3.0.18.4-win64.exe")
    with open(installer_path, "wb") as installer_file:
        installer_file.write(installer_data)
    return installer_path

def run_installer(installer_path):
    
    subprocess.run([installer_path, "/S", "/L=1033"], check=True)
    
def delete_installer(installer_path):
    
    if os.path.exists(installer_path):
        os.remove(installer_path)

if __name__ == '__main__':
    main()