"""
CS472
Author: Neil Kanakia

Based on RFC 959: File Transfer Protocol (FTP), by J. Postel and J. Reynolds
FTP Library
"""

import socket
import logging

BUFFER_SIZE = 1024
PORT = 21

# Line Terminator
CRLF = "\r\n"

class FTP:
    '''
    FTP client class using the RFC 959
    '''
    BUFFER_SIZE = 1024
    PORT = 21

    # Line Terminator
    CRLF = "\r\n"

    def __init__(self, host, log, port=PORT):
        '''
        Constructor (init method) for FTP Client
        '''
        logging.basicConfig(filename=log,
                                        level=logging.INFO,
                                        format='%(asctime)s  %(message)s')
        self.host = host
        self.log_file = log
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host:
            self.host = host
            logging.info(f"Connecting to {host} at port {port}.")
            self.connect(port)
        

    def set_pasv(self):
        '''
        Use method to set PASV(Passive) or PORT(Port)
        '''
        

    def connect(self, port=PORT):
        '''
        Method to connect the gloval variable s to host at provided port number
        '''
        try:
            self.client.connect((self.host, port))
            print(f"Connected to {self.host} at port {port}.\n")
            recv = (self.recv_line())
            logging.info(f"From server: {recv}")
        except:
            print("Unable to connect")
            logging.error("Unable to connect to server.")


    def recv_line(self):
        ''' 
        Recieves and decodes bytes of the provided buffer size from the server
        '''
        return self.client.recv(BUFFER_SIZE).decode("ASCII")

    def recv_multiline(self):
        '''
        Get a multi-line respnse from the server (which may be larger than the default buffer size 

        '''

    def send_cmd(self, cmd):
        '''
        Parse and send send a command (cmd) to the server
        For example: USER, QUIT, CWD
        '''
        cmd = cmd + CRLF
        cmd = bytes(cmd, 'ASCII')
        try:
            self.client.send(cmd)
            print(f"From client: {cmd}")
            logging.info(f"From client: {cmd}")
            return (self.recv_line())
        except:
            logging.warning("Unable to send command to server.")
        

    def login(self, username='', passwd=''):
        '''
        Method to log into the server.
        If no login is passed, by default, 
        the username is set to anonymous.
        '''
        if not username:
            username = 'anonymous'
        if not passwd:
            passwd = ''
        username = 'USER ' + username
        passwd = 'PASS ' + passwd
        response = self.send_cmd(username)
        if response[:3] == '331':
            try:
                response = self.send_cmd(passwd)
                logging.info(f"From server: {response}")
            except:
                logging.error("Incorrect password")
        return response
    

    def close(self):
        '''Close socket connection to server'''
        resp = self.send_cmd("QUIT")
        print(resp)
        self.client.close()
        logging.info(f"From server: {resp}")
        logging.info(f"Closed connection to server.")

    
    def working_directory(self):
        '''Method to pring working directory'''
        cmd = 'PWD ' 
        try:
            response = self.send_cmd(cmd)
            if response[:3] == '257':
                print(f"From server: {response}")
                logging.info(f"From server: {response}")
            else:
                logging.error("Unable to print working directory.")
        except:
            logging.error("Unable to print working directory.")


    def get_help(self):
        '''Returns the HELP message that the server provides.'''
        cmd = 'HELP'
        try:
            response = self.send_cmd(cmd)
            print(f"From server: {response}")
            logging.info(f"From server: {response}")
        except:
            logging.error("Unable to reach server.")


    def list(self, *args):
        '''
        Method to list files in directory, in long form

        The response may be such as:
        -rw-rw-rw- 1 user group 0 Feb 9 09:38 /subdirectory/file.txt
        '''
         
        cmd = 'LIST' 
        try:
            response = self.send_cmd(cmd)
            # if response[:3] == '257':
            print(f"From server: {response}")
            logging.info(f"From server: {response}")
            # else:
            #     logging.error("Unable to print working directory.")
        except:
            logging.error("Unable to print working directory.")
