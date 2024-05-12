#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import requests


def main():
    gitUrl = "https://api.github.com/users/bdastur/repos?per_page=100"

    data = requests.get(gitUrl)
    jdata = json.loads(data.text)
    print(jdata)
    # parse dict.
    cloneUrls = []
    for urlInfo in jdata:
        print(urlInfo["clone_url"])
        cloneUrls.append(urlInfo["clone_url"])


if __name__ == '__main__':
    main()
