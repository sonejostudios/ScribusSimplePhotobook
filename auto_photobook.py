#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os

try:
    import scribus
except ImportError:
    print("This Python script is written for the Scribus scripting interface.")
    print("It can only be run from within Scribus.")
    sys.exit(1)




def main(argv):

    
###########################################    


    info_text = '''
    Welcome to Auto-Photobook!
    
    1. Select the process mode:
        9f = creates a 9x9 layout on each page and fill them with images.
        4f = creates a 4x4 layout on each page and fill them with images.
        
        9e = creates an empty 9x9 layout on each page.
        4e = creates an empty 4x4 layout on each page.
        
        9f+4f = creates a filled 9x9 layout on odd pages and a filled 4x4 layout on even pages.
        9e+4e = creates an empty 9x9 layout on odd pages and an empty 4x4 layout on even pages.
        
        9f+4e = creates a filled 9x9 layout on odd pages and an empty 4x4 layout on even pages (default).
        9e+4f = creates an empty 9x9 layout on odd pages and a filled 4x4 layout on even pages.

    2. Select a document layout, the margins (they need to be equal) and the bleed (if needed). Ignore the number of pages.
    
    3. Define the space between the images (default: 6mm).
    
    4a. If "9f" or "4f" is in your mode, you can choose an image folder and an image filter will be prompted.
    4b. Otherwise, set the amount of pages you want to create (default: 10 pages).
    
    5. Wait until it is done...
    
    6. Adjust you layouts and move your images as you need.
    
    
    Process mode:'''
    
# start dialog, choose mode

    #scribus.messageBox("Auto-Photobook", info_text)
    todo = scribus.valueDialog("Auto-Photobook", info_text, "9f+4e")
    todo = list(todo.split("+"))
    
    
    # wrong process mode
    if "9f" not in todo and "9e" not in todo and "4f" not in todo and "9e" not in todo:
        scribus.messageBox("Error", "Wrong process mode. Auto-Photobook was cancelled.") 
        sys.exit()


    # show new document dialog
    newdoc = scribus.newDocDialog()
    

    # exit if cancelled
    if newdoc == False:
        scribus.messageBox("Exit", "Auto-Photobook was cancelled.") 
        sys.exit()
    

    if scribus.haveDoc:
        scribus.setUnit(scribus.UNIT_MILLIMETERS)                                       
        (w,h) = scribus.getPageSize() 

        ###################
        
        # delete all pages except the first:
        pageamount = scribus.pageCount()
        while pageamount > 1:
            scribus.deletePage(pageamount)
            pageamount = scribus.pageCount()
            
            
        # set image border and bleed
        border = int(scribus.valueDialog("Space between images", "Define the space between the images (mm).", "6"))
        #border = 6
        
        # reset image border for easier calculations
        border = border*0.75
        


        if "9f" in todo or "4f" in todo:
            # ask for workdir
            workdir = scribus.fileDialog("Open directory with images", "", haspreview=False, issave=False, isdir=True)
            #workdir = "/media/sda7/Programming/Python/scribus_auto_photobook/pics"

            
            # file filter
            filefilter = scribus.valueDialog("File filter", "File filter examples: \n\n* or *.* = add all files\n*.jpg = add .jpg files only\nIMG_*.* = add all files starting with IMG_\n\nThis filter is case sensitive!","*.*")

            # get image paths 
            filelist = sorted(glob.glob(os.path.join(workdir,filefilter)))
            #filelist = sorted(glob.glob(os.path.join(workdir, "*")))
            
            # count files
            filesinworkdir = len(filelist)
            scribus.messageBox("Files in directory", "Images matched in folder: " + str(filesinworkdir))
            
            #error
            if filesinworkdir == 0:
                scribus.messageBox("Error", "This directory is empty.")
                sys.exit()

            #messagebar text
            scribus.messagebarText("Importing images...")
            
            #progressbar max
            scribus.progressTotal(filesinworkdir)
            
            # set maxpages (not needed here but needs to be assigned) 
            maxpages = len(filelist)
            
            
        else:
            # ask for page amount
            maxpages = int(scribus.valueDialog("Set page amount", "How many pages you want to create?", "10"))
            
            #progressbar max
            scribus.progressTotal(maxpages)
        

        
        
        # get page size (without bleed)
        size = scribus.getPageSize()
        
        # get margins
        margins = scribus.getPageMargins()[0]
        
        
        # set page final size
        final_size = (size[0]-margins, size[1]-margins)
        

        # simplify calc for 9x9 layout
        guide_layout_x =  final_size[0]/3-margins/3
        guide_layout_y =  final_size[1]/3-margins/3
        
        
        # set indexes
        page = 1
        pic = 0
        
        
        #create pages, add and load images
        x = True    
        while x == True:
            scribus.progressSet(page)
            scribus.gotoPage(page)
            
            
            # create 9x9 layout
            if "9f" in todo or "9e" in todo:
        
                #guides
                scribus.setVGuides([margins+guide_layout_x-border, margins+guide_layout_x+border/2,  margins+guide_layout_x*2-border/2, margins+guide_layout_x*2+border])
                scribus.setHGuides([margins+guide_layout_y-border, margins+guide_layout_y+border/2,  margins+guide_layout_y*2-border/2, margins+guide_layout_y*2+border])
                

                # create images
                scribus.createImage(margins, margins, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image1")
                scribus.createImage(margins+guide_layout_x+border/2, margins, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image2")
                scribus.createImage(margins+guide_layout_x*2+border, margins, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image3")
                
                scribus.createImage(margins, margins+guide_layout_y+border/2, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image4")
                scribus.createImage(margins+guide_layout_x+border/2, margins+guide_layout_y+border/2, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image5")
                scribus.createImage(margins+guide_layout_x*2+border, margins+guide_layout_y+border/2, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image6")
                
                scribus.createImage(margins, margins+guide_layout_y*2+border, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image7")
                scribus.createImage(margins+guide_layout_x+border/2, margins+guide_layout_y*2+border, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image8")
                scribus.createImage(margins+guide_layout_x*2+border, margins+guide_layout_y*2+border, guide_layout_x+border-border*2, guide_layout_y-border, "page"+str(page)+"image9")
                
                

                #load and scale images
                if "9f" in todo:
            
                    try:
                        scribus.loadImage(filelist[pic], "page"+str(page)+"image1")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image1")
                        
                        scribus.loadImage(filelist[pic+1], "page"+str(page)+"image2")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image2")
                        
                        scribus.loadImage(filelist[pic+2], "page"+str(page)+"image3")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image3")
                        
                        scribus.loadImage(filelist[pic+3], "page"+str(page)+"image4")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image4")
                        
                        scribus.loadImage(filelist[pic+4], "page"+str(page)+"image5")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image5")
                        
                        scribus.loadImage(filelist[pic+5], "page"+str(page)+"image6")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image6")
                        
                        scribus.loadImage(filelist[pic+6], "page"+str(page)+"image7")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image7")
                        
                        scribus.loadImage(filelist[pic+7], "page"+str(page)+"image8")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image8")
                        
                        scribus.loadImage(filelist[pic+8], "page"+str(page)+"image9")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image9")
                    
                    except:
                        x = False
                    
                    
                    # increase picture index
                    pic += 9

                
                # add page
                scribus.newPage(-1)
                page += 1
            
            
            
            # create 4x4 layout
            if "4f" in todo or "4e" in todo:
            
                #guides
                scribus.setVGuides([size[0]/2-border*0.75, size[0]/2+border*0.75])
                scribus.setHGuides([size[1]/2-border*0.75, size[1]/2+border*0.75])
                
                
                # create images
                scribus.createImage(margins, margins, size[0]/2-border*0.75-margins, size[1]/2-border*0.75-margins, "page"+str(page)+"image1")
                scribus.createImage(size[0]/2+border*0.75, margins, size[0]/2-border*0.75-margins, size[1]/2-border*0.75-margins, "page"+str(page)+"image2")
                
                scribus.createImage(margins, size[1]/2+border*0.75, size[0]/2-border*0.75-margins, size[1]/2-border*0.75-margins, "page"+str(page)+"image3")
                scribus.createImage(size[0]/2+border*0.75, size[1]/2+border*0.75, size[0]/2-border*0.75-margins, size[1]/2-border*0.75-margins, "page"+str(page)+"image4")


                #load and scale images
                if "4f" in todo:
                    try:
                        
                        scribus.loadImage(filelist[pic], "page"+str(page)+"image1")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image1")
                        
                        scribus.loadImage(filelist[pic+1], "page"+str(page)+"image2")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image2")
                        
                        scribus.loadImage(filelist[pic+2], "page"+str(page)+"image3")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image3")
                        
                        scribus.loadImage(filelist[pic+3], "page"+str(page)+"image4")
                        scribus.setScaleImageToFrame(True, proportional=True, name="page"+str(page)+"image4")
                        
                    
                    except:
                        x = False
                    
                    
                    # increase picture index
                    pic += 4

            
            
                # add page
                scribus.newPage(-1)
                page += 1
            
            
            #scribus.setImageOffset(0, 0, "imagename"+str(page))
            #scribus.setScaleFrameToImage(name="imagename"+str(page))
            

            # stop if maxpages reached
            if page > maxpages:
                x = False

            
            
        #delete last blank page
        scribus.deletePage(page)

       
    
    


##########################################   


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


