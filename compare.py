import numpy as np
import preprocess


# Takes in a query edgel set and returns the top n matches (idx,score)
def query_compare(query_set, edgel_table, hitcounts, n):
    db_images = np.zeros(len(hitcounts))
    for edgel in query_set:
        for i in edgel_table[edgel[0]][edgel[1]][edgel[2]]:
            db_images[i] += 1
    np_hitcounts = np.array(hitcounts)
    db_images = np.divide(db_images, np_hitcounts)
    x = db_images.argsort()[-n:][::-1]
    y = [db_images[i] for i in x]
    return (x,y)


def database_compare(images, query_img, i_size, n_angles):
    pre = preprocess.Preprocess(i_size, n_angles)
    pre.process_img(query_img)
    hitmap = pre.get_hitmap()
    hitcount = pre.get_hitcounts()[0]
    delta = 1.0 / hitcount
    image_scores = np.asarray([0.] * len(images))
    for i in range(0, len(images)):
        edgels = pre.get_edgels(images[i])
        for edgel in edgels:
            for _ in hitmap[edgel[0]][edgel[1]][edgel[2]]:
                image_scores[i] += delta
    return image_scores
