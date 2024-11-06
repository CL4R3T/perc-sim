import random

import matplotlib.pyplot as plt
import numpy
from PIL import Image


class Perc_graph():

    default_line_color = (1,0,0)

    def __init__(self,x,y,d=2):
        self.x = x
        self.y = y
        self.d = d
        self.p = numpy.empty((x,y,d))
        self.create()
        self.plt_clean()

    def create(self):
        for i in range(self.x):
            for j in range(self.y):
                for k in range(self.d):
                    self.p[i][j][k] =  (random.random())

    def judge_open_edges(self,p):
        e = numpy.empty((self.x,self.y,self.d))
        for i in range(self.x):
            for j in range(self.y):
                for k in range(self.d):
                    e[i][j][k] =  self.p[i][j][k]<=p
        return e


    def draw_dot_background(self, dot_size=4,dot_color=(0,0,0)):
        for i in range(self.x):
            for j in range(self.y):
                plt.scatter(i,j,s=dot_size,color = dot_color)
    
    def draw_all_lines(self,p,line_color=default_line_color):
        e = self.judge_open_edges(p)
        for i in range(self.x):
            for j in range(self.y):
                if e[i][j][0] and i<self.x-1:
                    plt.plot([i,i+1],[j,j],color=line_color)
                if e[i][j][1] and j<self.y-1:
                    plt.plot([i,i],[j,j+1],color=line_color)



    def draw_one_cluster_line(self,x,y,p,line_color=default_line_color):
        e = self.judge_open_edges(p)
        queue = [[x,y]]
        drawn = numpy.zeros((self.x,self.y))
        drawn.fill(False)
        while len(queue)>0:
            i,j = queue[0][0],queue[0][1]
            if i<self.x-1 and e[i][j][0] and not [i+1,j] in queue and not drawn[i+1][j]:
                plt.plot([i,i+1],[j,j],color=line_color)
                queue.append([i+1,j])
            if j<self.y-1 and e[i][j][1] and not [i,j+1] in queue and not drawn[i][j+1]:
                plt.plot([i,i],[j,j+1],color=line_color)
                queue.append([i,j+1])
            if i>0 and e[i-1][j][0] and not [i-1,j] in queue and not drawn[i-1][j]:
                plt.plot([i,i-1],[j,j],color=line_color)
                queue.append([i-1,j])
            if j>0 and e[i][j-1][1] and not [i,j-1] in queue and not drawn[i][j-1]:
                plt.plot([i,i],[j,j-1],color=line_color)
                queue.append([i,j-1])
            drawn[i][j] = True
            queue.pop(0)

    def draw_all_cluster_pixel(self,p,color_pattern_path) -> Image:

        e = self.judge_open_edges(p)
        color_pattern = Image.open(color_pattern_path)
        im = Image.new("RGB",(self.x,self.y))
        drawn = numpy.zeros((self.x,self.y))
        drawn.fill(False)  
        for x in range(self.x):
            for y in range(self.y):
                if(drawn[x][y]):continue
                color = color_pattern.getpixel((x,y))
                im.putpixel((x,y),color)
                queue = [[x,y]]
                
                while len(queue)>0:
                    i,j = queue[0][0],queue[0][1]
                    if i<self.x-1 and e[i][j][0] and not [i+1,j] in queue and not drawn[i+1][j]:
                        im.putpixel((i+1,j),color)
                        queue.append([i+1,j])

                    if j<self.y-1 and e[i][j][1] and not [i,j+1] in queue and not drawn[i][j+1]:
                        im.putpixel((i,j+1),color)
                        queue.append([i,j+1])

                    if i>0 and e[i-1][j][0] and not [i-1,j] in queue and not drawn[i-1][j]:
                        im.putpixel((i-1,j),color)
                        queue.append([i-1,j])

                    if j>0 and e[i][j-1][1] and not [i,j-1] in queue and not drawn[i][j-1]:
                        im.putpixel((i,j-1),color)
                        queue.append([i,j-1])

                    drawn[i][j] = True
                    queue.pop(0)
        return im
            




    def plt_show(self):
        plt.show()
    
    def plt_clean(self):
        plt.close()
        plt.axis('off')
        ax = plt.gca()
        ax.set_aspect(1) 




if __name__ == "__main__":
    graph = Perc_graph(512,512)
    n=100
    start = 0.45
    end = 0.55
    for i in range(0,n+1):
        p = start+i/n*(end-start)
        image = graph.draw_all_cluster_pixel(p,color_pattern_path = "color-pattern.png")
        image.save(f"fig/pixel512slow/512-512-{(str(p)[:5]+'00')[:5]}.png")
    