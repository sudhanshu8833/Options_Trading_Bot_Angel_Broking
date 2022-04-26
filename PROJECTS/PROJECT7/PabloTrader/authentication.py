import os
import os.path
import sys
import requests
import time
from selenium import webdriver
from shutil import which
import urllib.parse as up

from account import CLIENT_ID, API_KEY

def authentication(client_id, redirect_uri):
    client_id = client_id + '@AMER.OAUTHAP'
    url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' + up.quote(redirect_uri) + '&client_id=' + up.quote(client_id)

    options = webdriver.ChromeOptions()

    if sys.platform == 'darwin':
        # MacOS
        if os.path.exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
            options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif os.path.exists("/Applications/Chrome.app/Contents/MacOS/Google Chrome"):
            options.binary_location = "/Applications/Chrome.app/Contents/MacOS/Google Chrome"
    elif 'linux' in sys.platform:
        # Linux
        options.binary_location = which('google-chrome') or which('chrome') or which('chromium')

    else:
        # Windows
        if os.path.exists('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'):
            options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        elif os.path.exists('C:/Program Files/Google/Chrome/Application/chrome.exe'):
            options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    chrome_driver_binary = which('chromedriver') or "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    driver.get(url)

    # Setting TDAUSER and TDAPASS environment variables enables
    # fully automated oauth2 authentication
    if 'TDAUSER' in os.environ and 'TDAPASS' in os.environ:
        ubox = driver.find_element_by_id('username')
        pbox = driver.find_element_by_id('password')
        ubox.send_keys(os.environ['TDAUSER'])
        pbox.send_keys(os.environ['TDAPASS'])
        driver.find_element_by_id('accept').click()

        driver.find_element_by_id('accept').click()
        while 1:
            try:
                code = up.unquote(driver.current_url.split('code=')[1])
                if code != '':
                    break
                else:
                    time.sleep(2)
            except (TypeError, IndexError):
                pass
    else:
        print('please finish login flow process in 120 seconds')
        i=0
        while(i<321):
            time.sleep(1)
            if i%10==0: print('Seconds remaining for token generation:',120-i)
            i+=1    
        #input('After giving access, hit enter to continue')
        try:
            code = up.unquote(driver.current_url.split('code=')[1])
        except:
            print('token code failed')
            return None
    driver.close()

    resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data={'grant_type': 'authorization_code',
                               'refresh_token': '',
                               'access_type': 'offline',
                               'code': code,
                               'client_id': client_id,
                               'redirect_uri': redirect_uri})
    if resp.status_code != 200:
        raise Exception('Could not authenticate!')
    return resp.json()


def refresh_token(refresh_token, client_id):
    resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         json={'grant_type': 'refresh_token',
                               'refresh_token': up.quote(refresh_token),
                               'client_id': up.quote(client_id)})
    if resp.status_code != 200:
        raise Exception('Could not authenticate!')
    return resp.json()


def generate_refresh_token():
    client_id = CLIENT_ID
    redirect_uri = "http://127.0.0.1"
    tokens = authentication(client_id, redirect_uri)
    if tokens is None:
        print('token generation failed')
        return None
    refresh_token = tokens['refresh_token']
    data_folder = os.path.dirname(os.path.realpath('__file__'))
    filename = "REFRESH_TOKEN"
    filepath = os.path.join(data_folder, filename)
    with open(filepath,"w") as f:
        f.write('%s' %(refresh_token))
    print('token generation success!')
    return refresh_token