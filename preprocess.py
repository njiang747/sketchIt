import numpy as np
import cv2
from scipy.ndimage.filters import sobel


class Preprocess:
    # initialize a preprocess object given the size of the images
    def __init__(self, size, n_angles):
        self.i_size = size
        self.angles = n_angles
        self.thresh_l = 100
        self.thresh_h = 200
        self.splat_radius = 4
        self.hitcounts = []
        self.hits = [[[set() for i in range(0, n_angles)] for j in range(0, self.i_size)] for k in range(0, self.i_size)]

    # process an image and update the hitmap with its img id
    def process_img(self, raw_img):
        # increment number of img_hits
        self.hitcounts.append(1.0)
        # resize the image
        resize_img = self.resize(raw_img)
        # calculate the edges of the resized image
        canny = cv2.Canny(resize_img, self.thresh_l, self.thresh_h)
        # calculate the edgels grid
        edgels = self.q_grad(resize_img)
        # update the hit map
        e_r, e_c = canny.shape
        off_r = (self.i_size - e_r) / 2
        off_c = (self.i_size - e_c) / 2
        for i, row in enumerate(canny):
            for j, entry in enumerate(row):
                if entry:
                    self.splat(len(self.hitcounts)-1, i + off_r, j + off_c, edgels[i, j])
                    self.hitcounts[-1] += 1

    # get the edgels of an img
    def get_edgels(self, raw_img):
        # resize the image
        resize_img = self.resize(raw_img)
        # calculate the edges of the resized image
        canny = cv2.Canny(resize_img, self.thresh_l, self.thresh_h)
        # calculate the edgels grid
        edgels = self.q_grad(resize_img)
        # return the list of edgels
        e_r, e_c = canny.shape
        off_r = (self.i_size - e_r) / 2
        off_c = (self.i_size - e_c) / 2
        edgel_list = []
        for i, row in enumerate(canny):
            for j, entry in enumerate(row):
                if entry:
                    edgel_list.append((i + off_r, j + off_c, edgels[i, j]))
        return edgel_list

    # return the hitmap
    def get_hitmap(self):
        return self.hits

    # return the list of number of image hits
    def get_hitcounts(self):
        return self.hitcounts

    # resizes an image up to max_dim
    def resize(self, img):
        r, c = img.shape
        fac = float(self.i_size) / max(r, c)
        img2 = cv2.resize(img, None, fx=fac, fy=fac)
        return img2

    # compute the grid of quantized angle bin numbers
    def q_grad(self, img):
        img2 = cv2.GaussianBlur(img, (5, 5), 3)
        dx = sobel(img2, axis=0, mode='constant')
        dy = sobel(img2, axis=1, mode='constant')
        grad = np.arctan2(dy, dx) * 180 / np.pi
        quantizer = np.vectorize(self.quantize)
        return quantizer(grad)

    # add img_id to the hitmap entries radius r around r, c, theta
    def splat(self, img_id, r, c, theta):
        for i in range(1, self.splat_radius + 1):
            for j in range(1, self.splat_radius + 1 - i):
                if r >= i:
                    if c >= j:
                        self.hits[r - i][c - j][theta].add(img_id)
                    if c < self.i_size - j:
                        self.hits[r - i][c + j][theta].add(img_id)
                if r < self.i_size - i:
                    if c >= j:
                        self.hits[r + i][c - j][theta].add(img_id)
                    if c < self.i_size - j:
                        self.hits[r + i][c + j][theta].add(img_id)
            if r >= i:
                self.hits[r - i][c][theta].add(img_id)
            if r < self.i_size - i:
                self.hits[r + i][c][theta].add(img_id)
            if c >= i:
                self.hits[r][c - i][theta].add(img_id)
            if c < self.i_size - i:
                self.hits[r][c + 1][theta].add(img_id)
            self.hits[r][c][theta].add(img_id)

    # quantize the angle (-pi,pi) into one of self.angles bins
    def quantize(self, angle):
        angle2 = (angle + 90/self.angles) % 180
        return int(angle2 / (180.0 / self.angles))
