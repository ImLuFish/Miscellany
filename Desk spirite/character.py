import pygame
from pygame.locals import *
import pandas as pd
import random

standnum = 271


class Kalsit(pygame.sprite.Sprite):
    def __init__(self, screen, rect):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.rect = rect

        self.init_stand()
        self.status = 'stand'

    def init_stand(self):
        self.img_stand = {}
        for i in range(standnum):
            i += 1
            self.img_stand[i] = pygame.transform.scale(pygame.image.load("E://game project//姿势存储//kalsit stand//stand (%s).png" % i), (300, 300))
        self.num_stand = 1

    def refresh_stand(self):
        self.screen.blit(self.img_stand[self.num_stand], self.rect)
        self.num_stand += 1
        if self.num_stand % (standnum + 1) == 0:
            self.num_stand = 1

    def refresh(self):
        if self.status == 'stand':
            self.refresh_stand()