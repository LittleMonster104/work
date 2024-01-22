import pandas as pd
import numpy as np
import glob
import openpyxl.utils.exceptions as excel_exceptions

# 获取所有要读取的 Excel 文件的文件名
file_pattern = 'beishi/待完善元数据/*.xls'  # 指定 Excel 文件所在的文件夹路径和文件名模式
file_list = glob.glob(file_pattern)
# 创建一个空的 DataFrame 来存储所有 Excel 文件的内容
unlabeled_data = pd.DataFrame()
# 循环遍历文件列表并读取数据
for file in file_list:
    # 读取 Excel 文件
    data = pd.read_excel(file)
    unlabeled_data = pd.concat([unlabeled_data, data], ignore_index=True)

labeled_data = pd.DataFrame()
labeled_file = 'beishi/已标记元数据.xls'
labeled_data = pd.read_excel(labeled_file)

all_data = pd.DataFrame()
all_data = pd.concat([labeled_data, unlabeled_data], ignore_index=True)

# 读取埋点数据
file_pattern = 'beishi/埋点数据/*.xls'  # 指定 Excel 文件所在的文件夹路径和文件名模式
file_list = glob.glob(file_pattern)
# 创建一个空的 DataFrame 来存储所有 Excel 文件的内容
Buried_data = pd.DataFrame()
# 循环遍历文件列表并读取数据
for file in file_list:
    # 读取 Excel 文件
    data = pd.read_excel(file)
    Buried_data = pd.concat([Buried_data, data], ignore_index=True)
# print(Buried_data)

# 统计每个资源被评价的次数
comment = pd.read_excel('beishi/资源埋点数据.xlsx', sheet_name='用户的评价内容')
comment = comment.groupby('资源ID').size().reset_index(name='资源被评价次数')
# print(comment)


# 统计每个资源被浏览的总时间
df = pd.read_excel('beishi/资源埋点数据.xlsx', sheet_name='资源预览被点击查看的时长')
# 将时间列转换为日期时间类型
df['时间'] = pd.to_datetime(df['时间'])
# 标记需要计算的行
df['计算'] = False
# 找到满足条件的行并标记为计算
enter_mask = (df['操作'] == '进入资源详情页') & (df['操作'].shift(-1) == '退出资源详情页')
df.loc[enter_mask, '计算'] = True
cumulative_time = 0
for index, row in df.iterrows():
    if row['计算']:
        next_row = df.iloc[index + 1]
        time_difference = (next_row['时间'] - row['时间']).total_seconds()
        df.at[index, '时间差'] = time_difference
df['时间差'].fillna(0, inplace=True)
# 按照资源id进行分组，并计算每组的时间差的累加
sum_time = df.groupby('访问资源id')['时间差'].sum().reset_index()
sum_time = sum_time.rename(columns={'访问资源id': '资源ID'})
sum_time = sum_time.rename(columns={'时间差': '资源被访问时长'})
# print(sum_time)

# 处理非法字符并替换为空字符串
def clean_string(value):
    if pd.notna(value):
        return ''.join(filter(lambda x: x.isprintable(), str(value)))
    return value

# 统计资源信息，实际上没有资源ID重复的情况
resource_all = all_data.iloc[:, 0:3]
resource = resource_all.drop_duplicates(subset=["资源ID"], keep="first")
# 合并DataFrame，根据资源ID列匹配
resource = resource.merge(Buried_data, on="资源ID", how="left")
resource = resource.merge(comment, on="资源ID", how="left")
resource = resource.merge(sum_time, on="资源ID", how="left")
resource['资源被评价次数'].fillna(0, inplace=True)
resource['单个用户观看资源中心内容的次数'].fillna(0, inplace=True)
resource['点击收藏的次数'].fillna(0, inplace=True)
resource['点击点赞的次数'].fillna(0, inplace=True)
resource['用户查看元数据的次数'].fillna(0, inplace=True)
resource['用户基于SKN网络查看用户的次数'].fillna(0, inplace=True)
resource['资源被访问时长'].fillna(0, inplace=True)
# 清洗 DataFrame 中的每个单元格
for col in resource_all.columns:
    resource[col] = resource_all[col].apply(clean_string)
# 将 DataFrame 写入 Excel 文件，如果还有非法字符，会被替换为空字符串

# 对预处理好的数据进行归一化处理
# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换

# 对单个用户观看资源中心内容的次数不为零的资源进行对数转换和归一化
non_zero_views = resource[resource['单个用户观看资源中心内容的次数'] != 0]['单个用户观看资源中心内容的次数']
resource.loc[resource['单个用户观看资源中心内容的次数'] != 0, '单个用户观看资源中心内容的次数'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['单个用户观看资源中心内容的次数'].max()
min_score = resource['单个用户观看资源中心内容的次数'].min()
resource.loc[resource['单个用户观看资源中心内容的次数'] != 0, '单个用户观看资源中心内容的次数'] = (resource['单个用户观看资源中心内容的次数'] - min_score) / (max_score - min_score)
resource.loc[resource['单个用户观看资源中心内容的次数'] == 0, '单个用户观看资源中心内容的次数'] = 0


# 对点击收藏的次数不为零的资源进行对数转换和归一化
non_zero_views = resource[resource['点击收藏的次数'] != 0]['点击收藏的次数']
resource.loc[resource['点击收藏的次数'] != 0, '点击收藏的次数'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['点击收藏的次数'].max()
min_score = resource['点击收藏的次数'].min()
resource.loc[resource['点击收藏的次数'] != 0, '点击收藏的次数'] = (resource['点击收藏的次数'] - min_score) / (max_score - min_score)
resource.loc[resource['点击收藏的次数'] == 0, '点击收藏的次数'] = 0


# 对点击点赞的次数不为零的资源进行对数转换和归一化
non_zero_views = resource[resource['点击点赞的次数'] != 0]['点击点赞的次数']
resource.loc[resource['点击点赞的次数'] != 0, '点击点赞的次数'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['点击点赞的次数'].max()
min_score = resource['点击点赞的次数'].min()
resource.loc[resource['点击点赞的次数'] != 0, '点击点赞的次数'] = (resource['点击点赞的次数'] - min_score) / (max_score - min_score)
# 对点击点赞的次数为零的资源直接将评分置为0
resource.loc[resource['点击点赞的次数'] == 0, '点击点赞的次数'] = 0


# 对用户查看元数据的次数不为零的资源进行对数转换和归一化
non_zero_views = resource[resource['用户查看元数据的次数'] != 0]['用户查看元数据的次数']
resource.loc[resource['用户查看元数据的次数'] != 0, '用户查看元数据的次数'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['用户查看元数据的次数'].max()
min_score = resource['用户查看元数据的次数'].min()
resource.loc[resource['用户查看元数据的次数'] != 0, '用户查看元数据的次数'] = (resource['用户查看元数据的次数'] - min_score) / (max_score - min_score)
# 对用户查看元数据的次数为零的资源直接将评分置为0
resource.loc[resource['用户查看元数据的次数'] == 0, '用户查看元数据的次数'] = 0


non_zero_views = resource[resource['用户基于SKN网络查看用户的次数'] != 0][
    '用户基于SKN网络查看用户的次数']
resource.loc[resource['用户基于SKN网络查看用户的次数'] != 0, '用户基于SKN网络查看用户的次数'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['用户基于SKN网络查看用户的次数'].max()
min_score = resource['用户基于SKN网络查看用户的次数'].min()
resource.loc[resource['用户基于SKN网络查看用户的次数'] != 0, '用户基于SKN网络查看用户的次数'] = (resource['用户基于SKN网络查看用户的次数'] - min_score) / (max_score - min_score)
resource.loc[resource['用户基于SKN网络查看用户的次数'] == 0, '用户基于SKN网络查看用户的次数'] = 0


non_zero_views = resource[resource['资源被评价次数'] != 0]['资源被评价次数']
resource.loc[resource['资源被评价次数'] != 0, '资源被评价次数'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['资源被评价次数'].max()
min_score = resource['资源被评价次数'].min()
resource.loc[resource['资源被评价次数'] != 0, '资源被评价次数'] = (resource['资源被评价次数'] - min_score) / (max_score - min_score)
resource.loc[resource['资源被评价次数'] == 0, '资源被评价次数'] = 0


# 访问时间以秒为单位
non_zero_views = resource[resource['资源被访问时长'] != 0]['资源被访问时长']
resource.loc[resource['资源被访问时长'] != 0, '资源被访问时长'] = base_score + np.log(non_zero_views) / np.log(log_base)
max_score = resource['资源被访问时长'].max()
min_score = resource['资源被访问时长'].min()
resource.loc[resource['资源被访问时长'] != 0, '资源被访问时长'] = (resource['资源被访问时长'] - min_score) / (max_score - min_score)
resource.loc[resource['资源被访问时长'] == 0, '资源被访问时长'] = 0


try:
    resource.to_excel('resource.xlsx', index=False)
    resource.to_csv('resource.csv', index=False)
except excel_exceptions.IllegalCharacterError as e:
    print(f"An IllegalCharacterError occurred: {e}")
