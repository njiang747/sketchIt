import cv2
import search
import database
from matplotlib import pyplot as plt
import pygame
import os

def save_hits():
    database.save_data(searcher.pre.get_hitmap(), searcher.pre.get_edgel_counts(), 'save_state.csv')

def top_hits(filename, tag=None):
    raw_img = cv2.imread(filename, 0)
    top = searcher.top_n_mult(raw_img, 50, tag)
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


pygame.init()
screen = pygame.display.set_mode((800, 800))

draw_on = False
last_pos = (0, 0)
color = (255, 255, 255)
black = (0, 0, 0)
radius = 2
sketch = pygame.Surface(screen.get_size())
sketch = sketch.convert()
sketch.fill(black)
tag_text = ''
font = pygame.font.SysFont('segoeui', 48)
text = font.render(tag_text, 1, (0,255,255))
textpos = text.get_rect()

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
            pygame.draw.circle(sketch, color, e.pos, radius)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(sketch, color, e.pos, radius)
                roundline(sketch, color, e.pos, last_pos, radius)
            last_pos = e.pos
        if e.type == pygame.KEYDOWN:
            if e.key == 13:
                pygame.image.save(sketch, 'temp.jpg')
                text2 = font.render("Searching for Matches...", 1, (128,128,128))
                textpos2 = text2.get_rect()
                textpos2.centerx = screen.get_rect().centerx
                textpos2.centery = 50
                screen.blit(sketch, (0,0))
                screen.blit(text2, textpos2)
                pygame.display.flip()
                if len(tag_text) > 0:
                    top_hits('temp.jpg', tag_text)
                else:
                    top_hits('temp.jpg')
                tag_text = ''
                text = font.render(tag_text, 1, (128,128,128))
                screen.fill(black)
                sketch.fill(black)
            elif e.key in range(256) and (chr(e.key).isalpha() or e.key == 32):
                tag_text += chr(e.key)
                text = font.render(tag_text, 1, (128,128,128))
                textpos = text.get_rect()
                textpos.centerx = screen.get_rect().centerx
                textpos.centery = 50
            elif e.key == 8:
                tag_text = tag_text[:-1]
                text = font.render(tag_text, 1, (128,128,128))
                textpos = text.get_rect()
                textpos.centerx = screen.get_rect().centerx
                textpos.centery = 50

        screen.blit(sketch, (0,0))
        screen.blit(text, textpos)
        pygame.display.flip()


except StopIteration:
    pass
pygame.image.save(screen, 'temp.jpg')
pygame.quit()
