#!/usr/bin/env python3
import re
import json
import requests
import logging
from os import getcwd
from random import randint
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup as bs
from .functions import pick_user_agent


class Utility:
    """Other web scanner techniques independent of the framework used"""
    def __init__(self,  url, wordlist = None):
        self.logger = logging.getLogger("BregoMain")
        self.URL = url
        self.WORDLIST = wordlist
        self._loop()

    def _loop(self):
        self.dirBuster()

    def dirBuster(self):
        if not self.WORDLIST: return False
        with open(self.WORDLIST, 'r') as wl:
            lines = [l.rstrip() for l in wl] 
            detected = []
            avaliable = []

            for l in lines:
                resp = requests.head(f"{self.URL}/{l}")
            
                # Detected paths
                if resp.status_code == 200 or resp.status_code == 301:
                    avaliable.append((f"{resp.url}",f"{resp.status_code}"))
                elif resp.status_code < 400 and resp.status_code >= 500:
                    detected.append((f"{resp.url}",f"{resp.status_code}"))
            
        # Print out results
        if ((len(avaliable) > 0) or (len(detected) > 0)):
            self.logger.info(f"\nFinded paths: {len(detected) + len(avaliable)}")
        if (len(avaliable) > 0):
            self.logger.info(f"Avaliable: {len(avaliable)}")
            for i in avaliable:
                print(f"[{avaliable[i][1]}]\t{avaliable[i][0]}")

        if (len(detected) > 0):
            self.logger.info(f"Detected: {len(detected)}")
            for i in detected:
                print(f"[{detected[i][1]}]\t{detected[i][0]}")