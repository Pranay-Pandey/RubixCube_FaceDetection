import cv2
import os
import numpy as np

# img = cv2.imread("Input/20.jpg")

folderpath = "Input"
outputpath = "Output"
mylist = os.listdir(folderpath)
list = []

for imPath in mylist:
    img = cv2.imread(f'{folderpath}/{imPath}')
    list.append(img)
    impath_without_extention = os.path.splitext(imPath)[0]
    h , w, c = img.shape

    points = []
    colors = [1]
    colors_count = 2
    i = 0
    co = 1
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
    edged = cv2.Canny(gray, 50, 200)
    edged = cv2.dilate(edged,None, iterations=1)
    edged = cv2.erode(edged, None,iterations=1)
    edged = cv2.dilate(edged,None, iterations=1)
    edged = cv2.erode(edged, None,iterations=1)
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    for c in contours:
        A1 = cv2.contourArea(c)
        if A1<h*w/2 and A1>80:
            perimeter = cv2.arcLength(c,True)
            if cv2.norm(((perimeter/4)*(perimeter/4))-A1)<300:
                co = 1
                if(i==9):
                    break
                x,y,w1,h1 = cv2.boundingRect(c)
                # for k in range(0,i+1):
                #     if(k==0):
                #         break
                #     if(points[k][1]==x and points[k][2]==y):
                #         co = 0
                #         break
                b,g,r = img[int(y+h1/2),int(x+w1/2)]
                point = [x+w1/2,y+h1/2,b,g,r]
                if point not in points:
                    points.append(point)
                    cv2.rectangle(img,(x,y),(x+w1,y+h1),(255,0,255),2)
                    i = i+1
        
                # cv2.drawContours(img,c,0,(169,0,255),5)


    # def draw_function(event,x,y,flags,params):
    #     if event == cv2.EVENT_LBUTTONDBLCLK:
    #         print(x,y)

    
    
    # cv2.setMouseCallback('img',draw_function)
    points.sort()
    
    if(i==9):
        for q in range(1,9):
            unique_color = 1
            cb,cg,cr = points[q][2],points[q][3],points[q][4]
            for j in range(0,q):
                bb,bg,br = points[j][2],points[j][3],points[j][4]
                b,g,r = 0,0,0
                if(bb>cb):
                    b = bb-cb
                else:
                    b = cb-bb
                if(bg>cg):
                    g = bg-cg
                else:
                    g = cg-bg
                if(cr>br):
                    r = cr-br
                else:
                    r = br-cr
                if(b<25 and g<25 and r<25):
                    colors.append(colors[j])
                    unique_color = 0
                    break
            if(unique_color==1):
                colors.append(colors_count)
                colors_count = colors_count+1
        
        f = open(f'{outputpath}/'+"output_"+impath_without_extention+'.txt',"w")
        f.write(str(colors[0]) + " " + str(colors[3]) + " " +str(colors[6]))
        f.write("\n"+str(colors[1]) + " " + str(colors[4]) + " " +str(colors[7]))
        f.write("\n"+str(colors[2]) + " " + str(colors[5]) + " " +str(colors[8]))
        f.close()



#cv2.waitKey(0)
cv2.destroyAllWindows
