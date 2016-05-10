


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

