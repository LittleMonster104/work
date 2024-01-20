## 代码环境
The code has been tested running under Python 3.9.12. The required packages are as follows:

- numpy == 1.23.5
- pandas == 2.0.3
- transformers == 4.26.1
- torch == 1.13.1
- openpyxl == 3.1.2

### 文本情绪分类模型
SA.py  

输入：评论列表，类型list  

输出：列表中情感占比的最大项，及其所占比例

### 被动反馈数据
数据输入为beishi文件夹下面的数据  

1.运行excel_process.py进行数据预处理，生成resource.xlsx文件
```
python excel_process.py
```
2.运行resource_scoring.py对数据进行归一化处理，根据CRITIC权重计算综合评分，生成score.xlsx文件
```
python resource_scoring.py
```

### CRITIC权重
CRITIC权重法是一种基于数据波动性和冲突性的客观赋权方法。它涉及两个关键指标：  

1.对比强度：通常使用标准差来表示，标准差越大表明数据波动性越大，相应的权重也越高。  

2.冲突性：通过相关系数来表示，相关系数越大，表明指标间的冲突性越小，权重相应地降低。  

3.权重：将对比强度与冲突性指标相乘并执行归一化处理得到的。  

这种方法适用于评估那些具有关联关系的多个指标或因素的重要程度，以减少由于相关性较强而导致的指标间信息的重叠，从而获得更加可信的综合评价结果。
