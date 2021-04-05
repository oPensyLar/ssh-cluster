import paramiko
import time
import os
from socket import gaierror
import glob
import util
import app

def sftp_upload_file(host, port, user, passwd, local_file, remote_file):
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.put(local_file, remote_file)
    sftp.close()
    transport.close()


def ssh_loop(host, prt, usr, pwd, cmd):
    repeat = True

    while repeat:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        time.sleep(1)

        try:
            client.connect(host, port=prt, username=usr, password=pwd)

        except gaierror:
            print("[!] gaierror")
            continue

        except ConnectionError:
            print("[!] ConnectionError")
            continue

        except TimeoutError:
            print("[!] TimeoutError")
            continue

        except EOFError:
            print("[!] ERROR")
            continue

        except paramiko.ssh_exception.AuthenticationException:
            print("[!] ERROR")
            continue

        except paramiko.ssh_exception.NoValidConnectionsError:
            print("[!] ERROR")
            continue

        try:
            stdin, stdout, stderr = client.exec_command(cmd)

        except ConnectionResetError:
            print("[!] exec_command() ERROR")
            continue

        except paramiko.ssh_exception.SSHException:
            print("[!] SSHException ERROR")
            continue

        stdout = stdout.readlines()
        stderr = stderr.readlines()
        # stdin = stdin.readlines()
        client.close()

        # print(stdin)

        str_output = ''.join(str(e) for e in stdout)
        str_err_output = ''.join(str(e) for e in stderr)
        print()

        return {"stdout": str_output, "stderr": str_err_output}

        # print(stdout)
        # print(stderr)
        repeat = False


a = app.App()
utils = util.Util()
remote_folder = "/tmp/"
ssh_port = 22
creds_b64 = a.get_creds("creds.json")
usr = utils.b64_decrypt(creds_b64["ssh_user"])
pwd = utils.b64_decrypt(creds_b64["ssh_password"])
plaintext_sudo_password = utils.b64_decrypt(creds_b64["ssh_password"])
upload = True

array_cmds = a.get_array_cmd("cmds.json", plaintext_sudo_password)

with open("srv.txt") as fp:
    lines = fp.readlines()

    for c_line_hst in lines:

        if upload is True:
            # Get local all files
            upload_files = glob.glob("files_uploads/*")
            for c_file in upload_files:
                file_name = os.path.basename(c_file)
                remote_file_path = remote_folder + file_name

                # Upload recursive
                print("[+] Uploading " + c_file + " to " + remote_file_path + " on " + c_line_hst)
                sftp_upload_file(c_line_hst, ssh_port, usr, pwd, c_file, remote_file_path)

        for c_cmd in array_cmds:
            # Execute cmds over Host
            str_out = None

            if c_cmd.find("sudo") > 0x0:
                str_out = "[+] Executing sudo cmd"

            else:
                str_out = "[+] Executing '" + c_cmd + "' over '" + c_line_hst + "'"

            print(str_out)
            output = ssh_loop(c_line_hst, ssh_port, usr, pwd, c_cmd)

            with open("log.log", "a", encoding="utf-8") as fp:
                all_output = output["stdout"] + output["stderr"]
                fp.write(all_output)
                fp.close()

        # Create host folder (save logs per host)
        if os.path.exists(c_line_hst) is False:
            os.mkdir(c_line_hst)