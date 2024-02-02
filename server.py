#!/usr/bin/env python3

import asyncio
import logging
import json
import http.client
from aiohttp import web
from os import environ as env


logging.basicConfig(level=logging.DEBUG)

SETTINGS_FILE = env.get("SETTINGS", "settings.json")

class DummyHandler:
    def __init__(self, name="DummyHandler"):
        self.name = name
        self.timeout = 1

    async def handle(self, request):
        return web.Response(text=self.name)

class DummiestHandler(DummyHandler):
    message = "empty"

    def configure(self, settings):
        self.timeout = settings.get("TIMEOUT", 1)
        self.message = settings.get("MESSAGE", "dummy response")
        self.backend_host = settings.get("backend_host")
        self.backend_port = settings.get("backend_port", 80)

    async def handle(self, request):
        try:
            async with asyncio.timeout(self.timeout):
                await self.external_handler(request)
        except TimeoutError:
            web.Response(self.message, status=504)
        return web.Response(text=self.message)

    async def external_handler(self, request):
        conn = http.client.HTTPConnection(self.backend_host, port=self.backend_port)
        param = request.match_info.get("param", "default")
        conn.request("GET", f"/handler?param={param}")

    async def counter(self, request):
        conn = http.client.HTTPConnection(self.backend_host, port=self.backend_port)
        conn.request("GET", "/counter")
        res = conn.getresponse()
        if res.status != 200:
            return web.Response(text=res.reason, status=res.status)
        else:
            response = res.read().decode()
            return web.Response(text=response)


async def init():
    app = web.Application()

    # read settings
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)

    # Create handlers
    handler_one = DummyHandler("one")
    handler_two = DummiestHandler("two")
    handler_two.configure(settings)

    app.router.add_get('/one/', handler_one.handle)
    app.router.add_get('/ext/{param}', handler_two.handle)
    app.router.add_get('/last/', handler_two.counter)

    return app

if __name__ == '__main__':
    app = init()
    web.run_app(app, port=8080)
