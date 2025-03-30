# -*- coding: utf-8 -*-
"""
Created on Wed May 12 22:08:31 2021

@author: Roel
"""

import pygame
import mult_ui as mu
import col

bf = mu.bf

def main():
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    scrwid,scrhei = mu.scrwid,mu.scrhei
    
    screen.fill(col.blue_dark)
    mu.draw_message('Please wait a moment',0.2*scrwid,0.1*scrhei,col.black,screen)
    pygame.display.flip()
    
    return
                        
# main()