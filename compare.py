import numpy as np
import preprocess


# Takes in a query edgel set and returns the top n matches (idx,score)
def query_compare(query_set, edgel_table, edgel_counts, n):
    hit_counts = np.zeros(len(edgel_counts))
    for edgel in query_set:
        for i in edgel_table[edgel[0]][edgel[1]][edgel[2]]:
            hit_counts[i] += 1
    np_edgel_counts = np.array(edgel_counts)
    hit_counts = np.divide(hit_counts, np_edgel_counts)
    x = hit_counts.argsort()[-n:][::-1]
    y = [hit_counts[i] for i in x]
    return (x,y)


def database_compare(images, query_img, i_size, n_angles):
    pre = preprocess.Preprocess(i_size, n_angles)
    pre.process_img(query_img)
    hitmap = pre.get_hitmap()
    edgel_count = pre.get_edgel_counts()[0]
    hit_counts = np.asarray([0.] * len(images))
    for i in range(0, len(images)):
        edgels = pre.get_edgels(images[i])
        for edgel in edgels:
            for _ in hitmap[edgel[0]][edgel[1]][edgel[2]]:
                hit_counts[i] += 1
    return hit_counts / edgel_count
