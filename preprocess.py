import cv2
import numpy as np
from scipy.ndimage.filters import sobel
import time


# resizes an image up to max_dim
def resize(img, max_dim):
    r, c = img.shape
    fac = float(max_dim) / max(r, c)
    img2 = cv2.resize(img, None, fx=fac, fy=fac)
    return img2


def quantize(angle):
    angle2 = (angle + 15) % 180
    return int(angle2) / 30


def q_grad(img):
    dx = sobel(img, axis=0, mode='constant')
    dy = sobel(img, axis=1, mode='constant')
    grad = np.arctan2(dy, dx) * 180 / np.pi
    quantizer = np.vectorize(quantize)
    return quantizer(grad)


def splat(img_id, r, c, theta, radius):
    for i in range(1, radius + 1):
        for j in range(1, radius + 1 - i):
            if r >= i:
                if c >= j:
                    hits[r-i][c-j][theta].append(img_id)
                if c < i_size-j:
                    hits[r-i][c+j][theta].append(img_id)
            if r < i_size-i:
                if c >= j:
                    hits[r+i][c-j][theta].append(img_id)
                if c < i_size-j:
                    hits[r+i][c+j][theta].append(img_id)
        if r >= i:
            hits[r - i][c][theta].append(img_id)
        if r < i_size-i:
            hits[r + i][c][theta].append(img_id)
        if c >= i:
            hits[r][c - i][theta].append(img_id)
        if c < i_size-i:
            hits[r][c + 1][theta].append(img_id)
        hits[r][c][theta].append(img_id)


# constants
i_size = 200
thresh_l = 100
thresh_h = 200
splat_radius = 4
hits = [[[[] for i in range(0,6)] for j in range(0,i_size)] for k in range(0,i_size)]

start = time.time()

# open the image
raw_img = cv2.imread('butterfly.jpg', 0)
resize_img = resize(raw_img, i_size)

end = time.time()
print end - start
start = end

# calculate the edges of the resized image
canny = cv2.Canny(resize_img, thresh_l, thresh_h)

end = time.time()
print end - start
start = end

edgels = q_grad(resize_img)
e_r, e_c = canny.shape
off_r = (i_size - e_r) / 2
off_c = (i_size - e_c) / 2

end = time.time()
print end - start
start = end

for i, row in enumerate(canny):
    for j, entry in enumerate(row):
        if entry:
            splat(0, i + off_r, j + off_c, edgels[i, j], splat_radius)

end = time.time()
print end - start
start = end

# # fill until 200x200 img
# out_img = np.zeros((i_size,i_size))
# e_r,e_c = edges.shape
# out_img[(i_size-e_r)/2:(i_size+e_r)/2,(i_size-e_c)/2:(i_size+e_c)/2] = edges
#
# # show img
# plt.imshow(out_img,cmap = 'gray')
#
# plt.show()
