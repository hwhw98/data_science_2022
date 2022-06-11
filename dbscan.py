import pandas as pd
import numpy as np

print("type in input file number")
file_num = input()
print("type in cluster count")
n = int(input())
print("type in epsilon")
epsilon = int(input())
print("type in minPts")
minPts = int(input())


# initial cluster count
C = 0

x = pd.read_csv("./data-2/input{}.txt".format(file_num), "\t", header = None, names = ['0', '1', '2'])
x.drop('0', axis=1, inplace = True)
input = x.to_numpy()
d_n = len(x)

p, q = np.meshgrid(np.arange(d_n), np.arange(d_n))
dist = np.sqrt(np.sum(((input[p] - input[q])**2),2))


visited = np.full((d_n), False)
noise = np.full((d_n),False)
label = np.full((d_n),0)

def regionQuery(i, d_n, input, epsilon, dist):
    g = dist[i,:] < epsilon
    Neighbors = np.where(g)[0].tolist()
    return Neighbors

def expandCluster(i, neighbors, label, visited, minPts, d_n, input, epsilon, dist, C):
    label[i] = C
    k = 0
    
    while True:
        if len(neighbors) <= k:
            return
        j = neighbors[k]
        if visited[j] != True:
            visited[j] = True

            neighbors2 = regionQuery(j, d_n, input, epsilon, dist)
            v = [neighbors2[i] for i in np.where(label[neighbors2]==0)[0]]

            if len(neighbors2) >=  minPts:
                neighbors = neighbors+v

        # if unlabeled
        if label[j] == 0 : label[j] = C
        k += 1

for i in range(d_n):
    if visited[i] == False:
        visited[i] = True
        neighbors = regionQuery(i, d_n, input, epsilon, dist)
        if len(neighbors) >= minPts:
            C += 1
            expandCluster(i, neighbors, label, visited, minPts, d_n, input, epsilon, dist, C)
        else : noise[i] = True

clusters = {'cluster{}'.format(k):list() for k in range(1, C+1)} #각 클러스터 안에 data들
for i in range(d_n):
    if label[i]>0:
        cl = 'cluster{}'.format(label[i])
        clusters[cl].append(i)

clusters_n = [] #각 클러스터 인덱스
for i in range(C+1):
    clusters_n.append(0)
for i in range(d_n):
    clusters_n[label[i]] += 1
clusters_n = clusters_n[1:]# label 0인 outlier제외


cnt = C
rmv_idx = []
while cnt > n:
    min_idx = 0
    for i in range(1, C):
        if clusters_n[i]==0:
            continue
        elif clusters_n[min_idx]>clusters_n[i]:
            min_idx = i
    rmv_idx.append(min_idx)
    clusters_n[min_idx] = 0
    cnt -= 1

for i in range(len(rmv_idx)):
    clusters.pop('cluster{}'.format(rmv_idx[i]+1))

cluster_num = 0
for key in clusters:
    f = open("./result/input{}_cluster_{}".format(file_num, cluster_num), 'w')
    value = clusters[key]
    for j in range(len(value)):
        string = str(value[j])+"\n"
        f.write(string)
    cluster_num += 1
    