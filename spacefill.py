#!/usr/bin/env python3
# Borrowed from Tyler Bletsch
import sys

# algorithm and original javascript implementation by Lutz Tautenhahn - http://lutanho.net/pic2html/draw_sfc.html
# converted to python by tyler bletsch

# debug print - comment print in/out as desired
def dprint(*a):
    pass
    #print(*a)

def render(x, y, dir):
    global coords
    coords.append((int(x),int(y)))
    #print(((x,y)),dir)
    return

# #left, top, width, height
def spacefill(ww,hh,ll=1,tt=1):
    global coords
    coords = []
    if hh>ww: #go top->down
        if (hh%2==1) and (ww%2==0):
            go(ll, tt, ww, 0, 0, hh, "m"); #go diagonal
        else:
            go(ll, tt, ww, 0, 0, hh, "r"); #go top->down
    else: #go left->right
        if (ww%2==1) and (hh%2==0):
            go(ll, tt, ww, 0, 0, hh, "m"); #go diagonal
        else:
            go(ll, tt, ww, 0, 0, hh, "l"); #go left->right
    return coords

def go(x0, y0, dxl, dyl, dxr, dyr, dir):
    #x0, y0: start corner looking to the center of the rectangle
    #dxl, dyl: vector from the start corner to the left corner of the rectangle
    #dxr, dyr: vector from the start corner to the right corner of the rectangle
    #dir: direction to go - "l"=left, "m"=middle, "r"=right
    dprint("go: %d,%d  %d,%d  %d,%d  %s" % (x0,y0,dxl,dyl,dxr,dyr,dir))
    #render if 2x3 or smaller
    if abs((dxl+dyl)*(dxr+dyr))<=6:
        # ddx, ddy, ii
        if abs(dxl+dyl)==1:
            ddx=dxr/abs(dxr+dyr)
            ddy=dyr/abs(dxr+dyr)
            for ii in range(round(abs(dxr+dyr))):
                render(x0+ii*ddx+(dxl+ddx-1)/2, y0+ii*ddy+(dyl+ddy-1)/2, dir)
            return    
        
        if abs(dxr+dyr)==1:
            ddx=dxl/abs(dxl+dyl)
            ddy=dyl/abs(dxl+dyl)
            for ii in range(round(abs(dxl+dyl))):
                render(x0+ii*ddx+(dxr+ddx-1)/2, y0+ii*ddy+(dyr+ddy-1)/2, dir)        
            return
        if dir=="l":
            ddx=dxr/abs(dxr+dyr)
            ddy=dyr/abs(dxr+dyr)
            for ii in range(round(abs(dxr+dyr))):
                render(x0+ii*ddx+(dxl/2+ddx-1)/2, y0+ii*ddy+(dyl/2+ddy-1)/2, dir)
            for ii in range(round(abs(dxr+dyr))-1,-1,-1):
                render(x0+ii*ddx+(dxl+dxl/2+ddx-1)/2, y0+ii*ddy+(dyl+dyl/2+ddy-1)/2, dir)                
            return    
        if dir=="r":
            ddx=dxl/abs(dxl+dyl)
            ddy=dyl/abs(dxl+dyl)
            for ii in range(round(abs(dxl+dyl))):
                render(x0+ii*ddx+(dxr/2+ddx-1)/2, y0+ii*ddy+(dyr/2+ddy-1)/2, dir)
            for ii in range(round(abs(dxl+dyl))-1,-1,-1):
                render(x0+ii*ddx+(dxr+dxr/2+ddx-1)/2, y0+ii*ddy+(dyr+dyr/2+ddy-1)/2, dir)                
            return    
        if dir=="m":
            if abs(dxr+dyr)==3:
                ddx=dxr/abs(dxr+dyr)
                ddy=dyr/abs(dxr+dyr)
                render(x0+(dxl/2+ddx-1)/2, y0+(dyl/2+ddy-1)/2, dir)
                render(x0+(dxl+dxl/2+ddx-1)/2, y0+(dyl+dyl/2+ddy-1)/2, dir)
                render(x0+ddx+(dxl+dxl/2+ddx-1)/2, y0+ddy+(dyl+dyl/2+ddy-1)/2, dir)
                render(x0+ddx+(dxl/2+ddx-1)/2, y0+ddy+(dyl/2+ddy-1)/2, dir)
                render(x0+2*ddx+(dxl/2+ddx-1)/2, y0+2*ddy+(dyl/2+ddy-1)/2, dir)
                render(x0+2*ddx+(dxl+dxl/2+ddx-1)/2, y0+2*ddy+(dyl+dyl/2+ddy-1)/2, dir)
                return
            if abs(dxl+dyl)==3:
                ddx=dxl/abs(dxl+dyl)
                ddy=dyl/abs(dxl+dyl)
                render(x0+(dxr/2+ddx-1)/2, y0+(dyr/2+ddy-1)/2, dir)
                render(x0+(dxr+dxr/2+ddx-1)/2, y0+(dyr+dyr/2+ddy-1)/2, dir)
                render(x0+ddx+(dxr+dxr/2+ddx-1)/2, y0+ddy+(dyr+dyr/2+ddy-1)/2, dir)
                render(x0+ddx+(dxr/2+ddx-1)/2, y0+ddy+(dyr/2+ddy-1)/2, dir)
                render(x0+2*ddx+(dxr/2+ddx-1)/2, y0+2*ddy+(dyr/2+ddy-1)/2, dir)
                render(x0+2*ddx+(dxr+dxr/2+ddx-1)/2, y0+2*ddy+(dyr+dyr/2+ddy-1)/2, dir)
                return
        raise Exception("renderError")
        return
    #divide into 2 parts if necessary
    if 2*(abs(dxl)+abs(dyl)) > 3*(abs(dxr)+abs(dyr)): 
        dprint("2p")
        dxl2=round(dxl/2)
        dyl2=round(dyl/2)
        if (abs(dxr)+abs(dyr))%2==0: #right side is even
            if (abs(dxl)+abs(dyl))%2==0: #make 2 parts from even side
                if (dir=="l"):
                    if ((abs(dxl)+abs(dyl))%4==0): #make 2 parts even-even from even side
                        go(x0, y0, dxl2, dyl2, dxr, dyr, "l")
                        go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr, dyr, "l")
                    else: #make 2 parts odd-odd from even side
                        go(x0, y0, dxl2, dyl2, dxr, dyr, "m")
                        go(x0+dxl2+dxr, y0+dyl2+dyr, -dxr, -dyr, dxl-dxl2, dyl-dyl2, "m")
                    return
            else: #make 2 parts from odd side
                if dir=="m":
                    if (abs(dxl2)+abs(dyl2))%2==0:
                        go(x0, y0, dxl2, dyl2, dxr, dyr, "l")
                        go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr, dyr, "m")
                    else:
                        go(x0, y0, dxl2, dyl2, dxr, dyr, "m")
                        go(x0+dxl2+dxr, y0+dyl2+dyr, -dxr, -dyr, dxl-dxl2, dyl-dyl2, "r")
                    return
        else: #right side is odd
            if (dir=="l"):
                go(x0, y0, dxl2, dyl2, dxr, dyr, "l")
                go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr, dyr, "l")
                return
            if dir=="m":
                go(x0, y0, dxl2, dyl2, dxr, dyr, "l")
                go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr, dyr, "m")
                return
    if 2*(abs(dxr)+abs(dyr)) > 3*(abs(dxl)+abs(dyl)): #right side much longer than left side
        dprint("rsl")
        dxr2=round(dxr/2)
        dyr2=round(dyr/2)
        if (abs(dxl)+abs(dyl))%2==0: #left side is even
            if (abs(dxr)+abs(dyr))%2==0: #make 2 parts from even side
                if dir=="r":
                    if (abs(dxr)+abs(dyr))%4==0: #make 2 parts even-even from even side
                        go(x0, y0, dxl, dyl, dxr2, dyr2, "r")
                        go(x0+dxr2, y0+dyr2, dxl, dyl, dxr-dxr2, dyr-dyr2, "r")
                    else: #make 2 parts odd-odd from even side
                        go(x0, y0, dxl, dyl, dxr2, dyr2, "m")
                        go(x0+dxr2+dxl, y0+dyr2+dyl, dxr-dxr2, dyr-dyr2, -dxl, -dyl, "m")
                    return
            else: #make 2 parts from odd side
                if dir=="m":
                    if (abs(dxr2)+abs(dyr2))%2==0:
                        go(x0, y0, dxl, dyl, dxr2, dyr2, "r")
                        go(x0+dxr2, y0+dyr2, dxl, dyl, dxr-dxr2, dyr-dyr2, "m")
                    else:
                        go(x0, y0, dxl, dyl, dxr2, dyr2, "m")
                        go(x0+dxr2+dxl, y0+dyr2+dyl, dxr-dxr2, dyr-dyr2, -dxl, -dyl, "l")
                    return
        else: #left side is odd
            if dir=="r":
                go(x0, y0, dxl, dyl, dxr2, dyr2, "r")
                go(x0+dxr2, y0+dyr2, dxl, dyl, dxr-dxr2, dyr-dyr2, "r")
                return
            if dir=="m":
                go(x0, y0, dxl, dyl, dxr2, dyr2, "r")
                go(x0+dxr2, y0+dyr2, dxl, dyl, dxr-dxr2, dyr-dyr2, "m")
                return
    #divide into 2x2 parts
    if dir=="l" or dir=="r":
        dprint("div 2x2")
        dxl2=round(dxl/2)
        dyl2=round(dyl/2)
        dxr2=round(dxr/2)
        dyr2=round(dyr/2)    
        if (abs(dxl+dyl)%2==0) and (abs(dxr+dyr)%2==0): #even-even
            if abs(dxl2+dyl2+dxr2+dyr2)%2==0: #ee-ee or oo-oo
                if dir=="l":
                    go(x0, y0, dxl2, dyl2, dxr2, dyr2, "r")
                    go(x0+dxr2, y0+dyr2, dxl2, dyl2, dxr-dxr2, dyr-dyr2, "l")
                    go(x0+dxr2+dxl2, y0+dyr2+dyl2, dxl-dxl2, dyl-dyl2, dxr-dxr2, dyr-dyr2, "l")
                    go(x0+dxr2+dxl, y0+dyr2+dyl, dxl2-dxl, dyl2-dyl, -dxr2, -dyr2, "r")
                else:
                    go(x0, y0, dxl2, dyl2, dxr2, dyr2, "l")
                    go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr2, dyr2, "r")
                    go(x0+dxr2+dxl2, y0+dyr2+dyl2, dxl-dxl2, dyl-dyl2, dxr-dxr2, dyr-dyr2, "r")
                    go(x0+dxr+dxl2, y0+dyr+dyl2, -dxl2, -dyl2, dxr2-dxr, dyr2-dyr, "l")
            else: #ee-oo or oo-ee
                if (dxr2+dyr2)%2==0: #ee-oo
                    if dir=="l":
                        go(x0, y0, dxl2, dyl2, dxr2, dyr2, "r")
                        go(x0+dxr2, y0+dyr2, dxl2, dyl2, dxr-dxr2, dyr-dyr2, "m")
                        go(x0+dxr+dxl2, y0+dyr+dyl2, dxr2-dxr, dyr2-dyr, dxl-dxl2, dyl-dyl2, "m")
                        go(x0+dxr2+dxl, y0+dyr2+dyl, dxl2-dxl, dyl2-dyl, -dxr2, -dyr2, "r")
                    else: #ee-oo for dir="r" not possible, so transforming into e-1,e+1-oo = oo-oo 
                        if dxr2!=0:
                            dxr2+=1 
                        else:
                            dyr2+=1 
                        go(x0, y0, dxl2, dyl2, dxr2, dyr2, "l")
                        go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr2, dyr2, "m")
                        go(x0+dxl+dxr2, y0+dyl+dyr2, dxr-dxr2, dyr-dyr2, dxl2-dxl, dyl2-dyl, "m")
                        go(x0+dxl2+dxr, y0+dyl2+dyr, -dxl2, -dyl2, dxr2-dxr, dyr2-dyr, "l")
                else: #oo-ee
                    if dir=="r":
                        go(x0, y0, dxl2, dyl2, dxr2, dyr2, "l")
                        go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr2, dyr2, "m")
                        go(x0+dxl+dxr2, y0+dyl+dyr2, dxr-dxr2, dyr-dyr2, dxl2-dxl, dyl2-dyl, "m")
                        go(x0+dxl2+dxr, y0+dyl2+dyr, -dxl2, -dyl2, dxr2-dxr, dyr2-dyr, "l")
                    else: #oo-ee for dir="l" not possible, so transforming into oo-e-1,e+1 = oo-oo 
                        if dxl2!=0:
                            dxl2+=1 
                        else:
                            dyl2+=1
                        go(x0, y0, dxl2, dyl2, dxr2, dyr2, "r")
                        go(x0+dxr2, y0+dyr2, dxl2, dyl2, dxr-dxr2, dyr-dyr2, "m")
                        go(x0+dxr+dxl2, y0+dyr+dyl2, dxr2-dxr, dyr2-dyr, dxl-dxl2, dyl-dyl2, "m")
                        go(x0+dxr2+dxl, y0+dyr2+dyl, dxl2-dxl, dyl2-dyl, -dxr2, -dyr2, "r")
        else: #not even-even
            if ((abs(dxl+dyl)%2!=0) and (abs(dxr+dyr)%2!=0)): #odd-odd
                if dxl2%2!=0: dxl2=dxl-dxl2 #get it in a shape eo-eo 
                if dyl2%2!=0: dyl2=dyl-dyl2
                if dxr2%2!=0: dxr2=dxr-dxr2
                if dyr2%2!=0: dyr2=dyr-dyr2
                if dir=="l":
                    go(x0, y0, dxl2, dyl2, dxr2, dyr2, "r")
                    go(x0+dxr2, y0+dyr2, dxl2, dyl2, dxr-dxr2, dyr-dyr2, "m")
                    go(x0+dxr+dxl2, y0+dyr+dyl2, dxr2-dxr, dyr2-dyr, dxl-dxl2, dyl-dyl2, "m")
                    go(x0+dxr2+dxl, y0+dyr2+dyl, dxl2-dxl, dyl2-dyl, -dxr2, -dyr2, "r")
                else:
                    go(x0, y0, dxl2, dyl2, dxr2, dyr2, "l")
                    go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr2, dyr2, "m")
                    go(x0+dxl+dxr2, y0+dyl+dyr2, dxr-dxr2, dyr-dyr2, dxl2-dxl, dyl2-dyl, "m")
                    go(x0+dxl2+dxr, y0+dyl2+dyr, -dxl2, -dyl2, dxr2-dxr, dyr2-dyr, "l")
            else: #even-odd or odd-even
                if abs(dxl+dyl)%2==0: #odd-even
                    if dir=="l":
                        if dxr2%2!=0: dxr2=dxr-dxr2 #get it in a shape eo-xx 
                        if dyr2%2!=0: dyr2=dyr-dyr2
                        if abs(dxl+dyl)>2:
                            go(x0, y0, dxl2, dyl2, dxr2, dyr2, "r")
                            go(x0+dxr2, y0+dyr2, dxl2, dyl2, dxr-dxr2, dyr-dyr2, "l")
                            go(x0+dxr2+dxl2, y0+dyr2+dyl2, dxl-dxl2, dyl-dyl2, dxr-dxr2, dyr-dyr2, "l")
                            go(x0+dxr2+dxl, y0+dyr2+dyl, dxl2-dxl, dyl2-dyl, -dxr2, -dyr2, "r")
                        else:
                            go(x0, y0, dxl2, dyl2, dxr2, dyr2, "r")
                            go(x0+dxr2, y0+dyr2, dxl2, dyl2, dxr-dxr2, dyr-dyr2, "m")
                            go(x0+dxr+dxl2, y0+dyr+dyl2, dxr2-dxr, dyr2-dyr, dxl-dxl2, dyl-dyl2, "m")
                            go(x0+dxr2+dxl, y0+dyr2+dyl, dxl2-dxl, dyl2-dyl, -dxr2, -dyr2, "r")
                    else:
                        raise Exception("4-part-error1: "+x0+", "+y0+", "+dxl+", "+dyl+", "+dxr+", "+dyr+", "+dir)
                else: #even-odd
                    if dir=="r":
                        if dxl2%2!=0: dxl2=dxl-dxl2 #get it in a shape xx-eo 
                        if dyl2%2!=0: dyl2=dyl-dyl2
                        if abs(dxr+dyr)>2:
                            go(x0, y0, dxl2, dyl2, dxr2, dyr2, "l")
                            go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr2, dyr2, "r")
                            go(x0+dxr2+dxl2, y0+dyr2+dyl2, dxl-dxl2, dyl-dyl2, dxr-dxr2, dyr-dyr2, "r")
                            go(x0+dxr+dxl2, y0+dyr+dyl2, -dxl2, -dyl2, dxr2-dxr, dyr2-dyr, "l")
                        else:
                            go(x0, y0, dxl2, dyl2, dxr2, dyr2, "l")
                            go(x0+dxl2, y0+dyl2, dxl-dxl2, dyl-dyl2, dxr2, dyr2, "m")
                            go(x0+dxl+dxr2, y0+dyl+dyr2, dxr-dxr2, dyr-dyr2, dxl2-dxl, dyl2-dyl, "m")
                            go(x0+dxl2+dxr, y0+dyl2+dyr, -dxl2, -dyl2, dxr2-dxr, dyr2-dyr, "l")
                    else:
                        raise Exception("4-part-error2: "+x0+", "+y0+", "+dxl+", "+dyl+", "+dxr+", "+dyr+", "+dir)                
    else: #dir=="m" -> divide into 3x3 parts
        dprint("div3")
        if (abs(dxl+dyl)%2==0) and (abs(dxr+dyr)%2==0):
            raise Exception("9-part-error1: "+x0+", "+y0+", "+dxl+", "+dyl+", "+dxr+", "+dyr+", "+dir)                
        if abs(dxr+dyr)%2==0: #even-odd: oeo-ooo
            dxl2=round(dxl/3)
            dyl2=round(dyl/3)
            dxr2=round(dxr/3)
            dyr2=round(dyr/3)
            if (dxl2+dyl2)%2==0: #make it odd    
                dxl2=dxl-2*dxl2 
                dyl2=dyl-2*dyl2 
            if (dxr2+dyr2)%2==0: #make it odd (not necessary, however results are better for 12x30, 18x30 etc.:
                if abs(dxr2+dyr2)!=2:
                    if dxr<0: dxr2+=1
                    if dxr>0: dxr2-=1    #dont use else here !
                    if dyr<0: dyr2+=1
                    if dyr>0: dyr2-=1    #dont use else here !
        else: #odd-even: ooo-oeo
            dxl2=round(dxl/3)
            dyl2=round(dyl/3)
            dxr2=round(dxr/3)
            dyr2=round(dyr/3)
            if (dxr2+dyr2)%2==0: #make it odd    
                dxr2=dxr-2*dxr2 
                dyr2=dyr-2*dyr2 
            if (dxl2+dyl2)%2==0: #make it odd (not necessary, however results are better for 12x30, 18x30 etc.:
                if abs(dxl2+dyl2)!=2:
                    if dxl<0: dxl2+=1
                    if dxl>0: dxl2-=1    #dont use else here !
                    if dyl<0: dyl2+=1
                    if dyl>0: dyl2-=1    #dont use else here !
        if abs(dxl+dyl) < abs(dxr+dyr):
            dprint("bigblock A")
            go(x0, y0, dxl2, dyl2, dxr2, dyr2, "m")
            go(x0+dxl2+dxr2, y0+dyl2+dyr2, -dxr2, -dyr2, dxl-2*dxl2, dyl-2*dyl2, "m")
            go(x0+dxl-dxl2, y0+dyl-dyl2, dxl2, dyl2, dxr2, dyr2, "m")
            go(x0+dxl+dxr2, y0+dyl+dyr2, dxr-2*dxr2, dyr-2*dyr2, -dxl2, -dyl2, "m")
            go(x0+dxr-dxr2+dxl-dxl2, y0+dyr-dyr2+dyl-dyl2, 2*dxl2-dxl, 2*dyl2-dyl, 2*dxr2-dxr, 2*dyr2-dyr, "m")
            go(x0+dxl2+dxr2, y0+dyl2+dyr2, dxr-2*dxr2, dyr-2*dyr2, -dxl2, -dyl2, "m")
            go(x0+dxr-dxr2, y0+dyr-dyr2, dxl2, dyl2, dxr2, dyr2, "m")
            go(x0+dxr+dxl2, y0+dyr+dyl2, -dxr2, -dyr2, dxl-2*dxl2, dyl-2*dyl2, "m")
            go(x0+dxr-dxr2+dxl-dxl2, y0+dyr-dyr2+dyl-dyl2, dxl2, dyl2, dxr2, dyr2, "m")
        else:
            dprint("bigblock B")
            go(x0, y0, dxl2, dyl2, dxr2, dyr2, "m")
            go(x0+dxl2+dxr2, y0+dyl2+dyr2, dxr-2*dxr2, dyr-2*dyr2, -dxl2, -dyl2, "m")
            go(x0+dxr-dxr2, y0+dyr-dyr2, dxl2, dyl2, dxr2, dyr2, "m")
            go(x0+dxr+dxl2, y0+dyr+dyl2, -dxr2, -dyr2, dxl-2*dxl2, dyl-2*dyl2, "m")
            go(x0+dxr-dxr2+dxl-dxl2, y0+dyr-dyr2+dyl-dyl2, 2*dxl2-dxl, 2*dyl2-dyl, 2*dxr2-dxr, 2*dyr2-dyr, "m")
            go(x0+dxl2+dxr2, y0+dyl2+dyr2, -dxr2, -dyr2, dxl-2*dxl2, dyl-2*dyl2, "m")
            go(x0+dxl-dxl2, y0+dyl-dyl2, dxl2, dyl2, dxr2, dyr2, "m")
            go(x0+dxl+dxr2, y0+dyl+dyr2, dxr-2*dxr2, dyr-2*dyr2, -dxl2, -dyl2, "m")
            go(x0+dxr-dxr2+dxl-dxl2, y0+dyr-dyr2+dyl-dyl2, dxl2, dyl2, dxr2, dyr2, "m")

if __name__ == "__main__":
    sx = int(sys.argv[1])
    sy = int(sys.argv[2])
    a=spacefill(sx,sy)
    print(a)

