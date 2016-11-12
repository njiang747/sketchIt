import cv2
import search

searcher = search.Search('images')

img = cv2.imread('sketches/person.jpg', 0)
print "======================================================="
for match in searcher.top_n_add(img,50):
    print match
print "======================================================="
for match in searcher.top_n_mult(img,50):
    print match
