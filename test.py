import sys, random, requests, traceback,bs4
from itertools import cycle
from proxyscrape import create_collector


#INIT PROXIES
collector = create_collector('my-collector', 'http')

#get proxies
proxy_list = collector.get_proxies()
proxy_pool = cycle(proxy_list)
proxy_type = next(proxy_pool)
proxy = ':'.join([proxy_type.host,proxy_type.port])

term = 'boruto'
website= f"https://subsplease.org/xdcc/search={term}"

#COLLECT RAW DATA
raw_html = requests.get(website,proxies={"http": proxy, "https": proxy}, timeout=3)
raw_html