import torch
import pandas as pd
import tqdm
from transformers import T5Tokenizer, AutoModelForSeq2SeqLM

# model_name = "yuyijiong/T5-large-sentiment-analysis-Chinese-MultiTask"
model_name = "./model2"


def SA_func(text: str):
    '''
    输入：评论内容，类型str
    输出：情感分析结果{消极，中性，积极}其中之一，类型str
    '''
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="auto")
    text = f'判断以下评论的情感极性: [{text}]'
    input_ids = tokenizer(text, return_tensors="pt", padding=True)['input_ids'].cuda(0)
    with torch.no_grad():
        output = model.generate(input_ids=input_ids)
    output_str = tokenizer.batch_decode(output, skip_special_tokens=True)
    if output_str[0] not in ["消极", "中性", "积极"]:
        return output_str[0][-2:]
    return output_str[0]


def statistic(comment_list: list):
    '''
    输入：评论列表，类型list
    输出：列表中情感占比的最大项，及其所占百分比
    示例：
    list = ["内容丰富，思路清晰，值得学习！",
            "知识点标注有误",
            "老师的教学思路非常清晰，课件制作也很生动，后面例子的讲解非常有效，可以直观地让学生感受细节描写的应用。",
            "哪里出错了吗?想打开学习，是黑屏。",
            "讲的透彻，值得学习",
            "重难点突出，讲解详细。",
            "详略得当，重难点突出。",
            "这个教学设计，针对性很强，内容很清晰，很容易理解与接受，使我们受益匪浅。",
            "内容很棒",
            "我觉得内容不完善，而且上传的资源也不相符",
            "内容有些不相关",
            "这个教学设计把整式乘法和因式分解相结合，把提公因式法讲解得非常全面，也很容易让学生理解和接受。",
            "郭老师在引入部分利用热点话题切入，在presentation部分先突破各个symptom，再结合语境给予建议，整个课程很流程。",
            "郭老师用真实的情境导入，引入健康话题，当我们不舒服时该用英语说，又该怎么关爱他人，引起学生学习兴趣，创设了用英语解决实际生活中问题的情境，学生在情境中学习句型词汇，效果就好多了。",
            "石老师的讲解，为我指明了学习方向和实践方向，在今后教学中要时刻牢记和渗透学科素养为育人导向，也要努力琢磨如何在命题中体现学科素养。"
            ]
    result,percent = statistic(list)
    print(result, percent)
    结果：积极 66.67
    '''
    if not comment_list:
        return "评论列表为空，无法分析。"

    sentiment_counts = {"消极": 0, "中性": 0, "积极": 0}

    for comment in comment_list:
        result = SA_func(comment)
        if result in sentiment_counts:
            sentiment_counts[result] += 1

    total_comments = len(comment_list)
    max_sentiment, max_count = max(sentiment_counts.items(), key=lambda item: item[1])
    max_ratio = round((max_count / total_comments) * 100, 2)

    return max_sentiment, max_ratio ,sentiment_counts

# if __name__ == '__main__':
#
#     # 读取Excel文件
#     df = pd.read_excel("./beishi/资源埋点数据.xlsx", engine='openpyxl', sheet_name='用户的评价内容')
#     # 仅对前10条评论进行情感分析
#     # df.loc[:1000, 'Sentiment'] = df.loc[:1000, '评价内容'].apply(SA_func)
#     df.loc['Sentiment'] = df.loc['评价内容'].apply(SA_func)
#     # 保存修改后的DataFrame到新的Excel文件
#     df.to_excel("./beishi/资源埋点数据_分析结果.xlsx", index=False, engine='openpyxl')
#     print("finished")
#     list = ["内容丰富，思路清晰，值得学习！",
#             "知识点标注有误",
#             "老师的教学思路非常清晰，课件制作也很生动，后面例子的讲解非常有效，可以直观地让学生感受细节描写的应用。",
#             "哪里出错了吗?想打开学习，是黑屏。",
#             "讲的透彻，值得学习",
#             "重难点突出，讲解详细。",
#             "详略得当，重难点突出。",
#             "这个教学设计，针对性很强，内容很清晰，很容易理解与接受，使我们受益匪浅。",
#             "内容很棒",
#             "我觉得内容不完善，而且上传的资源也不相符",
#             "内容有些不相关",
#             "这个教学设计把整式乘法和因式分解相结合，把提公因式法讲解得非常全面，也很容易让学生理解和接受。",
#             "郭老师在引入部分利用热点话题切入，在presentation部分先突破各个symptom，再结合语境给予建议，整个课程很流程。",
#             "郭老师用真实的情境导入，引入健康话题，当我们不舒服时该用英语说，又该怎么关爱他人，引起学生学习兴趣，创设了用英语解决实际生活中问题的情境，学生在情境中学习句型词汇，效果就好多了。",
#             "石老师的讲解，为我指明了学习方向和实践方向，在今后教学中要时刻牢记和渗透学科素养为育人导向，也要努力琢磨如何在命题中体现学科素养。"
#             ]
#     result,percent = statistic(list)
#     print(result, percent)