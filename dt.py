import math
from collections import Counter, defaultdict
from sys import argv 

def load(path):
    Datas = []
    f = open(path, "r")
    attribute_keys = f.readline()
    keys = attribute_keys
    attribute_keys = attribute_keys.split('\t')
    n = len(attribute_keys)
    class_key = attribute_keys[n-1]
    class_values = []
    attribute_keys = attribute_keys[:n-1]
    for lines in f:
        str_line = list(lines.split('\t'))
        class_value = str_line.pop()
        class_value = class_value.strip('\n')
        Data = dict(zip(attribute_keys, str_line))
        Datas.append((Data, class_value))
        class_values.append(class_value)
    class_values = list(set(class_values))
    
    return Datas, class_values, keys

path = argv[1]

inputs, class_values, keys = load(path)


def entropy(class_probabilites):
# 확률이 0인 경우는 제외함
    return sum(-p * math.log(p ,2) for p in class_probabilites if p is not 0)

def class_probabilities(labels):
# 총 개수 계산
    total_count = len(labels)
    return [float(count) / float(total_count) for count in Counter(labels).values()]

def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)

def partition_entropy(subsets):
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count for subset in subsets)

def partition_by(inputs, attribute):
    groups = defaultdict(list)
    for input in inputs:
        key = input[0][attribute]
        groups[key].append(input)
    return groups

def partition_entropy_by(inputs, attribute):
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())

from functools import partial
def build_tree(inputs, split_candidates=None):
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    num_inputs = len(inputs)

    class_value = inputs[0][1]
    boolean = True
    for k in range(num_inputs):
        if class_value != inputs[k][1]:
            boolean = False
            break
    if boolean == True:
        return class_value



    if not split_candidates:
    # 다수결
        list = [inputs[k][1] for k in range(num_inputs)]
        leaf = max(list, key=list.count) #[("class value", 개수)]
        return leaf

    best_attribute = min(split_candidates, key=partial(partition_entropy_by, inputs))
    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates if a != best_attribute]

    subtrees = { attribute_value : build_tree(subset, new_candidates) for attribute_value, subset in partitions.items()}
    # 기본
    list = [inputs[k][1] for k in range(num_inputs)]
    leaf = max(list, key=list.count)
    subtrees[None] = leaf
    return (best_attribute, subtrees)


def classify(tree, input):
    if tree in class_values:
        return tree
    # dict
    attribute, subtree_dict = tree

    subtree_key = input.get(attribute)

   
    if str(subtree_key) not in subtree_dict:
        subtree_key = None

    subtree = subtree_dict[subtree_key]
    return classify(subtree, input)


tree = build_tree(inputs)

path = argv[2]
f = open(path, "r")
attribute_keys_t = f.readline()
attribute_keys_t = attribute_keys_t.split('\t')
n = len(attribute_keys_t)
attribute_keys_t[n-1] = attribute_keys_t[n-1].strip('\n')
result = []
for lines in f:
    str_line = list(lines.split('\t'))
    str_line[n-1] = str_line[n-1].strip('\n')
    Data = dict(zip(attribute_keys_t, str_line))
    result.append(classify(tree, Data))

f = open(argv[2], 'r')
print(argv[2])
fw = open(argv[3], 'w')
f.readline()
fw.write(keys)
k = 0
for i in range(len(result)):
    lines = f.readline()
    str_line = lines.strip('\n')
    fw.write(str_line+'\t')
    fw.write(result[k])
    fw.write('\n')
    k+=1
