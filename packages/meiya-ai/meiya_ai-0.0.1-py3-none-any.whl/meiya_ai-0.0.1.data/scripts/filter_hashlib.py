import hashlib
from datasets import load_dataset
import json


def get_hash(example):
    """Get hash of content field."""
    return {"hash": hashlib.md5(example["text"].strip().encode("utf-8")).hexdigest()}

def check_uniques(example, uniques):
    """Check if current hash is still in set of unique hashes and remove if true."""
    if example["hash"] in uniques:
        uniques.remove(example["hash"])
        return True
    else:
        return False

def preprocess(example):
    """Chain all preprocessing steps into one function to not fill cache."""
    results = dict()
    results.update(get_hash(example))
    return results

def filter_duplicates(example, uniques):
    """Filter dataset with heuristics. Config, test and has_no_keywords files are removed with a given probability."""
    if not check_uniques(example, uniques):
        return False
    else:
        return True


def filter_based_hashlib(input_path: str, output_path: str):
    ag_dataset = load_dataset("json", data_files=input_path, split="train")
    print("过滤前的数据有：{}".format(len(ag_dataset)))
    # Run preprocessing
    sql_dataset = ag_dataset.map(preprocess, num_proc=4)

    # Deduplicate hashes
    uniques = set(sql_dataset.unique("hash"))

    # Deduplicate data and apply heuristics
    sql_dataset_hashlib_deduped = sql_dataset.filter(filter_duplicates, fn_kwargs={"uniques": uniques})
    sql_dataset_hashlib_deduped = sql_dataset_hashlib_deduped.to_list()
    keys = [k for k, v in sql_dataset_hashlib_deduped[0].items() if k != "hash"]
    sv_lst = []
    for itm in sql_dataset_hashlib_deduped:
        sv_lst.append({
            k: itm[k] for k in keys
        })
    with open(output_path, 'w', encoding='utf-8') as W:
        json.dump(sv_lst, W, ensure_ascii=False, indent=4)
    print("过滤后的数据有：{}".format(len(sv_lst)))
    return sv_lst


if __name__ == "__main__":
    # sv_lst = []
    filter_based_hashlib(input_path="data.json", output_path="datas.json")
    # with open("data.json", 'r', encoding='utf-8') as R:
    #     data = R.readlines()
    #     for itm in data:
    #         sv_lst.append(json.loads(itm))
    #     sv_lst = sv_lst[0:3000]


    # with open("data.json", 'w', encoding='utf-8') as W:
    #     json.dump(sv_lst, W, ensure_ascii=False, indent=4)
    # print(data[0])
    # print(len(data))


