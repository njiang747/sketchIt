import numpy as np
import preprocess

#Takes in a query edgel set and returns the top 5000 matches
def query_compare(query_set, edgel_table, hitcounts):
    db_images = np.zeros(len(hitcounts))
    for edgel in query_set:
        for i in edgel_table[edgel[0]][edgel[1]][edgel[2]]:
            db_images[i] += 1
    np_hitcounts = np.array(hitcounts)
    db_images = np.divide(db_images, np_hitcounts)
    x = db_images.argsort()[-50:][::-1]
    y = [(i,db_images[i]) for i in x]
    return y

def database_compare(images, rankings, query_img, n, i_size, n_angles):
    pre = preprocess.Preprocess(i_size, n_angles)
    pre.process_img(query_img)
    hitmap = pre.get_hitmap()
    hitcount = pre.get_hitcounts()[0]
    image_scores = np.asarray([y[1] for y in rankings])
    delta = 1.0/hitcount
    for i in range(0,len(images)):
        edgels = pre.get_edgels(images[i])
        for edgel in edgels:
            for j in hitmap[edgel[0]][edgel[1]][edgel[2]]:
                image_scores[i] += delta
    x = image_scores.argsort()[-n:][::-1]
    y = [(i, image_scores[i]) for i in x]
    return y

def query_compare_single(img1, img2, i_size, n_angles):
    pre = preprocess.Preprocess(i_size, n_angles)
    pre.process_img(img2)
    hitmap = pre.get_hitmap()
    hitcount = pre.get_hitcounts()[0]
    query_set = pre.get_edgels(img1)
    hits = 0
    for edgel in query_set:
        for i in hitmap[edgel[0]][edgel[1]][edgel[2]]:
            hits += 1
    return hits/hitcount