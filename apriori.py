import numpy as np
import sys 

def main():
    #path = "input.txt"
    path = sys.argv[2]
    min_support = int(sys.argv[1])/100


    # Transactions 불러오기
    order = [str(i)for i in range(100)]
    Transactions, max = load_transactions(path, order)
    order = [str(i)for i in range(max+1)]

    # ~46 apriori algorithm
    # index 붙인 candidate
    C = {}
    L = {}
    itemset_size = 1
    # not frequent itemsets
    Discarded = {itemset_size : []}
    C.update({itemset_size: [ [f] for f in order ]})
    # supp 계산한값 넣는 list
    supp_count_L = {}


    # 초기 사이즈 1 frequent itemset
    f, sup, new_discarded = get_frequent(C[itemset_size], Transactions, min_support, Discarded)
    Discarded.update({itemset_size : new_discarded})
    L.update({itemset_size:f})
    supp_count_L.update({itemset_size : sup})


    # 이후 사이즈 2이상 frequent itemsets
    k = itemset_size + 1
    c = False
    while c == 0:
        C.update({k : join_set_itemsets(L[k-1], order)})
        f, sup, new_discarded = get_frequent(C[k], Transactions, min_support, Discarded)
        Discarded.update({k: new_discarded})
        L.update({k : f})
        supp_count_L.update({k : sup})
        if len(L[k]) == 0:
            c = True
        k += 1


    #min support 만족하는 association rule 구하기
    num_trans = len(Transactions)
    association_rule = ""
    file = open(sys.argv[3], 'w')

    for i in range(1, len(L)):
        for j in range(len(L[i])):
            s = list(powerset(set(L[i][j])))
            s.pop()
            for z in s:
                S = set(z)
                X = set(L[i][j])
                X_S = set(X-S)
                sup_x = count_num(X, Transactions)
                conf = sup_x/ count_num(S, Transactions)
                if sup_x >= min_support:
                    association_rule += write_rules(X, X_S, S, sup_x, conf, num_trans)
    file.write(association_rule)






# input 파일에서 transactions들 읽어오기, item max number max로 return
def load_transactions(path, order):
    Transactions = []
    max = 0
    with open(path, 'r') as fid:
        for lines in fid:
            str_line = list(lines.strip().split('\t'))
            _t = list(np.unique(str_line))
            _t.sort(key=lambda x: order.index(x))
            num = int(_t[-1])
            if(max < num): max=num
            Transactions.append(_t)
    return Transactions, max



# itemset이 포함된 transactions에 itemsets개수
def count_num(itemset, Transactions):
    count = 0
    for i in range(len(Transactions)):
        if set(itemset).issubset(set(Transactions[i])):
            count += 1
    return count



# k-itemsets(특정 index k) candidate lists(itemsets)중 frequent한 itemsets들 L(k-itemsets)에 추가
#                                                   중 not frequent한 itemsets들 new-discarded에 담아서 return
#                                                   L에 itemsets들의 supp count들 return
def get_frequent(itemsets, Transactions, min_support, prev_discarded):
    L = []
    supp_count = []
    new_discarded = []

    k=len(prev_discarded.keys())

    for s in range(len(itemsets)):
        discarded_before = False
        if k > 0:
            for it in prev_discarded[k]:
                if set(it).issubset(set(itemsets[s])):
                    discarded_before = True
                    break
        if not discarded_before:
            count = count_num(itemsets[s], Transactions)
            if count / int(len(Transactions)) >= min_support:
                L.append(itemsets[s])
                supp_count.append(count)
            else:
                new_discarded.append(itemsets[s])
    return L, supp_count, new_discarded



#두개 itemsets 합집합 구하기
def join_two_itemsets(its1, its2, order):
    its1.sort(key=lambda x: order.index(x))
    its2.sort(key=lambda x: order.index(x))

    for i in range(len(its1)-1):
        if its1[i] != its2[i]:
            return []
    if order.index(its1[-1]) < order.index(its2[-1]):
        return its1 + [its2[-1]]
    return []



# itemsets들 가능한 경우의 합집합 구하기
def join_set_itemsets(set_of_itemsets, order):
    C = []
    for i in range(len(set_of_itemsets)):
        for j in range(i+1, len(set_of_itemsets)):
            it_out = join_two_itemsets(set_of_itemsets[i], set_of_itemsets[j], order)
            if len(it_out) > 0:
                C.append(it_out)
    return C



from itertools import combinations, chain

def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))



def write_rules(X, X_S, S, supp, conff, num_trans):
    association_rule = ""
    association_rule += "{"
    association_rule += ','.join(list(S))
    association_rule += "}    {"
    association_rule += ','.join(list(X_S))
    association_rule += "}    "
    sup = format(supp/num_trans*100, ".2f")
    conf = format(conff*100, ".2f")
    association_rule += (sup+"    "+conf+"\n")
    return association_rule



main()
