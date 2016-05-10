

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
                    4:1,
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
                    50:3,
                    52:3,
                    53:3,
                    64:3,
                    66:4,
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
                    105:3,
                    106:3,
                    107:3,
                    109:3,
                    113:4,
                    115:4,
                    117:3,
                    118:3,
                    121:3,
                    122:3,
                    125:3,
                    134:2,
                    135:3,
                    136:3,
                    142:4,
                    146:4
                    # 3005:4,
                    # 3435:3,
                    # 3562:4
                }

    return label_dict

def load_unknown_post_index(post2vec_txt_path):
    input_fh = open(post2vec_txt_path, 'rb')
    ans = []
    index = 1
    for line in input_fh:
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
        max_edge = max_key + 1
        unknown_post_index_list = load_unknown_post_index(post2vec_txt_path)
        for idx in unknown_post_index_list:
            if idx <= max_edge:
                labels[idx-1] = 0 # labeled as unknown

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

