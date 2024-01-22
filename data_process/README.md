## 代码环境
The code has been tested running under Python 3.9.12. The required packages are as follows:

- numpy == 1.23.5
- pandas == 2.0.3
- openpyxl == 3.1.2

### 文本情绪分类模型
SA.py  

输入：评论列表，类型list  

输出：列表中情感占比的最大项，及其所占比例

### 被动反馈数据
数据输入为beishi文件夹下面的数据  

1.运行excel_process.py对被动反馈数据进行数据清洗、对数转化、归一化操作，生成resource.xlsx文件
```
python excel_process.py
```


