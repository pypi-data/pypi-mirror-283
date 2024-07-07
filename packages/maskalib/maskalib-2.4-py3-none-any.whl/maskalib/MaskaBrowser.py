import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random

def fetch_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            proxies = response.text.strip().split('\r\n')
            return proxies
        else:
            raise Exception(f"Failed to fetch proxies. Status code: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch proxies: {str(e)}")

def check_proxy(proxy):
    try:
        proxies = {
            'http': proxy,
            'https': proxy
        }
        response = requests.get('https://www.google.com', proxies=proxies, timeout=10)
        if response.status_code == 200:
            # Check response time to ensure proxy is fast enough
            response_time = response.elapsed.total_seconds()
            if response_time <= 5:  # Accept proxies with response time less than or equal to 5 seconds
                print(f"Proxy {proxy} is working! Response time: {response_time:.2f} seconds")
                return True
            else:
                print(f"Proxy {proxy} responded too slow (Response time: {response_time:.2f} seconds)")
                return False
        else:
            print(f"Proxy {proxy} is not responding correctly (Status code: {response.status_code})")
            return False
    except requests.RequestException as e:
        print(f"Proxy {proxy} failed with exception: {str(e)}")
        return False

def main():
    try:
        proxies = fetch_proxies()
        random.shuffle(proxies)  # Shuffle the list of proxies
        for proxy in proxies:
            if check_proxy(proxy):
                break
        else:
            raise Exception("No fast working proxy found.")

        proxy_host, proxy_port = proxy.split(':')[-2], proxy.split(':')[-1]
        
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument(f"--proxy-server={proxy_host}:{proxy_port}")

        driver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)

        try:
            driver.get("https://www.google.com")
            
            # Optionally perform actions on Google here
            
            input("Press Enter to close the browser...")
        finally:
            driver.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def MaskaBrowser():
    main()
    
