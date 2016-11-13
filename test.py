import cv2
import search

searcher = search.Search('images')

raw_img = cv2.imread('temp.jpg', 0)
for match in searcher.top_n_add(raw_img,50):
    print match

raw_img = cv2.imread('temp.jpg', 0)
for match in searcher.top_n_mult(raw_img,50):
    print match
