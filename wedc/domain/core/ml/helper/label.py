

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
                    15:4,
                    16:4,
                    17:4,
                    11:4,
                    53:3,
                    66:4,
                    72:3,
                    73:4,
                    74:4,
                    75:4,
                    83:4,
                    105:3,
                    106:3,
                    107:3,
                    134:2,
                    135:3,
                    136:3,
                    146:4
                    # 3005:4,
                    # 3435:3,
                    # 3562:4
                }

    return label_dict

def generate_label_file(label_dict, output=None, is_np=True):
    # sorted_label_dict = sorted(label_dict.iteritems(), key=lambda x : x[0])
    max_key = max(label_dict.keys(), key=int)
    labels = [-1]*max_key
    
    for (k, v) in label_dict.items():
        labels[k-1] = v

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

