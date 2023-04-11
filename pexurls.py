from bs4 import BeautifulSoup
import time
import os
import re
import sys
import requests
import random
import subprocess

import asyncio
import aiohttp
import aiofiles
import multiprocessing

import pex
import subprocess
from bs4 import BeautifulSoup
pexurls_file = "someurls.txt" 
default_starting_point = 11500
default_end_ing_point = 90218
# import threading
import asyncio
willdlforumpost = True
urlspumped = 5
#howmanyfetches = 10
howmanyfetches = 5
semaphore_num = 5
url_get_maxretries = 5 * howmanyfetches

print('THE ULTIMATE PinoyExchange Scraper')

def checkifempty_url(url):
    # Define regular expression pattern
    pattern = r'^((http(s)?://)?(www.)?pinoyexchange.com/)?discussion/(\d+)(/)?$'

    # Use re.match() to search for pattern in url
    match = re.match(pattern, url)

    # Check if a match was found
    if match:
        return True
    return False    

def pex_geturlid(url):
    match = re.search(r"^(?:(?:http(s)?://)?(?:www.)?pinoyexchange.com/)?discussion/(?P<id>\d+)(/)?$", url)
    if match:
        return int(match.group("id"))
    else:
        return None

if len(sys.argv) > 0+1:
    stt_ = int(sys.argv[1])
else:
    stt_ = default_starting_point
if len(sys.argv) > 1+1:
    end_ = int(sys.argv[2])
else:
    end_ = default_end_ing_point
print("STARTING")

uris = []

import aiohttp
import aiofiles
import asyncio
from bs4 import BeautifulSoup

async def get_link_next(url):
    _default_url = f'https://www.pinoyexchange.com/discussion/{pex_geturlid(url)+1}/'
    try:
        response = await pex.fetch(url)
    except:
        print(f"[err] def get_link_next({url}), couldn't seem to LOAD url, check conn if ok")
        return _default_url
    
    if response == 404 or isinstance(response, int):
        return _default_url
    elif response is not None:
        # Parse the HTML content using BeautifulSoup
        
        try:
            soup = BeautifulSoup(response, "html.parser")
        except:            
            print(f"[err] def get_link_next({url}), couldn't seem to PARSE url, you may check url if valid HTML")
            return _default_url
        
        # Find the <link> tag with "prev" relationship
        prev_link = soup.find("link", rel="prev")

        # Extract the URL of the previous page
        if prev_link:
            prev_url = prev_link.get("href")
            # print("Previous URL:", prev_url)
            return prev_url

        else:            
            canon_link = soup.find("link", rel="canonical")
            if canon_link:
                    return canon_link.get("href")
    return _default_url


async def append_to_file(file_path, text):
    async with aiofiles.open(file_path, "a") as file:
        await file.write(text)
async def stt_as(start_=10000, end_=911218):
    di_id = start_
    tasks = []
    print(f"INIT DL SEQ {start_}-{end_}")
    while int(di_id) <= int(end_):
        # create multiple tasks for each url
        for i in range(urlspumped+1):
            url = f'https://www.pinoyexchange.com/discussion/{di_id}'
            
            print(di_id)
            print(f"LOADING {url}")
            curlink_task = asyncio.create_task(get_link_next(url))
            tasks.append(curlink_task)
            di_id += 1
            # break the loop if reached the end
            if di_id > end_:
                break
        curlinks = await asyncio.gather(*tasks)
        async with aiofiles.open(pexurls_file, "a") as f:
            for curlink in curlinks:
                if curlink and not checkifempty_url(curlink) and curlink != "https://www.pinoyexchange.com/entry/signin":
                    print(curlink)
                    # await f.write(text)
                    await f.write(f"\n{curlink}")
                    if willdlforumpost:
                        
                        delay = random.randint(500, 2000) / 1000.0
                        await asyncio.sleep(delay)
                        try:
                            await pex.pex_fetch_allpages(curlink)
                        except:
                            print(f"[err] can't FETCH the url. This may happen the fileid is 'False' which could mean the URL is invalid. C'est la vie. URL: {curlink}")
        tasks.clear()


def start(strt=10000, end_=911218):
    asyncio.run(stt_as(stt_,end_))

if __name__ == '__main__':
    print()
    start(stt_,end_)
