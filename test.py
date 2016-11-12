import cv2
import search

searcher = search.Search('Images')
raw_img = cv2.imread('person.jpg', 0)
for match in searcher.top_n(raw_img,10):
    print match
