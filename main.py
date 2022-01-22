"""
CS472
Author: Neil Kanakia

Main client application to run FTP Library
"""
import pyfiglet
from ftp import FTP

HOST_NAME = "10.246.251.93"
LOG_FILE = "log1.txt"
USER_NAME = "cs472"
PASSWORD = "hw2ftp"
PORT = 21


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
                "View files in server: ls\n"\
                "Print working directory: pwd\n"\
                "Close connection: logout\n"\
                "Quit application: quit\n"\
                "_____________________________________________________"

        print(str1)
        usr_input = get_input_string().lower().split(' ')
        cmd = usr_input[0]

        if cmd == 'login':
            print("Enter username:")
            user_name = get_input_string()
            print("Enter password:")
            passwd = get_input_string()
            response = my_ftp.login(user_name, passwd)
            print(response)
        if cmd == 'help':
            my_ftp.get_help()
        if cmd == 'ls':
            my_ftp.list()
        if cmd == 'pwd':
            my_ftp.working_directory()
        if cmd == 'logout':
            my_ftp.close()
        elif cmd == 'quit':
            break
           

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
    print("Enter hostname: ")
    # TODO: Temporary, change to get input from user
    # host_name = get_input_string()
    # log_file = get_input_string()
    # my_ftp = FTP(host_name, log_file)

    ftp_obj = FTP(HOST_NAME, LOG_FILE)

    # Get login information
    print("Enter username (Leave empty to login anonymously):")

    # TODO: Temporary, change to get input from user
    # user_name = get_input_string()
    user_name = USER_NAME
    print("Enter password:")

    # TODO: Temporary, change to get input from user
    # passwd = get_input_string()
    passwd = PASSWORD
    response = ftp_obj.login(user_name, passwd)
    print(response)
    
    menu(my_ftp=ftp_obj)


if __name__=="__main__":
    main()
