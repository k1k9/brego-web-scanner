#!/usr/bin/env python3
import os
import logging
import argparse
from datetime import date

import src.wordpress as wordpress
import src.utility as utility

# Setting up argument parser
parser = argparse.ArgumentParser(
    prog = "Brego - Web Scanner",
    description="Web scanner detects avaliable paths and wordpress plugins."
)
parser.add_argument(
    "-u",
    "--url",
    required=True,
    metavar='HOST',
    help="Full link or hostname"
)
parser.add_argument(
    '--dev',
    action="store_true",
    help="Entry developer mode to improve log reading"
)
parser.add_argument(
    "-w",
    "--wordlist",
    metavar="Path",
    help="Wordlist of possible paths"
)
parser.add_argument(
    "-p",
    "--port",
    metavar="INT",
    help="Specific port for testing application"
)
args = parser.parse_args()



# Setting up logs 
LOGFILE = f"{os.getcwd()}/logs/{str(date.today()).replace('-','')}.log"
# Create folder if not exists
if not os.path.exists(f"{os.getcwd()}/logs"):
    os.mkdir(f"{os.getcwd()}/logs")
# If developer mode remove old logfile
if args.dev:
    if os.path.isfile(LOGFILE):
        os.remove(LOGFILE)


# Setting up logger
LOGGERFMT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    filename=LOGFILE,
    encoding="utf-8",
    filemode="a+",
    level=logging.DEBUG,
    format=LOGGERFMT
)
logger = logging.getLogger('BregoMain')
# Console Hanlder
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(ch)

if __name__ == "__main__":
    wp = wordpress.Wordpress(args.url)
    u = utility.Utility()
    u.run(args.url, wordlist=args.wordlist)
