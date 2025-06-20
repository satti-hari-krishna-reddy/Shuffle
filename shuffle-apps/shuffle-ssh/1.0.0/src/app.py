import paramiko
from io import StringIO
from walkoff_app_sdk.app_base import AppBase 
import traceback

class SSHApp(AppBase):
    __version__ = "1.0.0"
    app_name = "shuffle-ssh"  

    def __init__(self, redis, logger, console_logger=None):
        super().__init__(redis, logger, console_logger)

    def run_ssh_command(self, host, port, user_name, private_key_file_id, password, command):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        port = int(port) if port else 22

        if private_key_file_id:
            try:
                new_file = self.get_file(private_key_file_id)
                key_data = new_file["data"].decode()
                private_key_file = StringIO()
                private_key_file.write(key_data)
                private_key_file.seek(0)
                private_key = paramiko.RSAKey.from_private_key(private_key_file)
                ssh_client.connect(hostname=host, username=user_name, port=port, pkey=private_key)

            except Exception as e:
                return {
                    "success": "false",
                    "message": f"Private key auth failed: {str(e)}",
                    "traceback": traceback.format_exc()
                }

        else:
            try:
                ssh_client.connect(hostname=host, username=user_name, port=port, password=str(password))
            except Exception as e:
                return {
                    "success": "false",
                    "message": f"Password auth failed: {str(e)}",
                    "traceback": traceback.format_exc()
                }

        try:
            stdin, stdout, stderr = ssh_client.exec_command(str(command))

            try:
                output = stdout.read().decode(errors='ignore')
            except Exception as e:
                output = f"Failed to read stdout: {e}"

            try:
                errorLog = stderr.read().decode(errors='ignore')
            except Exception as e:
                errorLog = f"Failed to read stderr: {e}"

        except Exception as e:
            return {
                "success": "false",
                "message": f"Command execution failed: {str(e)}",
                "traceback": traceback.format_exc()
            }

        return {
            "success": "true",
            "output": output,
            "error_logs": errorLog
        }

if __name__ == "__main__":
    SSHApp.run()
