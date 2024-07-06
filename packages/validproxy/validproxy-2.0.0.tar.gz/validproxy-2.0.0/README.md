# validproxy 2.0.0

`validproxy` is a robust and efficient Python package designed to streamline the process of validating proxy servers. It supports multiple proxy types including HTTP, HTTPS, SOCKS4, and SOCKS5. This package is ideal for developers who need to ensure that only valid proxies are used in their applications, enhancing reliability and performance.

## Features

- **Multiple Proxy Support:** Validate HTTP, HTTPS, SOCKS4, and SOCKS5 proxies.
- **File Handling:** Easily read proxies from a file.
- **Validation and Storage:** Validate proxies and save the valid ones to a separate file.
- **Simple Interface:** Easy to integrate and use within your existing projects.

### Benefits

- Efficiency : Quickly validate large lists of proxies.
- Automation : Easily integrate proxy validation into automated workflows and scripts.
- Reliability : Ensure only valid proxies are used, improving the reliability of your applications.

## Installation

You can install `validproxy` using pip:

```bash
pip install validproxy
```

## Usage

### Example 1: Check Proxies from a File Without Saving

This example demonstrates how to read a list of proxies from a file, check their validity, and print the results.

```python
from validproxy import validproxy

def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def main():
    proxy_list = "proxy.txt"
    proxies = read_proxies_from_file(proxy_list)

    valid_proxies = []

    for proxy in proxies:
        if validproxy(proxy):
            print(f'Valid proxy: {proxy}')
            valid_proxies.append(proxy)
        else:
            print(f'Invalid proxy: {proxy}')

if __name__ == "__main__":
    main()
```

### Explanation
- `read_proxies_from_file(file_path)` : Reads proxies from the specified file.
- `validproxy(proxy)` : Checks if the given proxy is valid.
- **Main Logic** : Iterates through the list of proxies, validates each, and prints the result.

### Example 2: Check Proxies from a File and Save Valid Proxies
This example extends the previous one by also saving the valid proxies to a separate file.

```python
from validproxy import validproxy

def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def save_valid_proxies(file_path, valid_proxies):
    with open(file_path, 'w') as file:
        for proxy in valid_proxies:
            file.write(f"{proxy}\n")

def main():
    proxy_list = "proxy.txt"
    valid_proxy_save = "valid_proxy.txt"
    proxies = read_proxies_from_file(proxy_list)

    valid_proxies = []

    for proxy in proxies:
        if validproxy(proxy):
            print(f'Valid proxy: {proxy}')
            valid_proxies.append(proxy)
        else:
            print(f'Invalid proxy: {proxy}')

    save_valid_proxies(valid_proxy_save, valid_proxies)

if __name__ == "__main__":
    main()
```
### Explanation
- `save_valid_proxies(file_path, valid_proxies)` : Saves the list of valid proxies to the specified file.
- **Main Logic** : Reads proxies, validates them, prints the results, and saves valid proxies.
  
### Example 3: Check a Single Proxy

This example shows how to validate a single proxy.

```python
from validproxy import validproxy

proxy = "http://102.38.31.8:9999"

if validproxy(proxy):
    print(f'Valid proxy: {proxy}')
else:
    print(f'Invalid proxy: {proxy}')
```
### Explanation

- Single Proxy Check : Simply validates a single proxy and prints whether it's valid or not.
  
### Thanks
- Thank you for using `validproxy`. Your support and feedback are greatly appreciated. If you find this package helpful, please consider contributing, providing feedback, or simply spreading the word. Together, we can make proxy validation easier and more efficient for everyone.
