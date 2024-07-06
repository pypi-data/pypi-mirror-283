import requests

def validproxy(proxy):
    try:
        proxies = {
            "http": proxy,
            "https": proxy,
            "socks4": proxy,
            "socks5": proxy,
        }
        response = requests.get("http://www.google.com", proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False

def save_valid_proxies(valid_proxies, file_path):
    with open(file_path, 'w') as file:
        for proxy in valid_proxies:
            file.write(proxy + '\n')
