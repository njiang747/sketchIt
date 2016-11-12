import cv2
import search
from matplotlib import pyplot as plt

searcher = search.Search('Images')

raw_img = cv2.imread('sketches/person.jpg', 0)
for match in searcher.top_n_add(raw_img,50):
    print match
    # img = cv2.imread(match, 0)
    # plt.imshow(img, cmap='gray')
