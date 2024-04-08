import pygame
import random
import numpy as np
import math
import os

#init pygame
pygame.init()

#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
orange = (255,165,0)

game_display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Physics Simulator")

width, height = game_display.get_size()

clock = pygame.time.Clock()

def d(x,y):
    sum = 0
    for i in range(len(x)):
        sum += (x[i] - y[i])**2
    return sum**0.5

def path(s, t, graph, marked_order):
    path = []
    current = t
    for i in marked_order[::-1]:
        for j in i:
            if j in graph[current]:
                path.append(j)
                current = j
    return path
        


def BFS(s, t, graph):
    marked = {s}
    marked_order = [{s}]
    while True:
        marked_order.append(set())
        for i in marked_order[-2]:
            for j in graph[i]:
                if j not in marked:
                    marked.add(j)
                    marked_order[-1].add(j)
                    if j == t:
                        return marked, marked_order
        if marked_order[-1] == set():
            break
    return None

def run():
    graph = []
    node_pos = []
    point = [-1.0,-1.0]
    start_node = 0
    lb_pressed = False
    run = True
    node_nearby = False
    s = -1
    t = -1

    while run:
        game_display.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i,pos in enumerate(node_pos):
                    if d(pos,pygame.mouse.get_pos()) <= 10:
                        node_nearby = True

                if not node_nearby:
                    node_pos.append(pygame.mouse.get_pos())
                    graph.append(set())
                
                node_nearby = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                lb_pressed = True

                for i,pos in enumerate(node_pos):
                    if d(pos,pygame.mouse.get_pos()) <= 10:
                        start_node = i
                        point = pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for i,pos in enumerate(node_pos):
                    if d(pos,pygame.mouse.get_pos()) <= 10 and not(start_node is None):
                        graph[start_node].add(i)
                        graph[i].add(start_node)
                        graph[start_node].add(start_node)
                        point = pos
                
                start_node = None
                point = [-1.0,-1.0]
                lb_pressed = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for i,pos in enumerate(node_pos):
                    if d(pos,pygame.mouse.get_pos()) <= 10:
                        if s >= 0 and t < 0:
                            t = i
                        if s < 0:
                            s = i



        for i in range(len(node_pos)):
            if BFS(s,t,graph) is not None and i in path(s,t,graph,BFS(s,t,graph)[1]):
                pygame.draw.circle(center = (node_pos[i][0], node_pos[i][1]), radius = 10, color = red, surface = game_display)
            else:
                pygame.draw.circle(center = (node_pos[i][0], node_pos[i][1]), radius = 10, color = white, surface = game_display)

        for node, connections in enumerate(graph):
            for j in connections:
                pygame.draw.line(start_pos = node_pos[node], end_pos = node_pos[j], color = white, surface = game_display, width = 5)
        
        if len(graph) > 0:
            if BFS(s,t,graph) is not None:
                p = path(s,t,graph,BFS(s,t,graph)[1])
                for i in range(len(p)-1):
                    pygame.draw.line(start_pos = node_pos[p[i]], end_pos = node_pos[p[i+1]], color = red, surface = game_display, width = 5)

        if lb_pressed and point != [-1.0,-1.0]:
            pygame.draw.line(start_pos = point, end_pos = pygame.mouse.get_pos(), color = white, surface = game_display, width = 5)

        pygame.display.update()
        clock.tick()
    
    print(graph)
    print(BFS(s,t,graph))
    print(path(s,t,graph,BFS(s,t,graph)[1]))
    pygame.quit()

run()