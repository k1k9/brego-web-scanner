#!/usr/bin/env python3
import re
import json
import requests
import logging
from os import getcwd
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup as bs
from .functions import pick_user_agent, test_connection


class Wordpress:
    def __init__(self, url):
        self.logger = logging.getLogger("BregoMain")
        self.URL = url
        try: self.run()
        except: exit(1)

    def run(self):
        if not test_connection(self.URL): exit(1)
        if not self._detect_wordpress():
            self.logger.info("This site doesn't use wordpress!")
            return False
        self._plugins_information()
        self._user_enumeration()


    def _detect_wordpress(self):
        """Simple script wich main goal to detect wordpress site based on
        site source code and avaliable paths. This isn't a full wordpress scan"""
        resp = requests.get(self.URL, headers={
                            "User-Agent": pick_user_agent()})
        detected = False

        if resp.status_code == 200:
            _content = resp.content.decode()
            # Search for wordpress signs in source code
            self.logger.debug("Searching for wordpress sings in source code")
            with open(f"{getcwd()}/config/wpsigns.json", 'r') as f:
                wpsigns = json.load(f)["inCode"]
            for sign in wpsigns:
                if sign in _content:
                    detected = True

            # Perform url detection
            if not detected:
                self.logger.debug("Searching for wordpress sings via paths")
                with open(f"{getcwd()}/config/wpsigns.json", 'r') as f:
                    wpsigns = json.load(f)["urlCheck"]
                for i, (k, v) in enumerate(wpsigns.items()):
                    _resp = requests.get(
                        f"{self.URL}/{k}", headers={"User-Agent": pick_user_agent()})
                    _content = _resp.content.decode()

                    if v in _content:
                        detected = True

            # Gathering info from feed
            try:
                _resp = requests.get(
                    f"{self.URL}/feed", headers={"User-Agent": pick_user_agent()})
                tree = et.fromstring(_resp.content.decode())
                tree = tree.find("channel")
                _lastBD = tree.find('lastBuildDate').text
                _ver = tree.find('generator').text.replace(
                    "https://wordpress.org/?v=", "")
                # Output
                self.logger.info(f"Informations from /feed path")
                self.logger.info("-"*30)
                self.logger.info(f"[*] Version: {_ver}")
                self.logger.info(f"[*] Last build date: {_lastBD}\n")
            except:
                # Get version from source if feed doesn't work
                soup = bs(_content, 'html.parser').find_all(
                    'meta', attrs={'name': 'generator'})
                _ver = f"Detected {soup}" if len(soup) else "Can't get wordpress version\n"
                self.logger.info(f"[*] {_ver}")
            
        else:
            raise ValueError('Cannot access to this URL')
        return True if detected else False

    def _plugins_information(self):
        """Informations about used plugins"""
        resp = requests.get(f"{self.URL}/wp-json",
                            headers={"User-Agent": pick_user_agent()}, allow_redirects=False)

        if resp.status_code != 200:
            return False

        plugins = json.loads(resp.content.decode())["namespaces"]

        if len(plugins) > 0:
            self.logger.info(f"\nDetected plugins: {len(plugins)}")
            self.logger.info("-"*30)
            for i in plugins:
                self.logger.info(f"[*] {i}")
        return True

    def _user_enumeration(self):
        """Finding users by enumerating a author parameter"""
        users = []
        for i in range(1, 15):
            resp = requests.get(f"{self.URL}/?author={i}",
                                headers={"User-Agent": pick_user_agent()})
            if resp.status_code == 200:
                soup = bs(resp.content.decode(), 'html.parser')
                user = soup.findAll("h1", {"class": "entry-title"})
                if len(user) > 0:
                    user = re.search(
                        "entry-title.*<span>(.*)</span>", str(user[0])).group(1)
                    users.append(user)
                else:
                    user = soup.findAll("h1", {"class":"wp-block-query-title"})
                    if len(user) > 0:
                        user = re.search(
                        "wp-block-query-title.*<span>(.*)</span>", str(user[0])).group(1)
                        users.append(user)


        if users:
            self.logger.info(f"\nDetected users")
            self.logger.info("-"*30)
            for i in users:
                self.logger.info(f"[*] {i}")
            return True
        else:
            return False
