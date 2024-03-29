from urllib import request
from bs4 import BeautifulSoup
import re
import pymysql
import time

fundSharesList = []

db =pymysql.connect(
    host = '127.0.0.1',  
    port =3306,
    user = 'root',
    password = '109036',
    db = 'fund',
    charset = 'utf8'      
)

head={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

find = {
    1:re.compile(r'html">(.*?)</a></td>'),
    2:re.compile(r'html">(.*?)</a></td>'),
    6:re.compile(r'">(.*?)</td>'),
    7:re.compile(r'">(.*?)</td>'),
    8:re.compile(r'">(.*?)</td>')
}

def handle (a):
    flag = False
    for i in range(0,len(fundSharesList)):
        if a[0] == fundSharesList[i][0]:
            fundSharesList[i][2] = round(float(fundSharesList[i][2]) + float(a[4]),2)
            flag =True
            break
    if not flag:
        new = [a[0],a[1],a[4]]
        fundSharesList.append(new)


if __name__=="__main__":  
    funds = []
    fundNum = 0
    errorNum = 0
    send = request.Request("http://fund.eastmoney.com/js/fundcode_search.js",headers = head)
    response = request.urlopen(send)
    js = response.read().decode('utf-8')
    js = js[11:len(js)-3].split("],[")
    for i in range(0,len(js)):
        fund = str(js[i]).replace('"','')
        fund = fund.split(",")
        funds.append(fund)

    while fundNum < len(funds):
        fund_id = funds[fundNum][0]
        print(fund_id + " " + funds[fundNum][2])
        try:
            url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=" + str(fund_id) + "&topline=10&year=2020&month=&rt=0.21822537857648627"
            send = request.Request(url,headers = head)
            response = request.urlopen(send, timeout=10)
            html = response.read().decode('utf-8')
            bs =BeautifulSoup(html,"html.parser")

            find_list = bs.find_all("tbody")
            tr = find_list[0].find_all("tr")

            for i in tr:
                td = i.find_all("td")
                fundShares = []
                for j in range(0,len(td)):
                    if j in [1,2,6,7,8]:
                        a = re.findall(find[j],str(td[j]))[0]
                        if j ==8 :
                            a = str(a).replace(",","")
                            if(len(a)>8):
                                time.sleep(6)
                        fundShares.append(a)
                handle(fundShares)
            print()
            errorNum = 0

        except Exception as e:
            print(fund_id + " 获取失败")
            print(e)
            if str(e) =="timed out" and errorNum <= 3:
                print("第" + str(errorNum) + "次超时，重试")
                errorNum = errorNum + 1
                fundNum = fundNum - 1
            print()

        fundNum = fundNum + 1
        # if fundNum == 1000:
        #     break 

        
#以下进行Dao层操作Begin>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor() 
    try:
        for insert in fundSharesList:
            sql = "INSERT INTO fundShares VALUES ('"+ str(insert[0]) +"', '" + str(insert[1]) +"', " + str(insert[2]) + ");"
            print(sql)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
    except Exception as e:
        # 回滚
        db.rollback()
        raise Exception("插入数据库错误！", e)
    # 关闭数据库连接
    db.close()
#以下进行Dao层操作End>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    '''
    更新日期
    20210204 V1.0 初版
    20210211 V1.1 从网页获取JS文件
    '''
