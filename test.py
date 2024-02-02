#!/usr/bin/env python3

import http.client
import os
from sys import exit


HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 8080)

ENDPOINTS_DIRECT = ["/one/"]
ENDPOINTS_EXT = [
    "/ext/foo",
    "/ext/bar",
    "/ext/adhd"
]
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
