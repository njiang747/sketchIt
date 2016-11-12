import numpy as np
import preprocess

# i_size = 200

#Takes in a query edgel set and returns the top 5000 matches
def query_compare(query_set, edgel_table, db_size):
    db_images = np.zeros(db_size)
    for edgel in query_set:
        for i in edgel_table[edgel[0]][edgel[1]][edgel[2]]:
            db_images[i] += 1
    x = db_images.argsort()[-50:][::-1]
    y = [(i,db_images[i]) for i in x]
    return y

def database_compare(images, query_img, n, i_size):
    pre = preprocess.Preprocess(i_size)
    pre.process_img(query_img, 0)
    edgel_table = pre.get_hitmap()
    image_scores = np.asarray([y[1] for y in images])
    for i in range(0,len(images)):
        edgels = pre.get_edgels(images[i])
        for edgel in edgels:
            for j in edgel_table[edgel[0]][edgel[1]][edgel[2]]:
                image_scores[i] += 1
    x = image_scores.argsort()[-n:][::-1]
    return x
         


