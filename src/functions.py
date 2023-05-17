#!/usr/bin/env python3
import json
from os import getcwd
from random import randint

def display_motd():
    print("  ____   _____   ______  _____   ____  \n |  _ \ |  __ \ |  ____|/ ____| / __ \ \n | |_) || |__) || |__  | |  __ | |  | |\n |  _ < |  _  / |  __| | | |_ || |  | |\n | |_) || | \ \ | |____| |__| || |__| |\n |____/ |_|  \_\|______|\_____| \____/ ")
    print("\n")

def pick_user_agent():
        """Pick random user agent for request"""
        with open(f"{getcwd()}/config/useragents.json", 'r') as f:
            _userAgents = json.load(f)['0']
        return _userAgents[randint(0, len(_userAgents)-1)]