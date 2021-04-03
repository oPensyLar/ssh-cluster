import paramiko
import os.path
import util
import app


def conn_ssh(ip, username, ssh_pass, remote_cmd):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, ssh_pass)
    stdin, stdout, stderr = s.exec_command(remote_cmd)

    stdout = stdout.readlines()
    stderr = stderr.readlines()

    str_output = ''.join(str(e) for e in stdout)
    str_err_output = ''.join(str(e) for e in stderr)

    ret = {"stdout": str_output, "stderr": str_err_output}
    s.close()
    return ret


def main():
    u = util.Util()
    a = app.App()
    creds_b64 = a.get_creds("creds.json")
    plaintext_sudo_password = u.b64_decrypt(creds_b64["sudo_password"])
    plaintext_ssh_user = u.b64_decrypt(creds_b64["ssh_user"])
    plaintext_ssh_password = u.b64_decrypt(creds_b64["ssh_password"])
    all_cmds = a.get_array_cmd("cmds.json", plaintext_sudo_password)

    # File with IPs
    serv_lst = "srv.txt"

    # Open IP file
    with open(serv_lst, "r") as f:
        text = f.readlines()

    # for-loop for IP list
    for lineHost in text:
        lineHost = lineHost.replace("\n", "")

        # Connect SSH
        print("[+]Connecting Addr::" + lineHost)

        for c_cmd in all_cmds:
            ret = conn_ssh(lineHost, plaintext_ssh_user, plaintext_ssh_password, c_cmd)

            with open("log.log", "a") as fp:
                all_output = ret["stdout"] + ret["stderr"]
                fp.write(all_output)
                fp.close()

        print("SOC Output Results")


main()
