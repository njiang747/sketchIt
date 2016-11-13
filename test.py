import cv2
import search
import time


start = time.time()

searcher = search.Search('images')

<<<<<<< HEAD
raw_img = cv2.imread('temp.jpg', 0)
=======
end = time.time()
print end - start

raw_img = cv2.imread('sketches/star.jpg', 0)
>>>>>>> 0368c1815dc74930b7c9bb723436ef0edfab6a83
for match in searcher.top_n_add(raw_img,50):
    print match

raw_img = cv2.imread('temp.jpg', 0)
for match in searcher.top_n_mult(raw_img,50):
    print match

# hits = [[[set() for i in range(0, 6)] for j in range(0, 100)] for k in range(0, 100)]
# edgels = database.load_data(hits, 'pre_state.csv')