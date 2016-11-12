import cv2
import preprocess
import compare
import os


class Search:
    def __init__(self, directory):
        self.img_size = 100
        self.n_angles = 4
        dir = directory
        self.pre = preprocess.Preprocess(self.img_size, self.n_angles)
        self.lookup = []

        for subdir, dirs, files in os.walk(dir):
            for file in files:
                filename = os.path.join(subdir, file)
                if filename[-3:] == 'jpg':
                    raw_img = cv2.imread(filename, 0)
                    self.pre.process_img(raw_img)
                    self.lookup.append(filename)
                    print 'Image', len(self.lookup), 'processed'

    def top_n(self, img, n):
        query_set = self.pre.get_edgels(img)
        top_matches = compare.query_compare(query_set, self.pre.get_hitmap(), self.pre.get_hitcounts())
        top_filenames = map(lambda x: self.lookup[x[0]], top_matches)
        top_imgs = map(lambda x: cv2.imread(x, 0), top_filenames)
        top_matches2 = compare.database_compare(top_imgs, top_matches, img, 50, self.img_size, self.n_angles)
        return map(lambda x: top_filenames[x[0]], top_matches2[0:n])
