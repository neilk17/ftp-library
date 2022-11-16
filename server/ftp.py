"""
FTP Server 
Author: Neil Kanakia
"""
from dataclasses import dataclass
import logging, os
import time
from socket import socket, AF_INET, SOCK_STREAM

CWD = os.getcwd()
BUFFER_SIZE = 1024
CRLF = "\r\n"
ENCODING = 'utf-8'

class FTPServer:
    '''
    FTP client class using the RFC 959
    '''

    def __init__(self, address, log, auth_file=None):
        '''
        Constructor (init method) for FTP server

        address     is a tuple with (host, port)
        log         is the name of a file log file 
        username    is an optinal argument for a username
        password    is an optinal argument for a password
        '''
        self.username, self.password = [], []
        self.set_auth(auth_file)
        self.welcome_message = "220 Welcome!"
        self.user_message = "331 Please specify the password."
        self.list_message = "150 File status okay; Here comes the directory Listing."
        self.login_invalid_message = "530 Login incorrect."
        self.login_success_message = "230 Login sucessful."
        self.quit_message = "221 Goodbye."

        self.syst_message = "215 UNIX Type: L8" # Always set to UNIX
        self.feat_message = "211 Feature List"
        self.port_message = "200 Recieved."
        self.eprt_message = "200 Recieved."

        self.data_socket = None
        self.working_dir = CWD

        # Logging
        self.log_file = log
        logging.basicConfig(filename=self.log_file,level=logging.INFO,format='%(asctime)s  %(message)s')

        # Creating initial socket
        self.host, self.port = address
        self.sock = socket(AF_INET, SOCK_STREAM) # Command socket
        self.bind()
    
    def set_auth(self, authfile):
        '''Sets username and password from the authentication file. 
        '''
        f = open(authfile, "r")
        for line in f:
            data = (line.strip().split(' '))
            self.username.append(data[0])
            self.password.append(data[1])


    def listen(self):
        self.sock = socket(AF_INET, SOCK_STREAM) # Command socket
        self.bind()
        self.sock.listen(5)
        print(f"Listening for connection at {self.sock}")
        logging.info(f"Listening for connection at {self.sock}")
        self.accept()
        self.welcome()

    def serve(self):
        '''Serve method'''
        self.listen()
        while True:
            self.recv = self.recv_data()
            cmd = self.recv[0]
            if cmd == 'QUIT':
                self.QUIT()
                self.close()
                self.listen()
            else:
                evaluation_format = f"self.{self.recv[0]}()"
                try:
                    eval(evaluation_format)
                except AttributeError as e:
                    print(f"This feature has not been implemented in this server")



    def bind(self):
        '''Method to bind the socket to address provided on initialization'''
        logging.info(f"Created connection with {self.host} at port {self.port}")
        self.sock.bind((self.host, self.port)) 
    

    def accept(self):
        ''' Method to accept socket after listening'''
        self.conn, self.addr = self.sock.accept()
        print(f"Connected at : {self.conn}\nAddr: {self.addr}")
        logging.info(f"Connected at : {self.conn}\nAddr: {self.addr}")
    
        
    def recv_data(self):
        while True:
            cmd = self.conn.recv(256)
            try:
                cmd = cmd.decode(ENCODING)
            except UnicodeDecodeError as e:
                print(cmd)
                print(e)
                
            if not cmd:
                break
            else:
                cmd = cmd.split()
                print(f"Recieved from client: {cmd}")
                logging.info(f"Recieved from client: {cmd}")
                return cmd


    def send_response(self, resp):
        '''Method to send response to client using command channel'''
        self.conn.send(bytes(resp+CRLF, ENCODING))
        print(f"Sent from server: {resp}")
        logging.info(f"Sent from Server: {resp}")


    def start_data_port(self):
        if self.ispasv:
            self.data_socket, addr = self.passive_sock.accept()
            print(f"Connected at: {self.data_socket}\nAddr: {addr}")
            logging.info(f"Connected at: {self.data_socket}\nAddr: {addr}")
            return

        # In case of Active connection
        self.data_socket= socket(AF_INET, SOCK_STREAM)
        print(f"Created {self.data_socket}")
        self.data_socket.connect((self.data_address, self.data_port))
        print(f"Connected at: {self.data_address} Addr: {self.data_port}")
        logging.info(f"Connected at: {self.data_address} Addr: {self.data_port}")


    def push_data_port(self,data):
        ''' Push data through data channel'''
        
        if type(data) != bytes:
            data = bytes(data+CRLF, ENCODING)

        self.data_socket.send(data)


    def close_data_port(self):
        '''Close data port'''
        logging.info(f"Closing data socket: {self.data_socket}")
        self.data_socket.close()
        self.data_socket = None


    def welcome(self):
        '''welcome function'''
        self.send_response(self.welcome_message)
    

    def USER(self):
        '''User function'''
        self.correct_user = (self.recv[-1] in self.username)
        self.send_response(self.user_message)


    def PASS(self):
        '''Password function'''
        if not(self.password) and not(self.username):
            self.send_response(self.login_success_message) 
            return
        
        if not(self.password):
            self.send_response(self.login_success_message) 
            return

        self.correct_pass = self.recv[-1] in self.password
        if not(self.correct_user):
            self.send_response(self.login_invalid_message)
            return
        elif not(self.correct_pass):
            self.send_response(self.login_invalid_message)
        else:
            self.send_response(self.login_success_message) 
   
    
    def TYPE(self):
        '''Type '''
        self.type = self.recv[-1] 
        print(self.type)
        self.type_message = "200 Type Success"
        self.send_response(self.type_message)
        

    def SYST(self):
        '''System function'''
        self.send_response(self.syst_message)
        

    def FEAT(self):
        '''FEAT function to return features of this FTP server'''
        self.send_response(self.feat_message)


    def PWD(self):
        '''PWD function'''
        pwd_success = f"257 \"{self.working_dir}\" is the current working directory"
        print(pwd_success)
        self.send_response(pwd_success)
    

    def CWD(self, up=False):
        '''CWD function'''
        if not up:
            new_dir = self.recv[-1]
        else:
            new_dir = ".."

        if not(os.path.isfile(new_dir)):
            self.send_response("500 file does not exist")


        try:
            os.chdir(new_dir)
            self.working_dir = new_dir
            cwd_sucess = f"250 Directory sucessfully changed to {os.getcwd()}"
            self.send_response(cwd_sucess)
            logging.info(cwd_sucess)
        except:
            print("Unable to change dir")
    

    def CDUP(self):
        ''' CWD to parent directory'''
        self.CWD(up=True)

    
    def LIST(self):
        '''List function '''
        self.send_response(self.list_message)

        listing = os.listdir('.')
        listing.sort()
        self.start_data_port()        
        for item in listing:
            stats = os.stat(item)
            d = os.path.isdir(item) and 'd' or '-'
            mode = ''
            for i in range(9):
                    mode+=((stats.st_mode>>(8-i))&1) and 'rwxrwxrwx'[i] or '-'
            ftime= time.strftime(' %b %d %H:%M ', time.gmtime(stats.st_mtime))
            output = "{} {:10} {} {}".format(d+mode, stats.st_size, ftime, os.path.basename(item))
            self.push_data_port(output)
        self.close_data_port()

        self.list_complete_message = "226 Directory Send OK." 
        self.send_response(self.list_complete_message)

    
    def RETR(self):
        ''' RETR file'''
        file_name = self.recv[-1]
        self.retr_message = f"150 Opening binary mode for {file_name}"
        self.send_response(self.retr_message)

        f = open(file_name, 'rb')  
        self.start_data_port()
        while True:
            line = f.read(BUFFER_SIZE)
            while line:
                self.push_data_port(line)
                line = f.read(BUFFER_SIZE)
            if not line:
                f.close()
                self.close_data_port()
                break
        
        self.send_response("226 Transfer complete.")
    

    def get_from_dataport(self):
        '''Get from data port'''
        if not self.data_socket:
            print("Data socket not created")
            return
        
        data = ''
        while True:
            l = self.data_socket.recv(BUFFER_SIZE)
            if not l:
                break
            else:
                data += l.decode(ENCODING)

        return data


    def STOR(self):
        ''' STOR file '''
        file_path = self.recv[-1]
        self.stor_message = "150 Ok to send data."
        self.send_response(self.stor_message)

        f = open(file_path, 'w')
        self.start_data_port()

        data = self.get_from_dataport()
        f.write(data)
        f.close()

        self.close_data_port()

        self.stor_complete = "226 Transfer complete."
        self.send_response(self.stor_complete)
            

    def EPRT(self):
        self.ispasv = False
        position_of_address = self.recv.index('EPRT')+1
        recieved = self.recv[position_of_address][1:-1].split('|')
        print(recieved)
        self.data_address= recieved[1]
        self.data_port = int(recieved[-1])
        logging.info(f"Address: {self.data_address}\nPort: {self.data_port}")
        self.send_response(self.port_message)
        # self.data_socket= socket(AF_INET, SOCK_STREAM)
        # self.data_socket.connect((self.data_adddress, self.data_port))


    def PASV(self):
        '''PASV function to set to Passive Mode'''

        if self.data_socket is not None:
            self.close_data_port()

        self.ispasv = True
        self.passive_sock = socket(AF_INET, SOCK_STREAM) 
        self.passive_sock.bind((self.sock.getsockname()[0], 0))
        port = self.passive_sock.getsockname()[-1]

        self.pasv_message = f"227 Entering Passive Mode (|||{port}|)"
        self.send_response(self.pasv_message)
        logging.info(self.pasv_message)


        print(f"Listening for connection at {self.passive_sock}")
        logging.info(f"Listening for connection at {self.passive_sock}")
        self.passive_sock.listen(5)


    def EPSV(self):
        '''EPSV function to set to Extended Passive Mode'''
        if self.data_socket is not None:
            self.close_data_port()

        self.ispasv = True
        self.passive_sock = socket(AF_INET, SOCK_STREAM) 
        self.passive_sock.bind((self.sock.getsockname()[0], 0))
        port = self.passive_sock.getsockname()[-1]
        
        self.epsv_message = f"229 Entering Extended Passive Mode (|||{port}|)"

        self.send_response(self.epsv_message)
        logging.info(self.epsv_message)
        print(self.epsv_message)

        print(f"Listening for connection at {self.passive_sock}")
        logging.info(f"Listening for connection at {self.passive_sock}")
        self.passive_sock.listen(5)


    def PORT(self):
        self.ispasv = False
        recieved = self.recv[-1].split(',')
        print(recieved)
        self.data_address = '.'.join(recieved[:4])
        self.data_port = (int(recieved[4])<<8)+int(recieved[5])
        self.send_response(self.port_message)


    def QUIT(self):
        '''Quit function'''
        self.send_response(self.quit_message)
        # self.close()


    def close(self):
        '''Method to close the socket connection'''
        self.sock.close()
