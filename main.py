#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys, pygame, random, linecache
from sys import exit
from pygame import *
from random import *
from linecache import getline
#kolory
czarny = (0, 0, 0)
bialy = (255, 255, 255)
czerwony = (255, 0, 0)
zielony = (0, 255, 0)
niebieski = (0, 0, 255)
clock = pygame.time.Clock()
class Game(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen_size=self.screen_width,self.screen_height=1000, 600
        self.screen = pygame.display.set_mode(self.screen_size, DOUBLEBUF)
        pygame.display.set_caption("Curve fever")
        self.segment = pygame.image.load("assets/segment.png").convert_alpha()
        self.glowa = pygame.image.load("assets/head.png").convert_alpha()
        self.ziemia = pygame.image.load("assets/underground.png").convert()
        self.pajak1 = pygame.image.load("assets/spider_1.png").convert_alpha()
        self.pajak2 = pygame.image.load("assets/spider_2.png").convert_alpha()
        self.pajak3 = pygame.image.load("assets/spider_3.png").convert_alpha()
        self.pajak4 = pygame.image.load("assets/spider_4.png").convert_alpha()
        self.punkt = pygame.image.load("assets/point.png").convert_alpha()
        self.serce = pygame.image.load("assets/heart.png").convert_alpha()
        self.music_score = pygame.mixer.music.load("sounds/score.mp3")
        self.gamestate = 4
        self.ltlo = [self.ziemia]
        self.pajak = self.pajak4
        self.ltlo_x = [0]
        self.is_music = 'ON'
        self.fps = 30
        self.menu()
    def game_exit(self):
        pygame.quit()
        exit()
    def collision_square(self,list_x_player, list_y_player, i, x1, y1, x2, y2):
        if self.points_x[-1] - (list_x_player[i] + 110) > 0:
            return False
        if list_x_player[i] - (self.points_x[-1] + 42) > 0:
            return False
        if self.points_y[-1] - (list_y_player[i] + 128) > 0:
            return False
        if list_y_player[i] - (self.points_y[-1] + 32) > 0:
            return False
        return True
    def collision_circle_square(self, i):
        px = self.lscore_x[i]
        py = self.lscore_y[i]
        if (self.points_x[-1] + 42) < self.lscore_x[i]:
            px = self.points_x[-1] + 42
        if self.points_x[-1] > (self.lscore_x[i] + 32):
            px = self.points_x[-1]
        if (self.points_y[-1] + 32) < self.lscore_y[i]:
            py = self.points_y[-1] + 32
        if self.points_y[-1] > (self.lscore_y[i] + 32):
            py = self.points_y[-1] + 32
        if ((self.lscore_x[i] - px)**2 + (self.lscore_y[i] - py)**2) < (32**2):
            return True
        return False
    def new_pos_spr(self, listx, listy, x, y):
        listy.append(randint(0,y - 40))
        listx.append(x - 40)
    def move_spr(self, lista, i, ile):
        lista[i] -= ile
    def move_player(self):
        key = pygame.key.get_pressed()
        if key[K_DOWN] and self.player_y < 526:
            self.player_y += 7
        if key[K_UP] and self.player_y > 0:
            self.player_y -= 7
    def text_center(self, tekst, size, color, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(tekst, True, color)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text, text_rect)
    def text(self, tekst, size, color, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(tekst, True, color)
        self.screen.blit(text, (x,y))
    def new_score(self, score, plik):
        self.scores = open(plik, 'r').read()
        self.list_scores = self.scores.split('=')
        if int(self.list_scores[0]) < score:
            self.list_scores[0] = str(score)
            open(plik, 'w').write(self.list_scores[0]+'='+self.list_scores[1]+'='+self.list_scores[2]+'='+self.list_scores[3]+'='+self.list_scores[4])
        elif int(self.list_scores[1]) < score:
            self.list_scores[1] = str(score)
            open(plik, 'w').write(self.list_scores[0]+'='+self.list_scores[1]+'='+self.list_scores[2]+'='+self.list_scores[3]+'='+self.list_scores[4])
        elif int(self.list_scores[2]) < score:
            self.list_scores[2] = str(score)
            open(plik, 'w').write(self.list_scores[0]+'='+self.list_scores[1]+'='+self.list_scores[2]+'='+self.list_scores[3]+'='+self.list_scores[4])
        elif int(self.list_scores[3]) < score:
            self.list_scores[3] = str(score)
            open(plik, 'w').write(self.list_scores[0]+'='+self.list_scores[1]+'='+self.list_scores[2]+'='+self.list_scores[3]+'='+self.list_scores[4])
        elif int(self.list_scores[4]) < score:
            self.list_scores[4] = str(score)
            open(plik, 'w').write(self.list_scores[0]+'='+self.list_scores[1]+'='+self.list_scores[2]+'='+self.list_scores[3]+'='+self.list_scores[4])
        else:
            open(plik, 'w').write(self.list_scores[0]+'='+self.list_scores[1]+'='+self.list_scores[2]+'='+self.list_scores[3]+'='+self.list_scores[4])
    def show_wyniki(self, plik):
        self.open = open(plik, 'r')
        self.read = self.open.read()
        self.wyniki = self.read.split('=')
        self.open.close()
        while self.gamestate == 6:
            for event in pygame.event.get():
                if event.type==QUIT:
                    self.game_exit()
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    self.gamestate = 1
                    self.wyniki_menu()
            self.text(u'1. miejse: '+self.wyniki[0]+' monet', 35, (0,0,0), 453, 283)
            self.text(u'1. miejse: '+self.wyniki[0]+' monet', 35, (80,80,255), 450, 280)
            self.text(u'2. miejse: '+self.wyniki[1]+' monet', 35, (0,0,0), 453, 323)
            self.text(u'2. miejse: '+self.wyniki[1]+' monet', 35, (80,80,255), 450, 320)
            self.text(u'3. miejse: '+self.wyniki[2]+' monet', 35, (0,0,0), 453, 363)
            self.text(u'3. miejse: '+self.wyniki[2]+' monet', 35, (80,80,255), 450, 360)
            self.text(u'4. miejse: '+self.wyniki[3]+' monet', 35, (0,0,0), 453, 403)
            self.text(u'4. miejse: '+self.wyniki[3]+' monet', 35, (80,80,255), 450, 400)
            self.text(u'5. miejse: '+self.wyniki[4]+' monet', 35, (0,0,0), 453, 443)
            self.text(u'5. miejse: '+self.wyniki[4]+' monet', 35, (80,80,255), 450, 440)
            display.flip()
            display.update()
    def wyniki_menu(self):
        self.cur_lvl = 0
        while self.gamestate == 1:
            for event in pygame.event.get():
                if event.type==QUIT:
                    self.game_exit()
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    self.gamestate = 4
                    self.menu()
                if event.type==KEYDOWN and event.key==K_RETURN:
                    if self.cur_lvl == 4:
                        self.gamestate = 4
                        self.menu()
                    else:
                        self.gamestate = 6
                        if self.cur_lvl == 0:
                            self.show_wyniki("scores/easy.txt")
                        elif self.cur_lvl == 1:
                            self.show_wyniki("scores/medium.txt")
                        elif self.cur_lvl == 2:
                            self.show_wyniki("scores/hard.txt")
                        elif self.cur_lvl == 3:
                            self.show_wyniki("scores/expert.txt")
                if event.type==KEYDOWN:
                    if event.key==K_UP:
                            self.cur_lvl -= 1
                            if self.cur_lvl == -1:
                                self.cur_lvl = 4
                    if event.key==K_DOWN:
                        self.cur_lvl += 1
                        if self.cur_lvl == 5:
                            self.cur_lvl = 0
            self.screen.fill((250,150,50))
            self.screen.blit(self.ziemia,(0,0))
            self.tekst_menu()
            pygame.draw.polygon(self.screen, (0,0,0),((368,23),(373,23),(373,583),(368,583)),0)
            pygame.draw.polygon(self.screen, (0,175,0),((365,20),(370,20),(370,580),(365,580)),0)
            self.text(u'Oto twoje wyniki:', 60, (0,0,0), 403, 23)
            self.text(u'Oto twoje wyniki:', 60, (80,80,255), 400, 20)
            self.text(u'Poziom łatwy', 45, (0,0,0), 433, 83)
            self.text(u'Poziom łatwy', 45, (80,80,255), 430, 80)
            self.text(u'Poziom średni', 45, (0,0,0), 433, 133)
            self.text(u'Poziom średni', 45, (80,80,255), 430, 130)
            self.text(u'Poziom trudny', 45, (0,0,0), 433, 183)
            self.text(u'Poziom trudny', 45, (80,80,255), 430, 180)
            self.text(u'Poziom eksperymentalny', 45, (0,0,0), 433, 233)
            self.text(u'Poziom eksperymentalny', 45, (80,80,255), 430, 230)
            self.text(u'Powrót', 60, (0,0,0), 453, 503)
            self.text(u'Powrót', 60, (80,80,255), 450, 500)
            if self.cur_lvl == 4:
                pygame.draw.polygon(self.screen, (0,0,0), ((413,503),(443,523),(413,543)), 0)
                pygame.draw.polygon(self.screen, (80,80,255), ((410,500),(440,520),(410,540)), 0)
            else:
                pygame.draw.polygon(self.screen, (0,0,0), ((403,50*self.cur_lvl +83),(423,50*self.cur_lvl +93),(403,50*self.cur_lvl +103)), 0)
                pygame.draw.polygon(self.screen, (80,80,255), ((400,50*self.cur_lvl +80),(420,50*self.cur_lvl +90),(400,50*self.cur_lvl +100)), 0)
            display.flip()
            display.update()
    def pomoc(self):
        while self.gamestate == 3:
            for event in pygame.event.get():
                if event.type==QUIT:
                    self.game_exit()
                if (event.type==KEYDOWN and event.key==K_RETURN) or (event.type==KEYDOWN and event.key==K_ESCAPE):
                    self.gamestate = 4
                    self.menu()
            self.screen.fill((250,150,50))
            self.screen.blit(self.ziemia,(0,0))
            self.tekst_menu()
            pygame.draw.polygon(self.screen, (0,0,0),((368,23),(373,23),(373,583),(368,583)),0)
            pygame.draw.polygon(self.screen, (0,175,0),((365,20),(370,20),(370,580),(365,580)),0)
            self.text(u'Twoim zadaniem jest zebranie jak', 45, (0,0,0), 403, 23)
            self.text(u'największej ilości monet i ominięcie', 45, (0,0,0), 403, 73)
            self.text(u'wszystkich pająków.', 45, (0,0,0), 403, 123)
            self.text(u'Twoim zadaniem jest zebranie jak', 45, (80,80,255), 400, 20)
            self.text(u'największej ilości monet i ominięcie', 45, (80,80,255), 400, 70)
            self.text(u'wszystkich pająków.', 45, (80,80,255), 400, 120)
            self.text(u'Tak wygląda moneta:', 45, (0,0,0), 403, 203)
            self.text(u'Tak wygląda moneta:', 45, (80,80,255), 400, 200)
            self.screen.blit(self.punkt, (720, 200))
            self.text(u'Tak wygląda pająk:', 45, (0,0,0), 403, 313)
            self.text(u'Tak wygląda pająk:', 45, (80,80,255), 400, 310)   
            self.screen.blit(self.pajak, (710, 260))
            if self.pajak == self.pajak1:
                self.pajak = self.pajak2
            elif self.pajak == self.pajak2:
                self.pajak = self.pajak3
            elif self.pajak == self.pajak3:
                self.pajak = self.pajak4
            else:
                self.pajak = self.pajak1
            self.text(u'Powrót', 60, (0,0,0), 453, 503)
            self.text(u'Powrót', 60, (80,80,255), 450, 500)
            pygame.draw.polygon(self.screen, (0,0,0), ((425,505),(445,520),(425,535)), 0)
            pygame.draw.polygon(self.screen, (80,80,255), ((420,500),(440,515),(420,530)), 0)
            display.flip()
            display.update()
    def ustawienia(self):
        self.options = 0
        while self.gamestate == 2:
            for event in pygame.event.get():
                if event.type==QUIT:
                    self.game_exit()
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    self.gamestate = 4
                    self.menu()
                if event.type==KEYDOWN and event.key==K_RETURN:
                    if self.options == 0:
                        if self.is_music == "ON":
                            self.is_music = "OFF"
                        else:
                            self.is_music = "ON"
                    elif self.options == 1:
                        self.gamestate = 4
                        self.menu()
                if event.type==KEYDOWN:
                    if event.key==K_UP:
                            self.options -= 1
                            if self.options == -1:
                                self.options = 1
                    if event.key==K_DOWN:
                        self.options += 1
                        if self.options == 2:
                            self.options = 0
            self.screen.fill((250,150,50))
            self.screen.blit(self.ziemia,(0,0))
            pygame.draw.polygon(self.screen, (0,0,0),((368,23),(373,23),(373,583),(368,583)),0)
            pygame.draw.polygon(self.screen, (0,175,0),((365,20),(370,20),(370,580),(365,580)),0)
            if self.is_music == "ON":
                self.text(u'Muzyka: ', 60, (0,0,0), 453, 23)
                self.text(u'Muzyka: ', 60, (80,80,255), 450, 20)
                self.text(self.is_music, 60, (0,0,0), 633, 23)
                self.text(self.is_music, 60, (0,175,0), 630, 20)
            else:
                self.text(u'Muzyka: ', 60, (0,0,0), 453, 23)
                self.text(u'Muzyka: ', 60, (80,80,255), 450, 20)
                self.text(self.is_music, 60, (0,0,0), 633, 23)
                self.text(self.is_music, 60, (175,0,0), 630, 20)
            self.text(u'Powrót', 60, (0,0,0), 453, 503)
            self.text(u'Powrót', 60, (80,80,255), 450, 500)
            if self.options == 1:
                pygame.draw.polygon(self.screen, (0,0,0), ((413,503),(443,523),(413,543)), 0)
                pygame.draw.polygon(self.screen, (80,80,255), ((410,500),(440,520),(410,540)), 0)
            else:
                pygame.draw.polygon(self.screen, (0,0,0), ((413,20 *self.options +23),(443,20 *self.options+43),(413,20 *self.options+63)), 0)
                pygame.draw.polygon(self.screen, (80,80,255), ((410,20 *self.options +20),(440,20 *self.options+40),(410,20 *self.options+60)), 0)
            self.tekst_menu()
            display.flip()
            display.update()
    def start_lvl(self):
        self.lvl = 0
        while self.gamestate == 0:
            for event in pygame.event.get():
                if event.type==QUIT:
                    self.game_exit()
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    self.gamestate = 4
                    self.menu()
                if event.type==KEYDOWN and event.key==K_RETURN:
                    if self.lvl == 4:
                        self.gamestate = 4
                        self.menu()
                    else:
                        self.time_start = pygame.time.get_ticks()
                        self.gamestate = 5
                        self.start()
                if event.type==KEYDOWN:
                    if event.key==K_UP:
                            self.lvl -= 1
                            if self.lvl == -1:
                                self.lvl = 4
                    if event.key==K_DOWN:
                        self.lvl += 1
                        if self.lvl == 5:
                            self.lvl = 0
            self.screen.fill((250,150,50))
            self.screen.blit(self.ziemia,(0,0))
            pygame.draw.polygon(self.screen, (0,0,0),((368,23),(373,23),(373,583),(368,583)),0)
            pygame.draw.polygon(self.screen, (0,175,0),((365,20),(370,20),(370,580),(365,580)),0)
            self.text(u'Wybierz poziom trudności:', 50, (0,0,0), 403, 23)
            self.text(u'Wybierz poziom trudności:', 50, (80,80,255), 400, 20)
            self.text(u'Łatwy:', 45, (0,0,0), 443, 73)
            self.text(u'Łatwy:', 45, (80,80,255), 440, 70)
            self.text(u'Jedno życie, maks. 10 monet', 45, (0,0,0), 443, 123)
            self.text(u'Jedno życie, maks. 10 monet', 45, (160,160,255), 440, 120)
            self.text(u'Średni:', 45, (0,0,0), 443, 173)
            self.text(u'Średni:', 45, (80,80,255), 440, 170)
            self.text(u'Trzy życia, maks. 20 monet', 45, (0,0,0), 443, 223)
            self.text(u'Trzy życia, maks. 20 monet', 45, (160,160,255), 440, 220)
            self.text(u'Trudny:', 45, (0,0,0), 443, 273)
            self.text(u'Trudny:', 45, (80,80,255), 440, 270)
            self.text(u'Pięć żyć, maks. 30 monet', 45, (0,0,0), 443, 323)
            self.text(u'Pięć żyć, maks. 30 monet', 45, (160,160,255), 440, 320)
            self.text(u'Eksperymentalny:', 45, (0,0,0), 443, 373)
            self.text(u'Eksperymentalny:', 45, (80,80,255), 440, 370)
            self.text(u'Trzy życia, mega szybkość', 45, (0,0,0), 443, 423)
            self.text(u'Trzy życia, mega szybkość', 45, (160,160,255), 440, 420)
            self.text(u'Powrót', 60, (0,0,0), 453, 503)
            self.text(u'Powrót', 60, (80,80,255), 450, 500)
            self.tekst_menu()
            if self.lvl == 4:
                pygame.draw.polygon(self.screen, (0,0,0), ((413,503),(443,523),(413,543)), 0)
                pygame.draw.polygon(self.screen, (80,80,255), ((410,500),(440,520),(410,540)), 0)
            else:
                pygame.draw.polygon(self.screen, (0,0,0), ((413,self.lvl * 100 + 73),(433,self.lvl * 100 + 88),(413,self.lvl * 100 + 103)), 0)
                pygame.draw.polygon(self.screen, (80,80,255), ((410,self.lvl * 100 + 70),(430,self.lvl * 100 + 85),(410,self.lvl * 100 + 100)), 0)
            display.flip()
            display.update()
    def tekst_menu(self):
        self.text(u'Rozpocznij grę', 55, (0,0,0), 44,24)
        self.text(u'Rozpocznij grę', 55, (255,50,150), 40,20)
        self.text(u'Wyniki', 55, (0,0,0), 44,74)
        self.text(u'Wyniki', 55, (255,50,150), 40,70)
        self.text(u'Ustawienia', 55, (0,0,0), 44,124)
        self.text(u'Ustawienia', 55, (255,50,150), 40,120)
        self.text(u'Jak grać ?', 55, (0,0,0), 44,174)
        self.text(u'Jak grać ?', 55, (255,50,150), 40,170)
        self.text(u'Wyjście', 55, (0,0,0), 44,224)
        self.text(u'Wyjście', 55, (255,50,150), 40,220)
        self.text(u'Strzałki - nawigacja', 30, czarny, 23, 523)
        self.text(u'Strzałki - nawigacja', 30, (200,255,200), 20, 520)
        self.text(u'Enter - potwierdzenie', 30, czarny, 23, 548)
        self.text(u'Enter - potwierdzenie', 30, (200,255,200), 20, 545)
        self.text(u'Escape - powrót', 30, czarny, 23, 573)
        self.text(u'Escape - powrót', 30, (200,255,200), 20, 570)
    def menu(self):
        self.cur_option = 0
        while self.gamestate == 4:
            for event in pygame.event.get():
                if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                    self.gamestate = 0
                if event.type == KEYDOWN:
                    if event.key==K_RETURN:
                        if self.cur_option == 0:
                            self.gamestate = 0
                            self.start_lvl()
                        elif self.cur_option == 1:
                            self.gamestate = 1
                            self.wyniki_menu() 
                        elif self.cur_option == 2:
                            self.gamestate = 2
                            self.ustawienia()
                        elif self.cur_option == 3:
                            self.gamestate = 3
                            self.pomoc()
                        elif self.cur_option == 4:
                            self.game_exit()
                    if event.key==K_UP:
                        self.cur_option -= 1
                        if self.cur_option == -1:
                            self.cur_option = 4
                    if event.key==K_DOWN:
                        self.cur_option += 1
                        if self.cur_option == 5:
                            self.cur_option = 0
            self.screen.fill((250,150,50))
            self.screen.blit(self.ziemia,(0,0))
            self.tekst_menu()
            pygame.draw.polygon(self.screen, (0,0,0), ((14,51 * self.cur_option +20),(34,51 * self.cur_option + 36),(14,51 * self.cur_option +49)), 0)
            pygame.draw.polygon(self.screen, (255,50,150), ((10,51 * self.cur_option + 19),(30,51 * self.cur_option+32),(10,51 * self.cur_option+45)), 0)
            display.flip()
            display.update()
        if self.gamestate == 0:
            self.game_exit()
    def start(self):
        self.timer = 1
        self.count = 0
        self.is_live_score = 1
        self.is_live_sprite = 1
        self.is_live_lives = 1
        self.lsprite_y = []
        self.lsprite_x = []
        self.lscore_y = []
        self.lscore_x = []
        self.llives_x = []
        self.llives_y = []
        self.player_x = 0
        self.player_y = 300
        self.points_x = [self.player_x]
        self.points_y = [self.player_y]
        if self.lvl == 0:
            self.lives = 5
            self.fps = 35
        elif self.lvl == 1:
            self.lives = 3
            self.fps = 35
        elif self.lvl == 2:
            self.lives = 1
            self.fps = 35
        else:
            self.lives = 3
            self.fps = 80
        for i in range(self.lvl *20 +20):
            self.new_pos_spr(self.lsprite_x, self.lsprite_y, 1100, 472)
            if i % 2 == 0:
                self.new_pos_spr(self.lscore_x, self.lscore_y, 1100, 568)
                if i % 10 == 0:
                    self.new_pos_spr(self.llives_x, self.llives_y, 1100, 500)
        self.music_countdown = pygame.mixer.music.load("sounds/countdown.mp3")
        if self.is_music == "ON":
            pygame.mixer.music.play(1)
        while self.gamestate == 5:
            for event in pygame.event.get():
                if event.type==QUIT:
                    self.game_exit()
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    self.gamestate = 4
                    self.menu()
            
            self.time_game = pygame.time.get_ticks()
            self.time = self.time_game - self.time_start
            clock.tick(self.fps)
            if self.timer == 1:
                self.move_player()
            self.screen.fill((czarny))
            
            #tło
            if self.ltlo_x[0] == 0:
                self.ltlo_x.append(1000)
            if self.ltlo_x[0] == -1000:
                self.ltlo_x.pop(0)
            for i in range(len(self.ltlo_x)):
                self.screen.blit(self.ziemia, (self.ltlo_x[i], -40))
                self.ltlo_x[i] -= 1
            if self.ltlo_x[0] == -1000:
                self.ltlo_x.pop(0)
            
            #pajaki
            if self.time > 7000 and len(self.lsprite_x) > 0:    
                self.move_spr(self.lsprite_x, 0, 18)
                if self.is_live_sprite == 1:
                    self.screen.blit(self.pajak, (self.lsprite_x[0], self.lsprite_y[0]))
                if self.lsprite_x[0] < -128:
                   self.lsprite_x.pop(0)
                   self.lsprite_y.pop(0)
                   self.is_live_sprite = 1
            if self.pajak == self.pajak1:
                self.pajak = self.pajak2
            elif self.pajak == self.pajak2:
                self.pajak = self.pajak3
            elif self.pajak == self.pajak3:
                self.pajak = self.pajak4
            else:
                self.pajak = self.pajak1
            
            #serca
            if self.time > 7000 and len(self.llives_x) > 0 and len(self.lsprite_x) % 7 ==0:
                self.move_spr(self.llives_x, 0, 18)
                if self.is_live_lives == 1:
                    self.screen.blit(self.serce, (self.llives_x[0], self.llives_y[0]))
                if self.llives_x[0] < -128:
                   self.llives_x.pop(0)
                   self.llives_y.pop(0)
                   self.is_live_lives = 1
            
            #punkty
            if self.time > 7000 and len(self.lscore_x) > 0:
                self.move_spr(self.lscore_x, 0, 9)
                if self.is_live_score == 1:
                    self.screen.blit(self.punkt, (self.lscore_x[0], self.lscore_y[0]))
                if self.lscore_x[0] < -32:
                    self.lscore_x.pop(0)
                    self.lscore_y.pop(0)
                    self.is_live_score = 1
            
            #gracz
            self.points_y.append(self.player_y)
            if len(self.points_x) < 15:
                self.player_x += 20
            self.points_x.append(self.player_x)
            for i in range(len(self.points_x) - 1):
                self.screen.blit(self.segment, (self.points_x[i], self.points_y[i]))
            self.screen.blit(self.glowa, (self.points_x[-1], self.points_y[-1]))
            if len(self.points_x) > 15:
                for i in range(len(self.points_x)):
                    self.points_x[i] -= 20
                if self.points_x.count(-20) > 0:
                    self.points_x.pop(0)
                    self.points_y.pop(0)
            
            #kolizja - punkty
            if len(self.lscore_x) > 0 and self.is_live_score == 1:
                if self.collision_circle_square(0):
                    pygame.mixer.music.load("sounds/score.mp3")
                    if self.is_music == "ON":
                        pygame.mixer.music.play(1)
                    self.count += 1
                    self.is_live_score = 0
            
            #tekst
            self.text_center(u"Wynik: "+str(self.count), 40, bialy, 70,580)
            self.text_center(u"Serca: ", 40, bialy, 770, 580)
            for i in range(self.lives):
                self.screen.blit(self.serce, (810 + i * 35, 564))
            
            #kolizja-serce
            if len(self.llives_x) > 0 and self.is_live_lives == 1:
                if self.collision_square(self.llives_x, self.llives_y,0, 32, 32, 32, 32):
                    if self.lives < 5:
                        self.lives += 1
                    self.is_live_lives = 0
            
            #kolizja - sprity
            if len(self.lsprite_x) > 0 and self.is_live_sprite == 1:
                if self.collision_square(self.lsprite_x, self.lsprite_y, 0, 110, 42, 128, 32) and self.lives == 0:
                    pygame.time.delay(300)
                    self.gamestate = 7
                    self.screen.fill((czarny))
                    self.screen.blit(self.ziemia,(0,0))
                    if self.is_music == "ON":
                        pygame.mixer.music.load("sounds/game_over.mp3")
                    if self.is_music == "ON":
                        pygame.mixer.music.play(1)
                    if self.lvl == 0:
                        self.new_score(self.count, "scores/easy.txt")
                    elif self.lvl == 1:
                        self.new_score(self.count, "scores/medium.txt")
                    elif self.lvl == 2:
                        self.new_score(self.count, "scores/hard.txt")
                    else:
                        self.new_score(self.count, "scores/expert.txt")
                    while self.gamestate == 7:
                        for event in pygame.event.get():
                            if event.type==QUIT:
                                self.game_exit()
                            if (event.type==KEYDOWN and event.key==K_ESCAPE) or (event.type==KEYDOWN and event.key==K_RETURN):
                                self.gamestate = 4
                                self.menu()
                        self.text_center(u"Game Over", 60, (0,0,0), self.screen_width/2+3,self.screen_height/2-60+3)
                        self.text_center(u"Twoje monety: "+str(self.count), 60, (0,0,0), self.screen_width/2+3,self.screen_height/2+3)
                        self.text(u'Powrót - Enter lub Escape', 40, (0,0,0), 20+3, 560+3)
                        self.text_center(u"Game Over", 60, (255,50,150), self.screen_width/2,self.screen_height/2-60)
                        self.text_center(u"Twoje monety: "+str(self.count), 60, (255,50,150), self.screen_width/2,self.screen_height/2)
                        self.text(u'Powrót - Enter lub Escape', 40, (80,80,255), 20, 560)
                        pygame.display.update()
                        pygame.display.flip()
                if self.collision_square(self.lsprite_x, self.lsprite_y, 0, 110, 42, 128, 32) and self.lives > 0:
                    pygame.mixer.music.load("sounds/heart_lost.mp3")
                    if self.is_music == "ON":
                        pygame.mixer.music.play(1,0.5)
                    self.lives -= 1
                    self.is_live_sprite = 0
            
            #koniec gry - ułożenie dżdżownicy
            if len(self.lsprite_x)<= 0 and self.timer == 1:
                self.time2 = pygame.time.get_ticks()
                self.timer = 0
            
            #koniec gry
            if len(self.lsprite_x)<= 0 and self.time - self.time2 > 3000:
                while self.points_x[-1] < 1000:
                    self.gamestate = 8
                    self.points_y.append(self.player_y)
                    self.player_x += 20
                    self.points_x.append(self.player_x)
                    for i in range(len(self.points_x)-1):
                        self.screen.blit(self.segment, (self.points_x[i], self.points_y[i]))
                    self.screen.blit(self.glowa, (self.points_x[-1], self.points_y[-1]))
                    pygame.display.update()
                    pygame.display.flip()
                    pygame.time.delay(100)
                    if self.lvl == 0:
                        self.new_score(self.count, "scores/easy.txt")
                    elif self.lvl == 1:
                        self.new_score(self.count, "scores/medium.txt")
                    elif self.lvl == 2:
                        self.new_score(self.count, "scores/hard.txt")
                    else:
                        self.new_score(self.count, "scores/expert.txt")
                while self.gamestate == 8:
                    for event in pygame.event.get():
                        if event.type==QUIT:
                            self.game_exit()
                        if (event.type==KEYDOWN and event.key==K_ESCAPE) or (event.type==KEYDOWN and event.key==K_RETURN):
                            self.gamestate = 4
                            self.menu()
                    self.screen.fill((czarny))
                    self.screen.blit(self.ziemia,(0,0))
                    self.text_center(u"Gratulacje!", 60, (0,0,0), self.screen_width/2+3,self.screen_height/2 - 100+3)
                    self.text_center(u"Twoje monety: "+str(self.count), 60, (0,0,0), self.screen_width/2+3,self.screen_height/2+3)
                    self.text(u'Powrót - Enter lub Escape', 40, (0,0,0), 20+3, 560+3)
                    self.text_center(u"Gratulacje!", 60, (255,50,150), self.screen_width/2,self.screen_height/2 - 100)
                    self.text_center(u"Twoje monety: "+str(self.count), 60, (255,50,150), self.screen_width/2,self.screen_height/2)
                    self.text(u'Powrót - Enter lub Escape', 40, (80,80,255), 20, 560)
                    pygame.display.update()
                    pygame.display.flip()
            
            pygame.display.flip()
            pygame.display.update()
        self.game_exit()

if __name__ == '__main__':
    Game()

