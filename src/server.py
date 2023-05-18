#!/usr/bin/env python
import logging
import requests as r

from src.functions import test_connection, pick_user_agent


class Server:
    def __init__(self, url):
        self.URL = url
        self.logger = logging.getLogger("BregoMain")
        if not test_connection(self.URL): exit(1)
        self.logger.debug("Server init")
        self._loop()

    def _loop(self) -> bool:
        self._check_server_informations()
        return True
    
    def _check_server_informations(self):
        self.logger.info("\nChecking server informations")
        self.logger.info("-"*30)
        rsp = r.options(self.URL, headers={
            "User-Agent": pick_user_agent()})
        try: self.logger.info(f"Server: {rsp.headers.get('Server')}")
        except: pass
        try: self.logger.info(f"Version: {rsp.headers.get('X-Powered-By')}")
        except: pass

        try:
            rsp = r.options(self.URL, headers={"User-Agent": pick_user_agent()})
            if rsp.headers.get('Allow'):
                mth = rsp.headers.get('Allow')
            else: mth = rsp.headers.get('Access-Control-Allow-Methods')
            self.logger.info(f"Avaliable methods: {mth}")
        except: pass


        