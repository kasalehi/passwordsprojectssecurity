import requests
import hashlib
import sys

def api_request(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response

def leak_func(hashes, real_hash):
    hash_lines = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hash_lines:
        if h == real_hash:
            return int(count)
    return 0

def hash_func(password):
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5, tail = hashed_password[:5], hashed_password[5:]
    response = api_request(first_5)
    if response:
        return leak_func(response, tail)
    return 0

def main(args):
    for password in args:
        count = hash_func(password)
        if count > 0:
            print(f"Password '{password}' has been leaked {count} times.")
        else:
            print(f"Password '{password}' has not been leaked.")

if __name__ == '__main__':
    main(sys.argv[1:])
