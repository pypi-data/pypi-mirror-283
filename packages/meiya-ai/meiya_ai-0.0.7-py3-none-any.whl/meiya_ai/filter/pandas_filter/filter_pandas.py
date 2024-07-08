import json
import pandas as pd
from datasets import load_dataset


def filter_based_pandas(input_path: str, output_path: str, filter_list: list):
    ag_dataset = load_dataset("json", data_files=input_path, split="train")
    print("过滤前的数据有：{}".format(len(ag_dataset)))
    ag_dataset = ag_dataset.to_pandas()
    for k in filter_list:
        ag_dataset = ag_dataset.drop_duplicates(subset=k)
    ag_dataset = ag_dataset.to_dict(orient='records')
    with open(output_path, 'w', encoding='utf-8') as W:
        json.dump(ag_dataset, W, ensure_ascii=False, indent=4)
    print("过滤后的数据有：{}".format(len(ag_dataset)))
    return ag_dataset


if __name__ == "__main__":

    # tmp(input_path="data.json", output_path="datas.json", filter_list=["text"])
    with open("datas.json", 'r', encoding='utf-8') as W:
        data = json.load(W)
    print(data[0])


    