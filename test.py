import cv2
import search
import database
from matplotlib import pyplot as plt
import pygame
import os

def save_hits():
    database.save_data(searcher.pre.get_hitmap(), searcher.pre.get_edgel_counts(), 'save_state.csv')

def top_hits(filename):
    raw_img = cv2.imread(filename, 0)
    top = searcher.top_n_mult(raw_img, 50)
    for match in top:
        print match
    plt.subplot(2, 3, 1), plt.imshow(raw_img, cmap='gray'), plt.axis('off')
    for i,match in enumerate(top[:5]):
        plt.subplot(2,3,i+2), plt.imshow(cv2.cvtColor(cv2.imread(match,1), cv2.COLOR_BGR2RGB)), plt.axis('off')
    plt.show()

if os.path.isfile('save_state.csv'):
    searcher = search.Search('images', 'save_state.csv')
else:
    searcher = search.Search('images')
    save_hits()

while True:
    screen = pygame.display.set_mode((800, 800))

    draw_on = False
    last_pos = (0, 0)
    color = (255, 255, 255)
    radius = 2

    def roundline(srf, color, start, end, radius=1):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int(start[0] + float(i) / distance * dx)
            y = int(start[1] + float(i) / distance * dy)
            pygame.draw.circle(srf, color, (x, y), radius)

    try:
        while True:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                # color = (random.randrange(256), random.randrange(256), random.randrange(256))
                pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, color, e.pos, radius)
                    roundline(screen, color, e.pos, last_pos, radius)
                last_pos = e.pos
            pygame.display.flip()


    except StopIteration:
        pass
    pygame.image.save(screen, 'temp.jpg')
    _img = open('temp.jpg', 'rb')
    _out = _img.read()
    _img.close()
    pygame.quit()

    top_hits('temp.jpg')
    cv2.waitKey(0)
