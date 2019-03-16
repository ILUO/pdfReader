import pdfplumber

path = 'C:\\Users\\Yang Xing Luo\\Desktop\\2_301709340f43.pdf'
pdf = pdfplumber.open(path)

infoDict = {}
for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    # print(page.extract_text())


    for table in page.extract_tables():
        # print(table)
        targetIndex = 0
        for row in table:
            # print(row)
            for i in range(0,len(row)):
                if((str)(row[i]).find("本季度") != -1):
                    targetIndex = i
                    nameIndex = i-1
                if(targetIndex != 0):
                    infoDict[row[nameIndex]] = row[targetIndex]

        # print('---------- 分割线 ----------')

for key in infoDict:
    print(key+" " +infoDict[key])


pdf.close()