#!/usr/bin/env python3

import http.client
import os
from sys import exit
import random
import string


HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 8080)

ENDPOINTS_DIRECT = ["/one/"]

ENDPOINTS_EXT = []
for _ in range(1, random.randint(4, 10)):
    ENDPOINTS_EXT.append("/ext/" + "".join(random.choices(string.ascii_lowercase, k=5)))
ENDPOINT_FINAL = ["/last/"]

ENDPOINTS = ENDPOINTS_DIRECT + ENDPOINTS_EXT + ENDPOINT_FINAL


def main():
    MAGIC = 0
    print("this is a dummy test script")
    conn = http.client.HTTPConnection(HOST, port=PORT)

    for endpoint in ENDPOINTS:
        conn.request("GET", endpoint)
        response = conn.getresponse()

        if response.status != 200:
            panic(response.reason)
        else:
            MAGIC = response.read().decode()
            print(f"endpoint: {endpoint} => OK")

    if int(MAGIC) != len(ENDPOINTS_EXT):
        panic(f"response from /counter endpoint must match the length of ENDPOINTS_EXT list, but it's {MAGIC}")

    print("Passed!")

def panic(msg):
    print(msg)
    exit(1)


if __name__ == "__main__":
    main()
