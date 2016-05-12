

def load_label_dict():
    # -1: unknown
    #  1: others
    #  2: massage
    #  3: escort
    #  4: job_ads

    label_dict = {
                    1:4,
                    2:4,
                    3:4,
                    # 4:1,
                    5:4,
                    6:4,
                    7:4,
                    8:4,
                    9:3,
                    10:3,
                    11:4,
                    15:4,
                    16:4,
                    17:4,
                    21:3,
                    35:4,
                    46:4,
                    50:3,
                    51:3,
                    52:3,
                    53:3,
                    62:4,
                    64:3,
                    66:4,
                    67:3,
                    68:3,
                    70:4,
                    71:4,
                    72:3,
                    73:4,
                    74:4,
                    75:4,
                    83:4,
                    84:3,
                    85:3,
                    86:3,
                    89:3,
                    91:3,
                    95:4,
                    105:3,
                    106:3,
                    107:3,
                    109:3,
                    112:4,
                    113:4,
                    115:4,
                    117:3,
                    118:3,
                    121:3,
                    122:3,
                    125:3,
                    127:3,
                    128:3,
                    129:3,
                    131:3,
                    134:3, #2,
                    135:3,
                    136:3,
                    137:3,
                    141:4,
                    142:4,
                    146:4,
                    200:3,
                    300:3,
                    400:4,
                    450:4,
                    470:4,
                    480:4,
                    485:4,
                    490:3,
                    500:4,
                    600:4,
                    700:4,
                    742:4,
                    744:4,
                    774:4,
                    767:4,
                    783:4,
                    800:4,
                    880:4,
                    888:4,
                    889:4,
                    890:4,
                    891:4,
                    892:4,
                    908:4,
                    950:4,
                    1045:3,
                    1120:4,
                    1175:4,
                    1177:4,
                    1180:4,
                    1200:4,
                    1251:4,
                    1350:4,  # 60.713s
                    1420:4,
                    1540:3,
                    1600:3,
                    1625:4,
                    1630:4,
                    1635:4,
                    1637:4,
                    1638:4,
                    # 1639:4,
                    1640:4,
                    # 1650:3,
                    # 1700:3,
                    # 1800:4,
                    # 1900:4,
                    # 2000:4,
                    # 2100:4,
                    # 2200:4,
                    # 2320:4,
                    # 2420:3,
                    # 2500:3,
                    # 2620:4,
                    # 2720:3,
                    # 2820:4,
                    # 2920:3,
                    # 3020:4,
                    # 3120:3,
                    # 3220:3,
                    # 3320:4
                    # 3446:2,
                    # 8569:2,
                    # 9006:3,
                    # 9306:3
                    # 3005:4,
                    # 3435:3,
                    # 3562:4
                }

    return label_dict

def load_unknown_post_index(post2vec_txt_path, upper_bound=None):
    input_fh = open(post2vec_txt_path, 'rb')
    ans = []
    index = 1
    lines = input_fh.readlines()
    for line in lines[:upper_bound]:
        line = line.strip()
        if max([float(_) for _ in line.split(' ')]) == 0:
            ans.append(index)
        index += 1
    return ans

def generate_label_file(label_dict, output=None, is_np=True, post2vec_txt_path=None):
    # sorted_label_dict = sorted(label_dict.iteritems(), key=lambda x : x[0])
    max_key = max(label_dict.keys(), key=int)
    labels = [-1]*max_key
    
    for (k, v) in label_dict.items():
        labels[k-1] = v

    if post2vec_txt_path:
        # max_edge = max_key + 1
        unknown_post_index_list = load_unknown_post_index(post2vec_txt_path, 
                                                        upper_bound=max_key + 1)
        for idx in unknown_post_index_list:
            # if idx <= max_edge:
            labels[idx-1] = 1 # labeled as unknown

    if output:
        output_fh = open(output, 'wb')
        for label in labels:
            output_fh.write(str(label) + '\n')
        output_fh.close()

    if is_np:
        import numpy as np
        labels = np.array(labels)

    return labels

"""
label_dict = {
                1:1,
                10:3,
                2:1,
                4:2,
                20:1
            }
print generate_label_file(label_dict)
"""

