from matplotlib import pyplot as plt
import cv2
import preprocess
import numpy as np

class Debug:
    def __init__(self, fname1, fname2):
        self.img_size = 100
        self.n_angles = 4
        self.pre = preprocess.Preprocess(self.img_size,self.n_angles)
        self.test_img = np.zeros((self.n_angles,self.img_size,self.img_size))

        query_img = cv2.imread(fname1, 0)
        database_img = cv2.imread(fname2, 0)

        self.query_set = self.pre.get_edgels(query_img)
        self.pre.process_img(database_img)
        self.hitmap = self.pre.get_hitmap()

        for i,r in enumerate(self.hitmap):
            for j,c in enumerate(r):
                for theta,entry in enumerate(c):
                    if len(entry) > 0:
                        self.test_img[theta,i,j] = 128

        for i, j, theta in self.query_set:
            self.test_img[theta,i,j] = 255

    def show(self):
        for i,v in enumerate(self.test_img):
            plt.subplot(2,self.n_angles/2,i+1),plt.imshow(self.test_img[i],cmap = 'gray')

        plt.show()

    def show_query_flat(self):
        test_img = np.zeros((self.img_size,self.img_size))
        for i, j, theta in self.query_set:
            test_img[i,j] = 255
        plt.imshow(test_img,cmap='gray')


deb = Debug('sketches/banana.jpg','images/banana/image93.jpg')
deb.show()