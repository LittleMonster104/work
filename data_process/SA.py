from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "hw2942/bert-base-chinese-finetuning-financial-news-sentiment-v2"
# model_name = "./model"


def SA_func(text: str):
    '''
    输入：评论内容，类型str
    输出：情感分析结果{消极，中性，积极}其中之一，类型str
    '''
    id2_label = {0: "消极", 1: "中性", 2: "积极"}
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt")
    logits = model(**inputs).logits
    pred = torch.argmax(logits, dim=-1)
    result = id2_label.get(pred.item())
    return result


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
            "内容很棒"
            ]
    result,percent = statistic(list)
    print(result, percent)
    结果：中性,55.56
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

    return max_sentiment, max_ratio

# if __name__ == '__main__':
#     list = ["内容丰富，思路清晰，值得学习！",
#             "知识点标注有误",
#             "老师的教学思路非常清晰，课件制作也很生动，后面例子的讲解非常有效，可以直观地让学生感受细节描写的应用。",
#             "哪里出错了吗?想打开学习，是黑屏。",
#             "讲的透彻，值得学习",
#             "重难点突出，讲解详细。",
#             "详略得当，重难点突出。",
#             "这个教学设计，针对性很强，内容很清晰，很容易理解与接受，使我们受益匪浅。",
#             "内容很棒"
#             ]
#     result, percent = statistic(list)
#     print(result, percent)
