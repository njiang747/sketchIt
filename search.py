import cv2
import preprocess
import compare
import os
import database


class Search:

    def __init__(self, directory, load_file=None):
        self.img_size = 100
        self.n_angles = 6
        direc = directory

        self.pre = preprocess.Preprocess(self.img_size, self.n_angles)
        self.lookup = []

        for subdir, dirs, files in os.walk(direc):
            for f in files:
                filename = os.path.join(subdir, f)
                if filename[-3:] == 'jpg':
                    if not load_file:
                        raw_img = cv2.imread(filename, 0)
                        self.pre.process_img(raw_img)
                    self.lookup.append(filename)
                    print '%i:\t%s' % (len(self.lookup), filename)
        if load_file:
            edgel_counts = database.load_data(self.pre.hits, load_file)
            self.pre.set_edgel_counts(edgel_counts)

    def top_n_mult(self, img, n, tag=None):
        num_imgs = 100
        query_set = self.pre.get_edgels(img)
        if (tag == None):
            idxs, query_scores = compare.query_compare(query_set, self.pre.get_hitmap(), self.pre.get_edgel_counts(),
                                                       num_imgs)
        else:
            idxs, query_scores = compare.query_compare(query_set, self.pre.get_hitmap(), self.pre.get_edgel_counts(),
                                                       num_imgs, tag, self.lookup)
        top_filenames = map(lambda x: self.lookup[x], idxs)
        top_imgs = map(lambda x: cv2.imread(x, 0), top_filenames)
        database_scores = compare.database_compare(top_imgs, img, self.img_size, self.n_angles)
        num_imgs = min(num_imgs, len(idxs))
        top_matches = [(idxs[i],query_scores[i] * database_scores[i]) for i in range(0, num_imgs)]
        top_fileidxs = map(lambda x: x[0], sorted(top_matches,key=lambda x: x[1],reverse=True))
        return map(lambda x: self.lookup[x], top_fileidxs[0:n])

    def top_n_add(self, img, n, tag=None):
        num_imgs = 100
        query_set = self.pre.get_edgels(img)
        if(tag == None):
            idxs, query_scores = compare.query_compare(query_set, self.pre.get_hitmap(), self.pre.get_edgel_counts(),
                                                       num_imgs)
        else:
            idxs, query_scores = compare.query_compare(query_set, self.pre.get_hitmap(), self.pre.get_edgel_counts(), num_imgs, tag, self.lookup)
        top_filenames = map(lambda x: self.lookup[x], idxs)
        top_imgs = map(lambda x: cv2.imread(x, 0), top_filenames)
        database_scores = compare.database_compare(top_imgs, img, self.img_size, self.n_angles)
        num_imgs = min(num_imgs, len(idxs))
        top_matches = [(idxs[i],query_scores[i] + database_scores[i]) for i in range(0, num_imgs)]
        top_fileidxs = map(lambda x: x[0], sorted(top_matches,key=lambda x: x[1],reverse=True))
        return map(lambda x: self.lookup[x], top_fileidxs[0:n])
