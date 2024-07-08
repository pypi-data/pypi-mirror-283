import hashlib

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
