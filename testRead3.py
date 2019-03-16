import pdfplumber
import re
import pandas as pd





def getDataFromOnePdf(pdfPath):
    path = '/home/iluo/桌面/pdf/2_301709340f43.pdf'
    pdf = pdfplumber.open(pdfPath)

    '''
    思路：
    对关键字列表进行循环：
      首先寻找当前关键字
      如果寻找关键字成功
        倒回去寻找最近的 上季度 和 本季度
        如果上季度离关键字更近 那么关键字对应的值是关键字之后的第二个数字
        否则 关键字对应的值是关键字之后的第一个数字
    '''
    keyList = ["核心偿付能力溢额", "核心偿付能力充足率", "综合偿付能力溢额", "综合偿付能力充足率", "风险综合评级", "保险业务收入", "净利润", "净资产", "认可资产", "认可负债",
               "实际资本",
               "核心一级资本", "核心二级资本", "附属一级资本", "附属二级资本", "量化风险最低资本", "寿险业务保险风险最低资本", "非寿险业务保险风险最低资本", "保险风险最低资本",
               "市场风险最低资本",
               "信用风险最低资本", "风险分散效应", "损失吸收效应", "控制风险最低资本", "附加资本", "逆周期附加资本", "国内系统重要性保险机构的附加资本", "全球系统重要性保险机构的附加资本",
               "其他附加资本",
               "最低资本", "净现金流", "个月内", "年内", "年以内", "年以上", "3到5年", "5年以上", "情景1", "情景2", "情景一", "情景二", "采取监管措施"]
    percentKeyList = ["核心偿付能力充足率", "综合偿付能力充足率", "个月内", "年内", "年以内", "年以上", "情景1", "情景2", "情景一", "情景二"]
    infoDict = {}
    text = ""
    lastTargetIndex = 0
    for page in pdf.pages:
        if(page.extract_text() != None):
            text = text + page.extract_text()

    name = re.compile(r'[\u4e00-\u9fa5]+有限公司')
    nameList = name.findall(text)
    chinese = re.compile(r'[\u4e00-\u9fa5]')

    timeStart = text.find("摘要")
    timeEnd = text.find("季度", timeStart) + 3
    time = re.compile(r'2.*年.*季度')
    timeList = time.findall(text, timeStart, timeEnd)

    company = "未知公司"
    date = "未知季度"
    if(len(nameList) > 0):
        company = nameList[0]
    if(len(timeList) > 0):
        date = timeList[0]
    yearPattern = re.compile(r'\d\d\d\d')
    yearList = yearPattern.findall(date)
    if (len(yearList) > 0):
        year = yearList[0]
        quarterPattern = re.compile(r'1|2|3|4|一|二|三|四')
        quarterList = quarterPattern.findall(date, 5)
        if (len(quarterList) > 0):
            quarter = quarterList[0]
            if (quarter == "1" or quarter == "一"):
                month = "03"
            elif (quarter == "2" or quarter == "二"):
                month = "06"
            elif (quarter == "3" or quarter == "三"):
                month = "09"
            elif (quarter == "4" or quarter == "四"):
                month = "12"
            date = (str)(yearList[0]) + "." + month

    for key in keyList:
        location = text.find(key)
        if (location != -1):
            if (key == "保险风险最低资本"):
                while (text[location - 1:location] != ' '):
                    if (text.find(key, location + 1) == -1):
                        break
                    else:
                        location = text.find(key, location + 1)
                if (location == -1):
                    break
            if (key == "实际资本" or key == "最低资本"):
                while (chinese.search(text[location - 1:location]) or text[location - 1:location] == '、'):
                    if (text.find(key, location + 1) == -1):
                        break
                    else:
                        location = text.find(key, location + 1)
                if (location == -1):
                    break
            if (key == "风险综合评级"):
                while (text.find("风险综合评级", location + 1) != -1):
                    location = text.find("风险综合评级", location + 1)

            pattern = re.compile(r'-*[\d+,*]+[.\d+]*[%]*|-')
            if (key == "风险综合评级"):
                pattern = re.compile(r'[A-Z]')
            if (key in percentKeyList):
                pattern = re.compile(r'-*\d+[.\d+]*')

            result = pattern.findall(text[location + 3:location + 50])
            if (len(result) > 0):
                start1 = 0
                start2 = 0
                while (True):
                    if (text.find("本季度", start1 + 1, location) != -1):
                        start1 = text.find("本季度", start1 + 1, location)
                    else:
                        break
                while (True):
                    if (text.find("上季度", start2 + 1, location) != -1):
                        start2 = text.find("上季度", start2 + 1, location)
                    else:
                        break
                if (start1 < start2):
                    if (len(result) >= 1):
                        # print(key +" " + result[0])
                        infoDict[key] = result[0]

                else:
                    if ((start1 - start2 > 30 and len(result) >= 1) or start1 == start2):
                        if (len(result) >= 1):
                            # print(key + " " + result[0])
                            infoDict[key] = result[0]
                    else:
                        if (len(result) >= 2):
                            # print(key +" " + result[1])
                            infoDict[key] = result[1]
            else:
                # print(key)
                infoDict[key] = "None"
        else:
            # print(key)
            infoDict[key] = "None"

    # for key in infoDict:
    #     print(key+" " +infoDict[key])

    pdf.close()

    colName = ['公司','时间', '核心偿付能力溢额（万元）', '核心偿付能力充足率（%）', '综合偿付能力溢额（万元）', '综合偿付能力充足率（%）', '最近一期风险综合评级', '保险业务收入（万元）',
               '净利润（万元）', '净资产（万元）', '认可资产（万元）', '认可负债（万元）', '实际资本（万元）',
               '核心一级资本（万元）', '核心二级资本（万元）', '附属一级资本（万元）', '附属二级资本（万元）', '量化风险最低资本（万元）', '寿险业务保险风险最低资本（万元）',
               '非寿险业务保险风险最低资本（万元）', '保险风险最低资本（万元）', '市场风险最低资本（万元）',
               '信用风险最低资本（万元）', '风险分散效应（万元）', '损失吸收效应（万元）', '控制风险最低资本（万元）', '附加资本（万元）', '逆周期附加资本（万元）',
               '国内系统重要性保险机构的附加资本（万元）', '全球系统重要性保险机构的附加资本（万元）', '其他附加资本（万元）',
               '最低资本（万元）', '实际净现金流（百万）', '未来三个月内综合流动比率（%）', '未来1年综合流动比率（%）', '未来1到3年内综合流动比率（%）', '未来3到5年综合流动比例（%）',
               '未来5年以上综合流动比率（%）', '公司整体流动性覆盖率（%）_压力情景1', '公司整体流动性覆盖率（%）_压力情景2', '报告期内公司是否被保监会采取监管措施']
    # keyList = ["核心偿付能力溢额", "核心偿付能力充足率", "综合偿付能力溢额", "综合偿付能力充足率", "风险综合评级", "保险业务收入", "净利润", "净资产", "认可资产","认可负债","实际资本",
    #            "核心一级资本","核心二级资本","附属一级资本","附属二级资本","量化风险最低资本","寿险业务保险风险最低资本","非寿险业务保险风险最低资本","保险风险最低资本","市场风险最低资本",
    #          "信用风险最低资本","风险分散效应","损失吸收效应","控制风险最低资本","附加资本","逆周期附加资本","国内系统重要性保险机构的附加资本","全球系统重要性保险机构的附加资本","其他附加资本",
    #            "最低资本","净现金流","个月内","年内","年以内","年以上","3到5年",5年以上,"情景1","情景2","情景一","情景二","采取监管措施"]

    if (infoDict["年内"] == "None"):
        keyList.remove("年内")
    else:
        if (infoDict["年以内"] == "None"):
            keyList.remove("年以内")
        else:
            if (len(infoDict["年内"]) > len(infoDict["年以内"])):
                keyList.remove("年以内")
            else:
                keyList.remove("年内")

    if (infoDict["情景1"] == "None"):
        keyList.remove("情景1")
    else:
        if (infoDict["情景一"] == "None"):
            keyList.remove("情景一")
        else:
            if (len(infoDict["情景1"]) > len(infoDict["情景一"])):
                keyList.remove("情景一")
            else:
                keyList.remove("情景1")

    if (infoDict["情景2"] == "None"):
        keyList.remove("情景2")
    else:
        if (infoDict["情景二"] == "None"):
            keyList.remove("情景二")
        else:
            if (len(infoDict["情景2"]) > len(infoDict["情景二"])):
                keyList.remove("情景二")
            else:
                keyList.remove("情景2")

    # for i in range(0,len(colName)):
    #     print(keyList[i],colName[i])

    # df = pd.DataFrame(columns= colName)
    data = []
    data.append(company)
    data.append(date)
    for key in keyList:
        data.append(infoDict[key])
    # df.loc[nameList[0]+timeList[0]] = data
    # print(df)
    # df.to_excel("text.xlsx")
    return data
