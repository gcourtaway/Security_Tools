#!/use/bin/env python

import requests


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1] # split string into groups by the /
    #executes while file is open
    with open(file_name, "wb") as out_file: #open file for writing, but its binary
        out_file.write(get_response.content)

download("")
