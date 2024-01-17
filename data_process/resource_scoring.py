import pandas as pd
import numpy as np

resource = pd.read_csv('resource.csv')
columns = ['资源ID', '资源标题', '单个用户观看资源中心内容的次数', '点击收藏的次数', '点击点赞的次数',
           '用户查看元数据的次数', '用户基于SKN网络查看用户的次数', '资源被评价次数', '资源被访问时长']
# 筛选列
filtered_resource = resource[columns]

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
# 对单个用户观看资源中心内容的次数不为零的资源进行对数转换和归一化
non_zero_views = filtered_resource[filtered_resource['单个用户观看资源中心内容的次数'] != 0][
    '单个用户观看资源中心内容的次数']
filtered_resource.loc[filtered_resource[
                          '单个用户观看资源中心内容的次数'] != 0, '单个用户观看资源中心内容的次数分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['单个用户观看资源中心内容的次数分数'].max()
min_score = filtered_resource['单个用户观看资源中心内容的次数分数'].min()
filtered_resource.loc[
    filtered_resource['单个用户观看资源中心内容的次数'] != 0, '单个用户观看资源中心内容的次数分数'] = (
                                                                                                                  filtered_resource[
                                                                                                                      '单个用户观看资源中心内容的次数分数'] - min_score) / (
                                                                                                                  max_score - min_score)
# 对单个用户观看资源中心内容的次数为零的资源直接将评分置为0
filtered_resource.loc[
    filtered_resource['单个用户观看资源中心内容的次数'] == 0, '单个用户观看资源中心内容的次数分数'] = 0

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
# 对点击收藏的次数不为零的资源进行对数转换和归一化
non_zero_views = filtered_resource[filtered_resource['点击收藏的次数'] != 0]['点击收藏的次数']
filtered_resource.loc[filtered_resource['点击收藏的次数'] != 0, '点击收藏的次数分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['点击收藏的次数分数'].max()
min_score = filtered_resource['点击收藏的次数分数'].min()
filtered_resource.loc[filtered_resource['点击收藏的次数'] != 0, '点击收藏的次数分数'] = (filtered_resource[
                                                                                             '点击收藏的次数分数'] - min_score) / (
                                                                                                    max_score - min_score)
# 对点击收藏的次数为零的资源直接将评分置为0
filtered_resource.loc[filtered_resource['点击收藏的次数'] == 0, '点击收藏的次数分数'] = 0

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
# 对点击点赞的次数不为零的资源进行对数转换和归一化
non_zero_views = filtered_resource[filtered_resource['点击点赞的次数'] != 0]['点击点赞的次数']
filtered_resource.loc[filtered_resource['点击点赞的次数'] != 0, '点击点赞的次数分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['点击点赞的次数分数'].max()
min_score = filtered_resource['点击点赞的次数分数'].min()
filtered_resource.loc[filtered_resource['点击点赞的次数'] != 0, '点击点赞的次数分数'] = (filtered_resource[
                                                                                             '点击点赞的次数分数'] - min_score) / (
                                                                                                    max_score - min_score)
# 对点击点赞的次数为零的资源直接将评分置为0
filtered_resource.loc[filtered_resource['点击点赞的次数'] == 0, '点击点赞的次数分数'] = 0

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
# 对用户查看元数据的次数不为零的资源进行对数转换和归一化
non_zero_views = filtered_resource[filtered_resource['用户查看元数据的次数'] != 0]['用户查看元数据的次数']
filtered_resource.loc[filtered_resource['用户查看元数据的次数'] != 0, '用户查看元数据的次数分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['用户查看元数据的次数分数'].max()
min_score = filtered_resource['用户查看元数据的次数分数'].min()
filtered_resource.loc[filtered_resource['用户查看元数据的次数'] != 0, '用户查看元数据的次数分数'] = (filtered_resource[
                                                                                                         '用户查看元数据的次数分数'] - min_score) / (
                                                                                                                max_score - min_score)
# 对用户查看元数据的次数为零的资源直接将评分置为0
filtered_resource.loc[filtered_resource['用户查看元数据的次数'] == 0, '用户查看元数据的次数分数'] = 0

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
non_zero_views = filtered_resource[filtered_resource['用户基于SKN网络查看用户的次数'] != 0][
    '用户基于SKN网络查看用户的次数']
filtered_resource.loc[
    filtered_resource['用户基于SKN网络查看用户的次数'] != 0, '用户基于SKN网络查看用户的次数分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['用户基于SKN网络查看用户的次数分数'].max()
min_score = filtered_resource['用户基于SKN网络查看用户的次数分数'].min()
filtered_resource.loc[filtered_resource['用户基于SKN网络查看用户的次数'] != 0, '用户基于SKN网络查看用户的次数分数'] = (
                                                                                                                                  filtered_resource[
                                                                                                                                      '用户基于SKN网络查看用户的次数分数'] - min_score) / (
                                                                                                                                  max_score - min_score)
filtered_resource.loc[filtered_resource['用户基于SKN网络查看用户的次数'] == 0, '用户基于SKN网络查看用户的次数分数'] = 0

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
non_zero_views = filtered_resource[filtered_resource['资源被评价次数'] != 0]['资源被评价次数']
filtered_resource.loc[filtered_resource['资源被评价次数'] != 0, '资源被评价次数分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['资源被评价次数分数'].max()
min_score = filtered_resource['资源被评价次数分数'].min()
filtered_resource.loc[filtered_resource['资源被评价次数'] != 0, '资源被评价次数分数'] = (filtered_resource[
                                                                                             '资源被评价次数分数'] - min_score) / (
                                                                                                    max_score - min_score)
filtered_resource.loc[filtered_resource['资源被评价次数'] == 0, '资源被评价次数分数'] = 0

# 设置基础评分和对数转换的底数
base_score = 1
log_base = 2  # 以2为底的对数转换
# 访问时间以秒为单位
non_zero_views = filtered_resource[filtered_resource['资源被访问时长'] != 0]['资源被访问时长']
filtered_resource.loc[filtered_resource['资源被访问时长'] != 0, '资源被访问时长分数'] = base_score + np.log(
    non_zero_views) / np.log(log_base)
max_score = filtered_resource['资源被访问时长分数'].max()
min_score = filtered_resource['资源被访问时长分数'].min()
filtered_resource.loc[filtered_resource['资源被访问时长'] != 0, '资源被访问时长分数'] = (filtered_resource[
                                                                                             '资源被访问时长分数'] - min_score) / (
                                                                                                    max_score - min_score)
filtered_resource.loc[filtered_resource['资源被访问时长'] == 0, '资源被访问时长分数'] = 0

# 计算CRITIC权重
columns_critic = ['单个用户观看资源中心内容的次数分数', '点击收藏的次数分数', '点击点赞的次数分数',
                  '用户查看元数据的次数分数', '用户基于SKN网络查看用户的次数分数', '资源被评价次数分数',
                  '资源被访问时长分数']
caculate_resource = filtered_resource[columns_critic]
# 计算标准差
std_score = np.std(caculate_resource)
# print(std_score)

# 计算指标相关性系数
correlation_matrix = caculate_resource.corr()


# 计算指标冲突性
def calculate_conflict(matrix):
    conflicts = []
    n = len(matrix)
    for i in range(n):
        conflict = 0
        for j in range(n):
            conflict += 1 - matrix.iloc[i, j]
        conflicts.append(conflict)
    return conflicts


conflicts = calculate_conflict(correlation_matrix)
# print(conflicts)

# 计算信息量
informations = []
for i in range(len(conflicts)):
    information = conflicts[i] * std_score[i]
    informations.append(information)
# print(informations)

# 计算权重
weights = []
sum = 0
for i in range(len(informations)):
    sum += informations[i]
for i in range(len(informations)):
    weight = informations[i] / sum
    weights.append(weight)
# print(weights)

# CRITIC权重
weight_view_resource = 0.17598471637568938
weight_collect = 0.05455503186889523
weight_like = 0.06246294047465217
weight_view_metadata = 0.10415047014010625
weight_SKN = 0.0520772883115747
weight_comment = 0.28144055041589766
weight_time = 0.2693290024131846

# 计算加权平均评分
filtered_resource['综合评分'] = (filtered_resource['单个用户观看资源中心内容的次数分数'] * weight_view_resource +
                                 filtered_resource['点击收藏的次数分数'] * weight_collect +
                                 filtered_resource['点击点赞的次数分数'] * weight_like +
                                 filtered_resource['用户查看元数据的次数分数'] * weight_view_metadata +
                                 filtered_resource['用户基于SKN网络查看用户的次数分数'] * weight_SKN +
                                 filtered_resource['资源被评价次数分数'] * weight_comment +
                                 filtered_resource['资源被访问时长分数'] * weight_time) / (
                                            weight_view_resource + weight_collect + weight_like + weight_view_metadata + weight_SKN + weight_comment)

filtered_resource.to_csv('score.csv', encoding='utf-8-sig', index=False)
filtered_resource.to_excel('score.xlsx')
pass
