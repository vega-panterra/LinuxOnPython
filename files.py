import paramiko


def upload_files(host, user, password, local_path, remote_path, port=22):
    print(f'Load files {local_path} in {remote_path}')
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_files(host, user, password, local_path, remote_path, port=22):
    print(f'Load files {local_path} in {remote_path}')
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()
