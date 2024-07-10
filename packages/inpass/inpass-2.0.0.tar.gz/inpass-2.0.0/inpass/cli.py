import argparse
import inpass
import os
import sys
import signal

def signal_handler(sig, frame):
    sys.exit(0) 
    
def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description="Login to Instagram and track URL changes.")
    parser.add_argument('--username', required=True, help="Your Instagram username")
    parser.add_argument('--password-file', required=True, help="File containing passwords to try")
    
    args = parser.parse_args()
    
    inpass.track_url_change(args.username, args.password_file)

if __name__ == '__main__':
    main()
