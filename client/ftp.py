"""
CS472
Author: Neil Kanakia

Based on RFC 959: File Transfer Protocol (FTP), by J. Postel and J. Reynolds
"""

import socket
import logging

# Buffer size
BUFFER_SIZE = 8192
# Line Terminator
CRLF = "\r\n"
# Port 
PORT = 21


class FTP:
    '''
    FTP client class using the RFC 959
    '''

    def __init__(self, host, log, port=PORT):
        '''
        Constructor (init method) for FTP Client
        '''
        self.log_file = log
        logging.basicConfig(filename=self.log_file,
                                        level=logging.INFO,
                                        format='%(asctime)s  %(message)s')
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        

    def connect(self):
        '''
        Method to create connection to global host and port values
        '''
        try:
            print(f"Connecting to {self.host} at port {self.port}.\n")
            self.client = socket.create_connection((self.host, self.port))
            logging.info(f"Connecting to {self.host} at port {self.port}.\n")
            recv = (self.recv_line())
            logging.info(f"From server: {recv}")
            print(recv)
        except:
            print("Unable to connect")
            logging.error("Unable to connect to server.")


    def recv_line(self):
        ''' 
        Recieves and decodes bytes of the provided buffer size from the server
        '''
        return self.client.recv(BUFFER_SIZE).decode("ASCII")


    def send_cmd(self, cmd):
        '''
        Parse and send send a command (cmd) to the server
        For example: USER, QUIT, CWD
        '''
        cmd = cmd + CRLF
        cmd = bytes(cmd, 'ASCII')
        try:
            self.client.send(cmd)
            # print(f"From client: {cmd}")
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
                response = response.split('"')[1::2]
                response = response[0]
                print(f"Remote directory: {response}")
                logging.info(f"From server: {response}")
            else:
                logging.error("Unable to print working directory.")
        except:
            logging.error("Unable to print working directory.")


    def change_working_directory(self, path):
        '''Method to pring working directory'''
        cmd = 'CWD ' + path
        # try:
        response = self.send_cmd(cmd)
        if '250' in response:
            print(response)
        else:
            print("Unable to change directory")


    def get_syst(self):
        '''Returns the SYST message that provided the system type.'''
        cmd = 'SYST'
        try:
            response = self.send_cmd(cmd)
            print(f"From server: {response}")
            logging.info(f"From server: {response}")
        except:
            logging.error("Unable to reach server.")


    def get_help(self):
        '''Returns the HELP message that the server provides.'''
        cmd = 'HELP'
        try:
            response = self.send_cmd(cmd)
            print(f"From server: {response}")
            logging.info(f"From server: {response}")
        except:
            logging.error("Unable to reach server.")


    def make_pasv(self):
        '''
        Send PASV Command and use regular expressions to extract the host and port
        '''
        cmd = 'PASV ' 
        try:
            response = self.send_cmd(cmd)
            print(f"From server {response}")
            logging.info(f"From server {response}")
            import re
            numbers = re.compile(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', re.ASCII).search(response).groups()
            host = '.'.join(numbers[:4])
            port = (int(numbers[4]) << 8) + int(numbers[5])
            # print(host, port)
            return host, port
        except:
            logging.error("Unable to set PASV mode")


    def transfer_cmd(self, cmd):
        '''
        Create temporary PASV connection to transfer data for commands such as LIST
        '''
        host, port = self.make_pasv()
        temp_conn = socket.create_connection((host, port))
        response = self.send_cmd(cmd)
        if '150' in response:
            return temp_conn
        else: 
            print("Unable to use transfer command")
        return temp_conn


    def get_list(self, *args):
        '''
        Method to list files in directory, in long form

        The response may be such as:
        -rw-rw-rw- 1 user group 0 Feb 9 09:38 /subdirectory/file.txt
        '''
         
        cmd = 'LIST' 
        connection = self.transfer_cmd(cmd)
        f = connection.makefile('r', encoding='ASCII')

        while True:
            l = f.readline(BUFFER_SIZE)
            print(l)
            if not l:
                break
        
        connection.close()
