"""
CS472
Author: Neil Kanakia

Main client application to run FTP Library
"""
import pyfiglet
import sys
from ftp import FTP


def get_input_int():
    '''
    Method to safely input an integer
    '''
    try:
        return int(input())
    except ValueError:
        print("Invalid input. Please enter an int")
        return get_input_int()


def menu(my_ftp):
    '''
    Main menu to call other functions
    '''

    while True:
        str1 = "_____________________________________________________\n"\
                "Login to server: login\n"\
                "Get help: help\n"\
                "Get system info: syst\n"\
                "View files in server: ls\n"\
                "Print working directory: pwd\n"\
                "Change working directory: cwd + 'path'\n"\
                "Close connection: logout\n"\
                "Quit application: quit\n"\
                "_____________________________________________________"

        usr_input = get_input_string().lower().split(' ')
        cmd = usr_input[0]
        if cmd == 'cwd':
            my_ftp.change_working_directory(usr_input[-1])
        if cmd == 'help':
            print(str1)
            my_ftp.get_help()
        if cmd == 'login':
            login()
        if cmd == 'ls':
            my_ftp.get_list()
        if cmd == 'pwd':
            my_ftp.working_directory()
        if cmd == 'pasv':
            my_ftp.make_pasv()
        if cmd == 'syst':
            my_ftp.get_syst()
        if cmd == 'logout' or cmd == 'quit':
            my_ftp.close()
            break
           
def login(my_ftp):
    print("Enter username (Leave blank if anonymous):")
    user_name = get_input_string()
    print("Enter password (Leave blank if not required):")
    passwd = get_input_string()
    response = my_ftp.login(user_name, passwd)
    print(response)


def get_input():
    '''
    Returns a tuple with hostname, filename
    '''
    print("Enter the server host: ")
    hostname = input()
    print("\nEnter log filename: ")
    log_file = input()
    return hostname, log_file


def get_input_string():
    '''
    Method to safely input a string
    '''
    try:
        return str(input())
    except ValueError:
        print("Invalid input. Enter a valid input: ")
        return get_input_string()


def main():
    '''
    Main function to execute the program
    '''
 
    welcome_message = pyfiglet.figlet_format("FTP client", font="digital")
    print(welcome_message)
    args = sys.argv
    arg_len = len(args)
    if(arg_len > 3):
        print("Hostname and logfile arguments must be passed.")
        sys.exit(0)

    host_name, port = '', 0
    if(arg_len == 4):
        port = args[-1]
        log_file = args[-2]
        host_name = args[-3]
    if(arg_len == 3):
        port = 21
        log_file = args[-1]
        host_name = args[-2]
    
    ftp_obj = FTP(host_name, log_file, port)
    login(ftp_obj)
    menu(my_ftp=ftp_obj)


if __name__=="__main__":
    main()
