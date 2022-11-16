"""
Neil Kanakia
CS472: Hw3
Feb 14th, 2022 
"""


HOST_IP = "127.0.0.1"

from ftp import FTPServer


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Specify logfile and port number to run FTP server")
    parser.add_argument('logfile', metavar='logfile', type=str, help='Enter logfile')
    parser.add_argument('portnumber', metavar='portnumber', type=int, help='Enter port number')
    parser.add_argument('authfile', metavar='authfile', type=str, 
                        help="Enter authfile which contains username and password", 
                        default='auth.txt')
    args = parser.parse_args()
    return args.portnumber, args.logfile, args.authfile


def main():
    port_number, log_file, auth_file = parse_args()
    address = (HOST_IP, port_number) 
    my_ftp = FTPServer(address, log_file, auth_file)
    print("Running FTP Server")
    my_ftp.serve()


if __name__ == "__main__":
    main()