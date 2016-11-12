import cv2
import preprocess
import compare
import os

# create a preprocess object with img size 200x200
img_size = 100
n_angles = 4
test_size = 2000
# dir = "101_ObjectCategories"
dir = 'Images'
pre = preprocess.Preprocess(img_size,n_angles)
lookup = []

for subdir, dirs, files in os.walk(dir):
    for file in files:
        filename = os.path.join(subdir, file)
        if filename[-3:] == 'jpg':
            raw_img = cv2.imread(filename, 0)
            pre.process_img(raw_img)
            lookup.append(filename)
            print len(lookup)
    #     if len(lookup) > test_size:
    #         break
    # if len(lookup) > test_size:
    #     break

raw_img = cv2.imread('hearts.jpg', 0)

query_set = pre.get_edgels(raw_img)

top_matches = compare.query_compare(query_set, pre.get_hitmap(), pre.get_hitcounts())
top_filenames = map(lambda x: lookup[x[0]], top_matches)
for match in top_filenames:
    print match
print "================================================================"
top_imgs = map(lambda x: cv2.imread(x, 0), top_filenames)
top_matches2 = compare.database_compare(top_imgs, top_matches, raw_img, 50, img_size ,n_angles)

for match in top_matches2:
    print top_filenames[match[0]]