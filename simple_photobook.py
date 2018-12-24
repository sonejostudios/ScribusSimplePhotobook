#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)


help_text = """
1. Choose the layout you want to add to the selected page.

2. Set the page frame size.
    This is the distance between the document's border (not the bleed)
    and the layouts.
    If you want a frameless layout, set here the document's bleed
    with a negative number, i.e. -3 if your bleed is 3mm.

3. Set the border size of the images.
    This will add a border around the images.
    If you want images without borders, set 0.
    This is not needed if only one image is used in the layout.
    Use the page frame size instead.

About image border:
The image border size adds a border around each image, 
but not around the page (this is set by the page frame size).
So the distance between images is twice the border size,
while the distance to the document's border is only the border size.
If you want everywhere the same borders, a good starting point
is to set the same number for page frame size and image border size.

Examples (page frame size, image border size):
    Same border everywhere (6mm): 3, 3
    Frameless (with 3mm bleed), no image borders: -3, 0
    Big frame, thin borders: 10, 1

Tip:
Set the document's margins like page frame size + image border size,
so you can easily modify the layouts using the margins' and the guides' snapping.
Example: 
    Document's margins = 6mm
    Page frame size = 3mm
    Image border size = 3mm

Default variable fields:
Using the option 'v' will create 3 text fields left outside the first page
(with the object property print disabled by default).
Use them to set the default page frame size, the default image border size
and the default layout style.
"""


layout_text = """
Choose a layout :

0 = 1 image on 2 pages
1 = 1 image on 1 page
2 = 2 vertical images
22 = 2 horizontal images
3 = 1 image left, 2 images right
33 = 2 images left, 1 image right
333 = 1 image on top, 2 images on bottom
3333 = 2 images on top, 1 image on bottom
4 = 4 images
6 = 6 images, 3x2
66 = 6 images, 2x3
9 = 9 images

h = help
v = create default variable fields
"""


if scribus. objectExists("myframe") == True:
    myframe = scribus.getText("myframe")
else:
    myframe = "3"
    
if scribus. objectExists("myborder") == True:
    myborder = scribus.getText("myborder")
else:
    myborder = "3"
    
if scribus. objectExists("mylayout") == True:
    mylayout = scribus.getText("mylayout")
else:
    mylayout = "h"


#scribus.messageBox("Values", myframe + "\n" + myborder)



def createDefaultVal():
    scribus.gotoPage(1)
    if scribus. objectExists("myframe") == False:
        scribus.createText(-70, 10, 40, 10, "myframelabel")
        scribus.setText("Default Frame:", "myframelabel")
        scribus.setProperty("myframelabel", "m_PrintEnabled", False)
        
        scribus.createText(-30, 10, 10, 10, "myframe")
        scribus.setText("3", "myframe")
        scribus.setProperty("myframe", "m_PrintEnabled", False)
        
    if scribus. objectExists("myborder") == False:
        scribus.createText(-70, 30, 40, 10, "myborderlabel")
        scribus.setText("Default Border:", "myborderlabel")
        scribus.setProperty("myborderlabel", "m_PrintEnabled", False)
        
        scribus.createText(-30, 30, 10, 10, "myborder")
        scribus.setText("3", "myborder")
        scribus.setProperty("myborder", "m_PrintEnabled", False)
        
    if scribus. objectExists("mylayout") == False:
        scribus.createText(-70, 50, 40, 10, "mylayoutlabel")
        scribus.setText("Default Layout:", "mylayoutlabel")
        scribus.setProperty("mylayoutlabel", "m_PrintEnabled", False)
        
        scribus.createText(-30, 50, 10, 10, "mylayout")
        scribus.setText("h", "mylayout")
        scribus.setProperty("mylayout", "m_PrintEnabled", False)



def main(argv):
    unit = scribus.getUnit()
    units = ['pts','mm','inches','picas','cm','ciceros']
    unitlabel = units[unit]
    
    #layout_style = ""
    #frame = 3
    #border = 3
    
# layout style
    layout_style = scribus.valueDialog("Layout Style", layout_text, mylayout)
    
    if layout_style == "h":
        scribus.messageBox("Help", help_text)
        sys.exit()
        
    if layout_style == "v":
        createDefaultVal()
        sys.exit()
    if layout_style == "":
        sys.exit()
    
# frame
    frame_str = scribus.valueDialog("Set Page Frame", "Set page frame size ("+unitlabel+") :\n(positiv for page margin,\nnegativ for page bleed)\n", myframe)
    
    if frame_str != "":
        frame = float(frame_str)
    else:
        sys.exit()
    
    
# border
    if int(layout_style) > 1:
        border_str = scribus.valueDialog("Add Image Border", "Add border around images ("+unitlabel+") :\n", myborder)
        if border_str != "":
            border = float(border_str)
        else:
            sys.exit()
    else:
        border = 0
    
    bleed = -frame
    

# get page size
    xysize = scribus.getPageSize()
    size = (xysize[0]+2*bleed , xysize[1]+2*bleed)
    #scribus.createImage(0, 0, size[0]/2, size[1]/2)
    
    
        
# layouts
# one image on two pages (put it on the left page)    
    if layout_style == "0": 
        scribus.createImage(0+border-bleed, 0+border-bleed, (size[0]*2)-border-bleed*2, size[1]-border)
    
# one image on one full page
    if layout_style == "1":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]-border*2, size[1]-border*2)
    
    
# two vertical images 
    if layout_style == "2":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]-border*2)
        scribus.createImage(size[0]/2+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        #scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
        
    
# two horizontal images
    if layout_style == "22": 
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]-border*2, size[1]/2-border*2)
        scribus.createImage(0+border-bleed, size[1]/2+border-bleed, size[0]-border*2, size[1]/2-border*2)
        
        #guides
        #scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
    
# one vertical image left, two horizontal images right
    if layout_style == "3": 
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]-border*2)
        scribus.createImage(size[0]/2+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/2+border-bleed, size[1]/2+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
    
# one vertical image left, two horizontal images right
    if layout_style == "33": 
        scribus.createImage(size[0]/2+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]-border*2)
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(0+border-bleed, size[1]/2+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
    
# one image on top, two images on bottom
    if layout_style == "333": 
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]-border*2, size[1]/2-border*2)
        scribus.createImage(0+border-bleed, size[1]/2+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/2+border-bleed, size[1]/2+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
    
# one image on top, two images on bottom
    if layout_style == "3333":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/2+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(0+border-bleed, size[1]/2+border-bleed, size[0]-border*2, size[1]/2-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
    
# four horizontal images 
    if layout_style == "4":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/2+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(0+border-bleed, size[1]/2+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/2+border-bleed, size[1]/2+border-bleed, size[0]/2-border*2, size[1]/2-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])

    
# six images 3 + 3
    if layout_style == "6":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/3-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/3+border-bleed, 0+border-bleed, size[0]/3-border*2, size[1]/2-border*2)
        scribus.createImage((size[0]/3)*2+border-bleed, 0+border-bleed, size[0]/3-border*2, size[1]/2-border*2)
        scribus.createImage(0+border-bleed, size[1]/2+border-bleed, size[0]/3-border*2, size[1]/2-border*2)
        scribus.createImage(size[0]/3+border-bleed, size[1]/2+border-bleed, size[0]/3-border*2, size[1]/2-border*2)
        scribus.createImage((size[0]/3)*2+border-bleed, size[1]/2+border-bleed, size[0]/3-border*2, size[1]/2-border*2)
        
        #guides
        scribus.setVGuides([size[0]/3-border-bleed, size[0]/3-bleed+border,(size[0]/3)*2-border-bleed,(size[0]/3)*2+border-bleed])
        scribus.setHGuides([size[1]/2-border-bleed, size[1]/2+border-bleed])
        
# six images 2 +2 + 2
    if layout_style == "66":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/2-border*2, size[1]/3-border*2)
        scribus.createImage(size[0]/2+border-bleed, 0+border-bleed, size[0]/2-border*2, (size[1]/3)-border*2)
        scribus.createImage(0+border-bleed, size[1]/3+border-bleed, size[0]/2-border*2, size[1]/3-border*2)
        scribus.createImage(size[0]/2+border-bleed, size[1]/3+border-bleed, size[0]/2-border*2, (size[1]/3)-border*2)
        scribus.createImage(0+border-bleed, (size[1]/3)*2+border-bleed, size[0]/2-border*2, size[1]/3-border*2)
        scribus.createImage(size[0]/2+border-bleed, (size[1]/3)*2+border-bleed, size[0]/2-border*2, (size[1]/3)-border*2)
        
        #guides
        scribus.setVGuides([size[0]/2-border-bleed, size[0]/2+border-bleed])
        scribus.setHGuides([size[1]/3-border-bleed, size[1]/3+border-bleed, (size[1]/3)*2-border-bleed, (size[1]/3)*2+border-bleed])


# nine images
    if layout_style == "9":
        scribus.createImage(0+border-bleed, 0+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage(size[0]/3+border-bleed, 0+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage((size[0]/3)*2+border-bleed, 0+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage(0+border-bleed, size[1]/3+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage(size[0]/3+border-bleed, size[1]/3+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage((size[0]/3)*2+border-bleed, size[1]/3+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage(0+border-bleed, (size[1]/3)*2+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage(size[0]/3+border-bleed, (size[1]/3)*2+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        scribus.createImage((size[0]/3)*2+border-bleed, (size[1]/3)*2+border-bleed, size[0]/3-border*2, size[1]/3-border*2)
        
        #guides
        scribus.setVGuides([size[0]/3-border-bleed, size[0]/3-bleed+border,(size[0]/3)*2-border-bleed,(size[0]/3)*2+border-bleed])
        scribus.setHGuides([size[1]/3-border-bleed, size[1]/3+border-bleed, (size[1]/3)*2-border-bleed, (size[1]/3)*2+border-bleed])
        
        

def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()


# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)


