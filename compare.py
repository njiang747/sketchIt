<<<<<<< HEAD
# Takes in a given query edgel set and the edgel_table and returns the top 5000 image matches
def query_compare (query_set, edgel_table):
    for 

# Takes in 5000 images and returns the top n matches when compared to query
def database_compare(images, query, n):
=======
import numpy as np


#Takes in a query edgel set and returns the top 5000 matches
def query_compare(query_set, edgel_table, db_size):
    db_images = np.zeros(db_size)
    for edgel in query_set:
        for i in edgel_table[edgel]:
            db_images[i] += 1
    x = db_images.argsort()[-5000][::-1]
    return x

def database_compare(images, query_set, n):
    image_scores = np.zeros(len(images))
    for i in range(0,len(images)):
        edgels = generate_edgels(images[i])
        for edgel in edgels:
            if edgel in query_set:
                image_scores[i] += 1
    x = image_scores.argsort()[-n][::-1]
    return x

         





    

>>>>>>> origin/master
