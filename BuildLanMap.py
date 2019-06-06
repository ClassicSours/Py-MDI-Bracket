#!/usr/bin/env python
from PIL import Image,ImageDraw,ImageFont
import math
import os
import itertools
import pandas as pd
import sys

width,height = 56,56
# blank_image = Image.new('RGBA', (width,height), (255,255,255,255))

def build_icon_dict(dir):
    files = os.listdir(dir)
    name = [i.rsplit('.',1)[0] for i in files]
    icon = [Image.open(dir + file) for file in files]
    return(dict(zip(name,icon)))

affixes = build_icon_dict('images/affix/')
dungeons = build_icon_dict('images/dungeon/icon/')

# Create text white w/ black outline
def add_text(image,x,y,text,fill, raline = False):
    if len(str(text)) == 1:
        x += .25
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 45)
    draw = ImageDraw.Draw(image)
    w = draw.textsize(str(text),font = font)[0]
    xoffset = 0
    if(raline):
        xoffset = width * .75 - w
    ImageDraw.Draw(image).text((x*width+1 + xoffset,y*height+height*.15),  str(text),font=font,fill="black")
    ImageDraw.Draw(image).text((x*width-1 + xoffset,y*height+height*.15),  str(text),font=font,fill="black")
    ImageDraw.Draw(image).text((x*width + xoffset,  y*height+height*.15+1),str(text),font=font,fill="black")
    ImageDraw.Draw(image).text((x*width + xoffset,  y*height+height*.15-1),str(text),font=font,fill="black")
    ImageDraw.Draw(image).text((x*width + xoffset,  y*height+height*.15),  str(text),font=font,fill=fill)
    return(image)

# create level for a dungeon (text w/ white outline)
def create_level(image,level):
    add_text(image,0,height,level,(0,255,0,255))
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 45)
    ImageDraw.Draw(image).text((0+1,height*.15),str(level),font=font,fill="black")
    ImageDraw.Draw(image).text((0-1,height*.15),str(level),font=font,fill="black")
    ImageDraw.Draw(image).text((0,height*.15+1),str(level),font=font,fill="black")
    ImageDraw.Draw(image).text((0,height*.15-1),str(level),font=font,fill="black")
    ImageDraw.Draw(image).text((0,height*.15),  str(level),font=font,fill="white")
    return(image)

# Adds a colored rectangle of color RGBA
def add_colorRectange(image,x,y,w_mod,h_mod,RGBA):
    colorRectangel = Image.new('RGBA', (width*w_mod, height*h_mod), RGBA)
    image.paste(colorRectangel,(x*width,y*height))
    return(image)

# Build the graphic for a dungeon
def build_map(level,map,affix):
    l_map = Image.new('RGBA', (width*5,height), (255,255,255,255))
    l_map.paste(create_level(dungeons[map],level), (width*0,height*0))
    for i in range(len(affix)):
        l_map.paste(affixes[affix[i]], (width*(i+1), height*0))
    return(l_map)

def build_match(maps):
    n = len(maps)
    l_match = Image.new('RGBA', (width*5,height*n), (255,255,255,255))
    for i in range(n):
        l_match.paste(maps[i],(width*0, height*i))
    return(l_match)


def add_WinLine(image,a,b,c,fill):
    a += .25
    b += .5
    c += .5
    draw = ImageDraw.Draw(image)
    draw.line((width*(a),height*(b),width*(a + .75),height*(b)),fill = fill, width = 2)
    draw.line((width*(a),height*(c),width*(a + .75),height*(c)),fill = fill, width = 2)
    draw.line((width*(a + .75),height*(b),width*(a + .75),height*(c)),fill = fill, width = 2)
    draw.line((width*(a + .75),height*((b + c)/2),width*(a + 1.5),height*((b+c)/2)),fill = fill, width = 2)
    del draw

def add_SingleWinLine(image,a,b,c,fill):
    a += .25
    b += .5
    c += .5
    draw = ImageDraw.Draw(image)
    draw.line((width*(a),height*(b),width*(a + .75),height*(b)),fill = fill, width = 2)
    draw.line((width*(a+.75),height*(b),width*(a + .75),height*(c)),fill = fill, width = 2)
    draw.line((width*(a+.75),height*(c),width*(a + 1.5),height*(c)),fill = fill, width = 2)
    del draw

if len(sys.argv) < 4:
    sys.tracebacklimit = 0
    raise ValueError("Program needs 4 Arguments to Run, <Mappool.csv> <Sets.csv> <Teams.txt> <keylevel> recieved: {}".format(len(sys.argv)))
    
mappool = sys.argv[1]
sets = sys.argv[2]
top8 = sys.argv[3]
keylevel = sys.argv[4]

maplist = pd.read_csv(mappool,delimiter=',', skipinitialspace=True)
maporder = pd.read_csv(sets,delimiter=',',index_col=0, skipinitialspace=True)
teams = pd.read_csv(top8,delimiter='\n')
maplist.columns = map(str.upper, maplist.columns)
for i in maplist:
    maplist[i] = maplist[i].apply(lambda x: x.upper())

maporder.columns = map(str.upper, maporder.columns)
for i in maporder:
    maporder[i] = maporder[i].apply(lambda x: None if pd.isnull(x) else x.upper())

# print(maplist)
# print(maporder)
match_graphics = []
for index,row in maporder.iterrows():
    x = []
    for col in row:
        if not pd.isnull(col):
            x.append(build_map(keylevel,col,maplist[col]))
    y = build_match(x)
    match_graphics.append(y)


BracketX1 = 10
BracketX2 = BracketX1 + 8
BracketX3 = BracketX2 + 8
BracketX4 = BracketX3 + 8
BracketY1 = 2
BracketY2 = BracketY1 + 18
YOffset = 4
DoubleElim = Image.new('RGBA', (width*42,height*28), (43,45,54,255))
##############################################################
# Upper Round 1
DoubleElim = add_text(DoubleElim,BracketX1,0,"Upper Round 1","white")

day = [1,1,1,1,1,1,2,2,2,2,2,3,3,3]
daycolor = [(127,196,254,255),(220,207,58,255),(212,70,51,255)]
for i in range(0,4):
    DoubleElim.paste(match_graphics[i],(width * (BracketX1 + 1),height * ((i * YOffset) + 1)))
    DoubleElim = add_text(DoubleElim, BracketX1, BracketY1 + (i * YOffset),i+1,daycolor[day[i]-1])

# print(teams)
teamcolor = [(230,126,34,255), (255,255,255,255), (255,144,22,255), (230,34,34,255), (46,204,113,255), (173,20,87,255), (155,89,182,255), (194,194,194,255)]
          # [1,8,4,5,2,7,3,6]
          # [1,2,3,4,5,6,7,8]
teamorder = [1,5,7,3,4,8,6,2]
for index, team in teams.iterrows():
    # print(team[0],index,teamorder[index])
    DoubleElim = add_text(DoubleElim,
                          BracketX1,
                          2 * teamorder[index] - 1,
                          team[0],
                          teamcolor[index],
                          True)

##############################################################

# Upper Round 2
DoubleElim = add_text(DoubleElim,BracketX2,0,"Upper Round 2","white")

for i in range(0,2):
    DoubleElim.paste(match_graphics[4+i],(width * (BracketX2+1), height * (3 + (8 * i))))
    DoubleElim = add_text(DoubleElim,BracketX2,4+(8*i),i+5,daycolor[day[i+4]-1])

##############################################################
# Lower Round 1
DoubleElim = add_text(DoubleElim,BracketX1,16,"Lower Round 1","white")
DoubleElim = add_text(DoubleElim,BracketX1+1,BracketY2-1,"L(1) v L(2)","white")
DoubleElim = add_text(DoubleElim,BracketX1+1,BracketY2+(2*YOffset)-1,"L(3) v L(4)","white")

for i in range(0,2):
    DoubleElim.paste(match_graphics[i+6],(width * (BracketX1 + 1),height * ((BracketY2) + (i * YOffset))))
    DoubleElim = add_text(DoubleElim,BracketX1,(BracketY2 + 1) + (i * YOffset),i+7,daycolor[day[i+6]-1])

##############################################################
# Lower Round 2
DoubleElim = add_text(DoubleElim,BracketX2,16,"Lower Round 2","white")
DoubleElim = add_text(DoubleElim,BracketX2+1,BracketY2-2,"L(6)","white")
DoubleElim = add_text(DoubleElim,BracketX2+1,BracketY2+(2*YOffset)-2,"L(5)","white")

for i in range(0,2):
    DoubleElim.paste(match_graphics[i+8],(width * (BracketX2 + 1),height * ((BracketY2-1) + (i*YOffset))))
    DoubleElim = add_text(DoubleElim,BracketX2,(BracketY2) + (i*YOffset),i+9,daycolor[day[i+8]-1])


##############################################################
# Upper Finals
DoubleElim = add_text(DoubleElim,BracketX3,0,"Upper Finals","white")

DoubleElim.paste(match_graphics[10],(width * (BracketX3 + 1),height * 7))

DoubleElim = add_text(DoubleElim,BracketX3,8,11,daycolor[day[10]-1])

##############################################################
# Lower Semifinals
DoubleElim = add_text(DoubleElim,BracketX3,16,"Lower Semifinals","white")

DoubleElim.paste(match_graphics[11],(width * (BracketX3 + 1),height * (BracketY2 + 1)))

DoubleElim = add_text(DoubleElim,BracketX3,BracketY2+2,12,daycolor[day[11]-1])

##############################################################
# Lower Finals
DoubleElim = add_text(DoubleElim,BracketX4,16,"Lower Finals","white")
DoubleElim = add_text(DoubleElim,BracketX4+1,BracketY2-1,"L(11)","white")

DoubleElim.paste(match_graphics[12],(width * (BracketX4 + 1),height * (BracketY2)))

DoubleElim = add_text(DoubleElim,BracketX4,BracketY2+1,13,daycolor[day[12]-1])

##############################################################
# Grand Finals
DoubleElim = add_text(DoubleElim,BracketX4,0,"Grand Finals","white")
DoubleElim = add_text(DoubleElim,BracketX4+1,7,"W(13)","white")

DoubleElim.paste(match_graphics[13],(width * (BracketX4 + 1),height * 7))

DoubleElim = add_text(DoubleElim,BracketX4,9,14,daycolor[day[13]-1])

##############################################################
# Index
for i in range(0,3):
    DoubleElim = add_colorRectange(DoubleElim,BracketX4,BracketY2+YOffset+i,1,1,daycolor[i])
    DoubleElim = add_text(DoubleElim,BracketX4+1,BracketY2+YOffset+i," = Day " + str(i + 1),daycolor[i])

##############################################################
# Bracket Lines

# UR(1) W(1) v W(2)
add_WinLine(DoubleElim,BracketX1 + 6,
                       BracketY1,
                       BracketY1+YOffset,(255,255,255))
# UR(1) W(3) v W(4)
add_WinLine(DoubleElim,BracketX1 + 6,
                       BracketY1+(YOffset*2),
                       BracketY1+(YOffset*3),(255,255,255))

# UR(2) W(5) v W(6)
add_WinLine(DoubleElim,BracketX2 + 6,
                       BracketY1 + (YOffset/2), #4 12
                       BracketY1 + (YOffset*3)-(YOffset/2) ,(255,255,255))
# LR(2) W(9) v W(10)
add_WinLine(DoubleElim,BracketX2 + 6,
                       BracketY2,
                       BracketY2 + YOffset,(255,255,255))

# LR(1) W(7)
add_SingleWinLine(DoubleElim,BracketX1 + 6,
                             BracketY2+1,
                             BracketY2,(255,255,255))
# LR(1) W(9)
add_SingleWinLine(DoubleElim,BracketX1 + 6,
                             BracketY2+YOffset+1,
                             BracketY2+YOffset,(255,255,255))
# UR(3) W(11)
add_SingleWinLine(DoubleElim,BracketX3 + 6,
                             BracketY1+YOffset+2,
                             BracketY1+YOffset+3,(255,255,255))
# LR(3) W(12)
add_SingleWinLine(DoubleElim,BracketX3 + 6,
                             BracketY2+2,
                             BracketY2+1,(255,255,255))

# DoubleElim.show()

filename_split = (mappool.split('.')[0].split('_'))
if len(filename_split[0].split('/')) == 2:
    filename_split[0] = filename_split[0].split('/')[1]
del(filename_split[2])
# print(filename_split)
# print("_".join(filename_split))
output_Filename = "_".join(filename_split[::-1])
DoubleElim.save("".join(output_Filename) + '_Bracket.png')

