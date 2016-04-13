# import operator
from wedc.domain.service.keyword_extraction.seeds import seed_dict
from wedc.domain.vendor.nltk import stem


# CATEGORIES = ['escort', 'job_ads', 'massage']

def identify_post(post):
    if not post.body:
        return []


    judge_dict = {}
    # for cate in CATEGORIES:
    #     judge_dict.setdefault(cate, 0)

    sdict = seed_dict.build_seed_dict()
    # print post.body

    for (word, cates) in sdict.items():
        if stem.stemming(word) in post.body:
            for cate in cates:
                judge_dict.setdefault(cate, 0)
                judge_dict[cate] += 1

    max_value = max(judge_dict.values())
    ans = [cate for (cate, count) in judge_dict.items() if count == max_value]

    return ans
    

    