
# Neil Kanakia

Feb 14th, 2022
CS472: hw3

# Questions

## Do you think that someone could hack into your FTP server? Why or why not? Through what methods?

Yes, an FTP server is easy to hack since it transfers all its data in plain text and is unencrypted, anyone could use a packet sniffer
such as wireshark and be able to read the username and password and gain access to the server.

## EXTRA CREDIT: Critique how FTP solves the problem of file transfer – what is good? What is bad? What is weird?

FTP solves the problem of sending files easily but is not easy to use, due to its nature of having a connection/command channel
and a separate channel to transfer data.

# Setup

Run 'make' file in command line

## Activate the venv

source venv/bin/activate

## Run script

python3 main.py log1.txt 2121 auth.txt

## Change host IP

In order to change HOST IP, change the first variable on line 10 in main.py

## To change the username / pass

Add new usernames and passwords to auth.txt separated by a single space.
example_username example_password
