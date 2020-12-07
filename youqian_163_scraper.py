from datetime import datetime
import requests
import pandas as pd
import json
import time

'''
作者：Coegle18
链接：https://github.com/Coegle/youqian_163_scraper
创建时间：2020/11/11
'''

'''
使用说明
- 使用之前请全局搜索"请修改此个人数据"，按照以下要求进行修改：
    cookies: 请在 qian.163.com 登录后找到以下 cookies 并且依次填入
    URL: 将 cookies 中的 TOKEN 字段复制填写到相应部分
- 在使用之前请按照需要修改以下几个参数：（可以参考已经填写的参数进行修改）
    file_name: 导出的文件名（若不存在将创建）
    start_time: 账单开始的时间
    end_time: 账单结束的时间
    bills_type: 账单的类型，有 TRANSFER INCOME OUTGO 三中类型，分别表示转账记录、收入和支出情况，请按照需要修改此参数以获得不同的账单明细，如果需要全部导出，则需要分别执行三次，得到三个 csv 文件
- 输出的 csv 文件编码格式为 utf-8，如果打开乱码请转换为 gb2312
- 详细说明请见 README.md
- 使用过程中如果有问题欢迎发邮件：coegle18[AT]gmail.com（将 [AT] 替换为 @）
'''
cookies = {"SERVER_ID": "请修改此个人数据",
           "TOKEN": "请修改此个人数据",
           "mail_client_uuid": "请修改此个人数据",
           "NTES_OSESS": "请修改此个人数据",
           "S_OINFO": "请修改此个人数据",
           "P_OINFO": "请修改此个人数据"
           }
url = "https://qian.163.com/pc/xhr/data/bill/list.do?token=请修改此个人数据（和 cookies 中的 TOKEN 值相同）"
file_name = 'youqian_out.csv'
start_time = datetime(2017, 1, 1)
end_time = datetime(2020, 12, 7)
bills_type = "OUTGO"    # TRANSFER INCOME OUTGO
# 需要修改的参数到此结束


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.183 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
}


# 获取订单词典
def get_bills_dict(response):
    single_layer_bills = []
    bill_dicts = json.loads(response.text)["data"]["result"]
    for each_bill_dict in bill_dicts:
        single_layer_bills.append(get_single_layer_bills(each_bill_dict))
    return single_layer_bills


# 将单条 Json 账单记录抽离成字典
def get_single_layer_bills(multilayer_dict_data):
    print(multilayer_dict_data)
    id = multilayer_dict_data["id"]
    category = multilayer_dict_data["category"]["categoryName"]
    if multilayer_dict_data["subCategory"] is not None:
        sub_category = multilayer_dict_data["subCategory"]["categoryName"]
    else:
        sub_category = ""
    if multilayer_dict_data["outMoney"] is not None:
        out_money = multilayer_dict_data["outMoney"][1:]
    else:
        out_money = multilayer_dict_data["outMoney"]
    out_money_type = multilayer_dict_data["outMoneyType"]
    out_fund_id = multilayer_dict_data["outFundId"]
    out_fund = multilayer_dict_data["outFund"]
    if multilayer_dict_data["inMoney"] is not None:
        in_money = multilayer_dict_data["inMoney"][1:]
    else:
        in_money = multilayer_dict_data["inMoney"]
    in_money_type = multilayer_dict_data["inMoneyType"]
    in_fund_id = multilayer_dict_data["inFundId"]
    in_fund = multilayer_dict_data["inFund"]
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(multilayer_dict_data["date"] / 1000.0))
    source = multilayer_dict_data["source"]
    remark = multilayer_dict_data["remark"]
    trade_type = multilayer_dict_data["tradeType"]
    refund = multilayer_dict_data["refund"]
    ebank_imported = multilayer_dict_data["ebankImported"]
    imported = multilayer_dict_data["imported"]
    loan_fund_id = multilayer_dict_data["loanFundId"]
    refund_item_ids = multilayer_dict_data["refundItemIds"]
    out_create_type = multilayer_dict_data["outCreateType"]
    in_create_type = multilayer_dict_data["inCreateType"]
    book_id = multilayer_dict_data["bookId"]
    book_name = multilayer_dict_data["bookName"]
    editable = multilayer_dict_data["editable"]
    return {
        "id": id,
        "category": category,
        "subCategory": sub_category,
        "outMoney": out_money,
        "outMoneyType": out_money_type,
        "outFundId": out_fund_id,
        "outFund": out_fund,
        "inMoney": in_money,
        "inMoneyType": in_money_type,
        "inFundId": in_fund_id,
        "inFund": in_fund,
        "date": date,
        "source": source,
        "remark": remark,
        "tradeType": trade_type,
        "refund": refund,
        "ebankImported": ebank_imported,
        "imported": imported,
        "loanFundId": loan_fund_id,
        "refundItemIds": refund_item_ids,
        "outCreateType": out_create_type,
        "inCreateType": in_create_type,
        "bookId": book_id,
        "bookName": book_name,
        "editable": editable
    }


# 保存结果
def save_bills(bills, i):
    data = pd.DataFrame(bills)
    try:
        if i == 0:
            csv_headers = ["id", "category", "subCategory", "outMoney", "outMoneyType", "outFundId", "outFund",
                           "inMoney", "inMoneyType", "inFundId", "inFund", "date", "source", "remark", "tradeType",
                           "refund", "ebankImported", "imported", "loanFundId", "refundItemIds", "outCreateType",
                           "inCreateType", "bookId", "bookName", "editable"]
            data.to_csv(file_name, header=csv_headers, index=False, mode='a+', encoding='utf-8')
        else:
            data.to_csv(file_name, header=False, index=False, mode='a+', encoding='utf-8')
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")


# 获取翻页时需要 post 的数据
def get_params_to_page(page, trade_type):
    return {
        "tradeType": trade_type,
        "startTime": start_time.timestamp() * 1000,
        "endTime": end_time.timestamp() * 1000,
        "categoryId": "",
        "parentId": "",
        "outFund": "",
        "inFund": "",
        "fund": "",
        "page": page,
        "size": 20,
        "totalPage": 0,
        "total": 0
    }


# 获取全局的信息：总账单数量和总页数
def get_params_of_all(trade_type):
    params = get_params_to_page(0, trade_type)
    response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(params))
    total_page = json.loads(response.text)["data"]["pagination"]["totalPage"]
    total = json.loads(response.text)["data"]["pagination"]["total"]
    return total_page, total


# 获取账单
def get_bills(trade_type):
    (total_page, total) = get_params_of_all(trade_type)
    print("共 %d 页，%d 条数据，三秒钟之后开始读取" % (total_page, total))
    time.sleep(3)
    for i in range(0, total_page):
        if i % 10 == 0:
            time.sleep(1)
        params = get_params_to_page(i, trade_type)
        print("page%d" % i)
        response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(params))
        save_bills(get_bills_dict(response), i)


get_bills(bills_type)
