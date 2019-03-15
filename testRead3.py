import pdfplumber
import re

path = '/home/iluo/桌面/pdf/30142345zfxd.pdf'
pdf = pdfplumber.open(path)

'''
思路：
对关键字列表进行循环：
  首先寻找当前关键字
  如果寻找关键字成功
    倒回去寻找最近的 上季度 和 本季度
    如果上季度离关键字更近 那么关键字对应的值是关键字之后的第二个数字
    否则 关键字对应的值是关键字之后的第一个数字
'''
keyList = ["核心偿付能力溢额", "核心偿付能力充足率", "综合偿付能力溢额", "综合偿付能力充足率", "最近一期风险综合评级", "保险业务收入", "净利润", "净资产", "认可资产","认可负债","实际资本",
           "核心一级资本","核心二级资本","附属一级资本","附属二级资本","量化风险最低资本","寿险业务保险风险最低资本","非寿险业务保险风险最低资本","保险风险最低资本","市场风险最低资本",
         "信用风险最低资本","风险分散效应","损失吸收效应","控制风险最低资本","附加资本","逆周期附加资本","国内系统重要性保险机构的附加资本","全球系统重要性保险机构的附加资本","其他附加资本",
           "最低资本","实际净现金流","个月内","年内","年以上","情景1","情景2"]
infoDict = {}
text = ""
lastTargetIndex = 0
for page in pdf.pages:
    text = text + page.extract_text()

for key in keyList:
    location = text.find(key)
    if(location != -1):
        pattern = re.compile(r'-*[\d+,*]+[.\d+]*%*')
        result = pattern.findall(text[location:location+50])
        if(len(result) > 0):
            print(key +" " + result[0])


for key in infoDict:
    print(key+" " +infoDict[key])


pdf.close()