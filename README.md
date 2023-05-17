# Brego Project
Web application scanner designed by @k1k9 used only for education purpose in controlled environment

## 📌 Setting up
```
pip install -r requirements.txt
```

## 🪅 Running
```sh 
python main.py -h
```
```sh
usage: Brego - Web Scanner [-h] -u HOST [--dev] [-w Path] [-p INT]

Web scanner detects avaliable paths and wordpress plugins.

options:
  -h, --help            show this help message and exit
  -u HOST, --url HOST   Full link or hostname
  --dev                 Entry developer mode to improve log reading
  -w Path, --wordlist Path
                        Wordlist of possible paths
  -p INT, --port INT    Specific port for testing application
```

## 👀 Features
I want make this script full automated and gathering information about used technology on scanned website, check known vulnerabilities, server information, allowed methods. Tasks:

🥷 **Wordpress**
- [*] Detect wordpress version (By meta tag or /feed)
- [*] Enumerating users
- [ ] Checks avaliables paths such as wp-admin
- [ ] Checks wp-cron
- [*] Detects used plugins
- [ ] Check xmlrpc.php

🥷 **Server**
- [ ] Server name
- [ ] Server version
- [ ] Avaliable HTTP methods

🥷 **Domain**
- [ ] Creation date
- [ ] Updated date
- [ ] Expiration date
- [ ] Registrar

🥷 **ToDo**
- [ ] Error handling (when domain isnt avaliable)