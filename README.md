
# Multi SFTP/SSH uploader

This is simple, upload files and execute commands  multiple uploads over multiple SSH/SFTP servers.



### Notes

- Python3 (Anaconda works)
- for Windows test need you install Visual Studio Build tools (paramiko package requeriment)
- Add your IP/hostname to srv.txt
- This does not save logs so you must redirect stdin



## How It Works


First, generate base64 string password

![Generate Base64 string](/img/base64-tool.png "Generate Base64 string").

Replace ** line 90 ** change **cGFzc3dvcmQ=** to **you-base64-string-output**




Change password & login

```python
usr = "you-user"
```



## Need to upload files?

Easy, drop files over `file_uploads`



## Need to change the path where your files will be uploaded?

By default, all files save over tmp, you can change this...

```python
remote_folder = "/tmp/"
```




## Need to change change cmds?

```python
array_cmds = [
    'chmod +x /tmp/xagtSetup-32.30.12.run',
    'echo ' + pwd + '| sudo -S sh /tmp/xagtSetup-32.30.12.run',
    'echo ' + pwd + '| sudo -S /opt/fireeye/bin/xagt -i /tmp/agent_config.json',
    'echo ' + pwd + '| sudo -S service xagt start',
    'echo ' + pwd + '| sudo -S service xagt status'
]
```


## Dependencies 

- paramiko