# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# from selenium import webdriver
# from selenium.webdriver.common.proxy import Proxy, ProxyType
# import time

# # change 'ip:port' with your proxy's ip and port
# proxy_ip_port = 'gw.proxy.rainproxy.io:5959'

# proxy = Proxy()
# proxy.proxy_type = ProxyType.MANUAL
# proxy.http_proxy = proxy_ip_port
# proxy.ssl_proxy = proxy_ip_port

# capabilities = webdriver.DesiredCapabilities.CHROME
# proxy.add_to_capabilities(capabilities)

# # replace 'your_absolute_path' with your chrome binary absolute path
# driver = webdriver.Chrome('/Users/sudhanshu/Desktop/algo-trading/PROJECTS/PROJECT27/chromedriver', desired_capabilities=capabilities)

# driver.get('https://www.dextools.io/app/bsc/pair-explorer/0x7143a91c45c411e204f3ab24a63298cfacc4e3ff')

# time.sleep(80)

# driver.quit()


# %%
# from seleniumwire import webdriver
# import time
# options = {
#     'proxy': {
#         'http': 'http://jbnryWjniB-cc-any-sid-85357661:NTb6ynwi@gw.proxy.rainproxy.io:5959', 
#         'https': 'https://jbnryWjniB-cc-any-sid-85357661:NTb6ynwi@gw.proxy.rainproxy.io:5959', 
#         'no_proxy': 'localhost,127.0.0.1' # excludes
#     }
# }
# browser = webdriver.Chrome('/Users/sudhanshu/Desktop/algo-trading/PROJECTS/PROJECT27/chromedriver', seleniumwire_options=options)
# browser.get('https://whatismyipaddress.com')


# %%
# from selenium import webdriver
import time
from seleniumwire import webdriver
import pandas as pd
df=pd.read_csv('proxy.csv')

for i in range(len(df)-1):
    try:
        tick=df['PROXY'][i]
        ticks=tick.split(':')
        value=str(ticks[2])+':'+str(ticks[3])+'@'+str(ticks[0])+':'+str(ticks[1])
        options = {
            'proxy': {
                'http': 'http://'+str(value), 
                'https': 'https://'+str(value), 
                'no_proxy': 'localhost,127.0.0.1' # excludes
            }
        }
        print(value)
        driver = webdriver.Chrome('/Users/sudhanshu/Desktop/algo-trading/PROJECTS/PROJECT27/chromedriver', seleniumwire_options=options)

        driver.get('https://www.dextools.io/app/bsc/pair-explorer/0x7143a91c45c411e204f3ab24a63298cfacc4e3ff')
        time.sleep(1)
        try:
            button = driver.find_element_by_xpath('/html/body/app-root/div[2]/div/main/app-exchange/div/app-pairexplorer/app-layout/div/div/div[2]/div[2]/ul/li[1]/span/button')
            button.click()
        except:
            button = driver.find_element_by_xpath('/html/body/app-root/div[2]/div/main/app-exchange/div/app-pairexplorer/app-layout/div/div/div[2]/div[2]/ul/li[1]/a')
            button.click()

        time.sleep(1)
        button2=driver.find_element_by_xpath('/html/body/app-root/div[2]/div/main/app-exchange/div/app-pairexplorer/app-layout/div/div/div[2]/div[2]/ul/li[1]/button[3]/i')
        button2.click()

        time.sleep(1)
        button3=driver.find_element_by_xpath('/html/body/app-root/div[2]/div/main/app-exchange/div/app-pairexplorer/app-layout/div/div/div[2]/div[2]/ul/li[1]/button[2]/i')
        button3.click()

        time.sleep(1)
        button4=driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/app-social-media-modal/div[2]/div/a[3]')
        button4.click()
        time.sleep(3)
        driver.quit()

        if i==len(df)-1:
            i=0


    except:
        pass


# %%
# # {'IP Address': '72.47.152.224', 'Port': '55443', 'Code': 'US', 'Country': 'United States', 'Anonymity': 'elite proxy', 'Google': 'no', 'Https': 'yes', 'Last Checked': '22 secs ago'}
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from splinter import Browser
# from selenium import webdriver
# PROXY = '23.107.176.100:32180'
# webdriver.DesiredCapabilities.CHROME['proxy']={
#     "httpProxy":PROXY,
#     "ftpProxy":PROXY,
#     "sslProxy":PROXY,
#     "proxyType":"MANUAL",
    
# }
# executable_path={'executable_path':'/Users/sudhanshu/Desktop/algo-trading/PROJECTS/PROJECT27/chromedriver'}
# driver=Browser('chrome',**executable_path,headless=False)
# driver.visit('https://www.dextools.io/app/bsc/pair-explorer/0x7143a91c45c411e204f3ab24a63298cfacc4e3ff')
# # driver.find_by_id('ng-tns-c115-5 btn btn-trade btn-icon-absolute ml-2 pancakeswap ng-star-inserted').first.click()
# driver.find_by_tag('button').first.click()


# %%
# from selenium import webdriver

# PROXY = "23.107.176.100:32180" # IP:PORT or HOST:PORT

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)

# chrome = webdriver.Chrome(options=chrome_options)
# chrome.get("https://www.dextools.io/app/bsc/pair-explorer/0x7143a91c45c411e204f3ab24a63298cfacc4e3ff")


# %%
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


# %%
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list


# %%
# options = webdriver.ChromeOptions()


# %%
# options.add_argument('--proxy-server=190.7.158.58:39871')


# %%
# driver = webdriver.Chrome(options=options, executable_path=r'/Users/sudhanshu/Desktop/algo-trading/PROJECTS/PROJECT27/chromedriver')


# %%
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import chromedriver_autoinstaller # pip install chromedriver-autoinstaller

# chromedriver_autoinstaller.install() # To update your chromedriver automatically
# driver = webdriver.Chrome()

# # Get free proxies for rotating
# def get_free_proxies(driver):
#     driver.get('https://sslproxies.org')

#     table = driver.find_element(By.TAG_NAME, 'table')
#     thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
#     tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

#     headers = []
#     for th in thead:
#         headers.append(th.text.strip())

#     proxies = []
#     for tr in tbody:
#         proxy_data = {}
#         tds = tr.find_elements(By.TAG_NAME, 'td')
#         for i in range(len(headers)):
#             proxy_data[headers[i]] = tds[i].text.strip()
#         proxies.append(proxy_data)

#     return proxies


# free_proxies = get_free_proxies(driver)


# %%
# from selenium import webdriver
# PROXY = "119.93.235.205:41731"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome = webdriver.Chrome(chrome_options=chrome_options)
# chrome.get("https://www.google.com")


# %%
# from selenium import webdriver
# PROXY = "103.208.200.115:23500"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome = webdriver.Chrome(chrome_options = chrome_options, executable_path=r'/Users/sudhanshu/Desktop/algo-trading/PROJECTS/PROJECT27/chromedriver')
# chrome.get("https://whatismyipaddress.com")


