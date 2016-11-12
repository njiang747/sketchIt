import cv2
import preprocess
import compare
import os

# create a preprocess object with img size 200x200
img_size = 200
pre = preprocess.Preprocess(img_size)
lookup = []

for subdir, dirs, files in os.walk("101_ObjectCategories"):
    for file in files:
        filename = os.path.join(subdir, file)
        if filename[-3:] == 'jpg':
            raw_img = cv2.imread(filename, 0)
            pre.process_img(raw_img, len(lookup))
            lookup.append(filename)
            print len(lookup)
        if len(lookup) > 1000:
            break
    if len(lookup) > 1000:
        break

raw_img = cv2.imread('anchor.jpg', 0)

query_set = pre.get_edgels(raw_img)

top_matches = compare.query_compare(query_set, pre.get_hitmap(), len(lookup))
for match in top_matches:
    print lookup[match]
print "================================================================"
top_filenames = map(lambda x: lookup[x], top_matches)
for match in top_filenames:
    print match
print "================================================================"
top_imgs = map(lambda x: cv2.imread(x, 0), top_filenames)
top_matches = compare.database_compare(top_imgs, raw_img, 50, img_size)

for match in top_matches:
    print top_filenames[match]