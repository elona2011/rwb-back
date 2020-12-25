import requests

headers = {
    'Host': 'u.zrb.net',
    'Origin': 'http://u.zrb.net',
    'Referer': 'http://u.zrb.net/user/userindex',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

sessionLogin = requests.Session()
sessionLogin.headers.update(headers)