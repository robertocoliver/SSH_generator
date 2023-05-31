import paramiko
import sys

class SSHConnection:
    def __init__(self, host, username, port):
        self.host = host
        self.username = username
        self.port = port
        self.password = password
        self.private_key_path = private_key_path
        self.client = None
 
    def connect(self, password):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.private_key_path:
                private_key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
                self.client.connect(self.host, username=self.username, port=self.port, pkey=private_key)
            else:
                self.client.connect(self.host, username=self.username, port=self.port, password=self.password)

            print("Conexão estabelecida com sucesso.")
        except Exception as error:
            print(f"Erro ao conectar via SSH: {error}")

    def execute_command(self, command):
        if self.client is None:
            print("Erro")
            return
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            for line in stdout.readlines():
                print(line.strip())
        except Exception as error:
            print(f"Erro ao executar o comando: {error}")

    def receive_file(self, remote_path, local_path):
        if self.client is None:
            print("Erro")
            return
        try:
            ftp_client = self.client.open_sftp()
            ftp_client.get(remote_path, local_path)
            ftp_client.close()
            print(f"Arquivo '{remote_path}' recebido com sucesso.")
        except Exception as error:
            print(f"Erro ao receber o arquivo: {error}")

    def send_file(self, local_path, remote_path):
        if self.client is None:
            print("Erro")
            return
        try:
            ftp_client = self.client.open_sftp()
            ftp_client.put(local_path, remote_path)
            ftp_client.close()
            print(f"Arquivo '{local_path}' enviado com sucesso.")
        except Exception as error:
            print(f"Erro ao enviar o arquivo: {error}")

    def close(self):
        if self.client is not None:
            self.client.close()
            print("Conexão SSH fechada com sucesso.")

if len(sys.argv) < 5:
    print("Uso: python3 ssh_file.py <host> <username> <port> [<password> or --key <private_key_path>]")
    sys.exit(1)

host = sys.argv[1]
username = sys.argv[2]
port = int(sys.argv[3])
password = None
private_key_path = None

if sys.argv[4] == '--key':
    private_key_path = sys.argv[5]
else:
    password = sys.argv[4]


ssh = SSHConnection(host, username, port, password=password, private_key_path=private_key_path)
ssh.connect()

while True:
    command = input('Command: ')
    if command.lower() == 'sair':
        ssh.close()
        break
    elif command.lower() == 'receive':
        remote_path = input('Remote File Path: ')
        local_path = input('Local File Path: ')
        ssh.receive_file(remote_path, local_path)
    elif command.lower() == 'send':
        local_path = input('Local File Path: ')
        remote_path = input('Remote File Path: ')
        ssh.send_file(local_path, remote_path)
    else:
        ssh.execute_command(command)
