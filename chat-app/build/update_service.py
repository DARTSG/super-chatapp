import paramiko
import socket
import os
from pathlib import Path

# Constants
SERVER_IP = '5.6.6.6'
USERNAME = 'student'
PASSWORD = 'password123'
UPDATE_TIMEOUT = 3

def get_remote_file_path():
    if os.name == 'nt':  # Windows
        return '/tmp/updates/chatapp_update.exe'
    else:  # macOS or Linux
        return '/tmp/updates/chatapp_update'

def get_local_file_path():
    if os.name == 'nt':  # Windows
        local_dir = Path("C:/temp")
    else:  # macOS or Linux
        local_dir = Path.home() / "temp"
    
    local_dir.mkdir(parents=True, exist_ok=True)
    return local_dir / "chatapp_update.exe"

def check_for_updates(status_callback):
    remote_file_path = get_remote_file_path()
    local_file_path = get_local_file_path()
    transport = None
    sftp = None

    try:
        status_callback("Connecting to update server...")
        
        # Use a socket to establish a connection with a timeout
        sock = socket.create_connection((SERVER_IP, 22), timeout=UPDATE_TIMEOUT)
        transport = paramiko.Transport(sock)
        
        transport.start_client(timeout=UPDATE_TIMEOUT)
        transport.auth_password(username=USERNAME, password=PASSWORD)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get_channel().settimeout(UPDATE_TIMEOUT)
        
        status_callback("Downloading update...")
        sftp.get(remote_file_path, str(local_file_path))
        status_callback("Update downloaded successfully")

        return str(local_file_path)
    except (socket.timeout, paramiko.SSHException, paramiko.AuthenticationException) as e:
        status_callback("Failed to check for updates: {}".format(e))
        return None
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
