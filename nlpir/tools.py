# coding = utf-8
import os
import requests


def download(url, des):
    """
    Download a file from url and save to des, use to download license from github

    :param url: url to download
    :param des: a path to save the data from url
    :return: None
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{url} download fail")
        return
    with open(des, "wb") as f:
        f.write(response.content)


def update_license(data_path=None) -> None:
    """
    update license from NLPIR github repo

    :param data_path: the path to save the license, save in Data if None provide
    """
    base_url = "https://github.com/NLPIR-team/NLPIR/raw/master/License/license%20for%20a%20month/"
    key_dict = {
        "NLPIR.user": "NLPIR-ICTCLAS分词系统授权/NLPIR.user",
        "KeyScanner/keyScan.user": "KeyScanner九眼智能扫描授权/keyScan.user",
        "DeepClassifier/deepclassifier.user": "classifier深度学习分类授权/deepclassifier.user",
        "keyExtract.user": "KeyExtract关键词提取授权/keyExtract.user",
        "NewWordFinder.user": "NewWordFinder新词发现授权/NewWordFinder.user",
        "summary.user": "Summary自动摘要提取授权/summary.user",
        "DocExtractor.user": "DocExtractor文档提取授权/DocExtractor.user",
        "sentiment.user": "SentimentNew情感分析授权/sentiment.user",
        "classifier.user": "classifier规则分类授权/classifier.user",
        "cluster.user": "cluster聚类授权/cluster.user",
        "TextSimilarity.user": "TextSimilarity文本相似度/TextSimilarity.user",
    }
    if data_path is None:
        destination = os.path.join(os.path.dirname(__file__), "Data")
    else:
        destination = data_path
    print("start download license!")
    for key in key_dict:
        des_path = os.path.join(destination, key)
        if not os.path.exists(os.path.dirname(des_path)):
            os.makedirs(os.path.dirname(des_path))
        print(f"download license:{key} from {base_url + key_dict[key]} save to {des_path}")
        download(base_url + key_dict[key], des_path)
