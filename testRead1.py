import pdfplumber

path = 'C:\\Users\\Yang Xing Luo\\Desktop\\pdf\\AXA_BALANCE_PROPERTY_INSURANCE_CO_LTD_IN_THE_FIRST_QUARTER_OF_2018_THREE_THE_SOLVENCY_REPORT.pdf'
pdf = pdfplumber.open(path)

infoDict = {}
lastTargetIndex = 0
for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    # print(page.extract_text())

    for table in page.extract_tables():
        # print(table)
        targetIndex = 0
        rowCount = 0
        for row in table:
            # print(row)
            if(rowCount == 0):
                for i in range(0,len(row)):
                    if((str)(row[i]).find("本季度") != -1):
                        targetIndex = i - len(row)
                        lastTargetIndex = targetIndex
                        nameIndex = targetIndex - 1
                        while((str)(row[nameIndex]).find("上季度") != -1 or row[nameIndex] == ''):
                            nameIndex = nameIndex - 1
                        # if(targetIndex == -1):
                        #     nameIndex = targetIndex-2
                        # else:
                        #     nameIndex = targetIndex-1
            if(targetIndex != 0):
                if(0-targetIndex < len(row)):
                    infoDict[row[nameIndex]] = row[targetIndex]
            elif(lastTargetIndex != 0):
                if(0-lastTargetIndex < len(row)):
                    infoDict[row[nameIndex]] = row[lastTargetIndex]
            rowCount = rowCount + 1
        # print('---------- 分割线 ----------')

for key in infoDict:
    print(key+" " +infoDict[key])


pdf.close()