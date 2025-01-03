README
Inside this folder there are 4 files. Those files are:
	1) wsl_download.bat
	2) wsl_startup.bat
	3) setup_key_for_ssh.sh
	4) ssh_startup.sh
- Document (1) downloads Windows Subsystem for Linux (wsl). You will only need to run this once, ever. If you run it again then it will open you machine as a Linux VM and you'll need to drop back down into Windows. To do this, run the command "exit"
- Document (2) is what you will execute in Windows every time. This will prompt you asking if you have set up your SSH key. If you have already, type "yes" and hit enter. If you have not, type "N" and hit enter and you will be prompted to set up the key.
	--> if the user enters some variation of "yes", this program will execute document (4) and pass it the username of the windows user. This username should be the O365 username of the user. This username will be used to build the SSH connection in document (4).
	--> if the user enters anything other that a variation of "yes", this program will execute document (3) then document (4) passing it the username of the user. Document (3) serves to build and export the key pair to support password-less logins for the Linux machine.
- Document (3) is what sets up your key to log into the Linux machine. The purpose of the key is to create a "fingerprint" so that you do not have to input your password every time. Follow the instructions and prompts very closely and read everything. You should only have to do this once.
	--> Document (3) will build the key pair for password-less SSHs. It will build the /.ssh directory if it is not already present and then cd into it. It will then generate the key pair using the <ssh-gen> function and save the key as the user defined name. It will then add the private key to the authorized user list using the <ssh-add> function and copy the public key to the Linux machine using <ssh-copy-id> function with <-i> as its flag.
- Document (4) is where you SSH into the Linux machine and you can begin to access it.
	--> This program accepts the username and sets the IP address to our Linux machine. It will cd into the /.ssh directory and add the existing private key to the authorized user list and copy the public key onto the machine. This is redundant if you have not made the key but is necessary if you already have generated the key pair. It will the execute a SSH request with the -XY tag.

Notes:
- If you need to change the IP address, go into the files and update the local variables with the name <IP>