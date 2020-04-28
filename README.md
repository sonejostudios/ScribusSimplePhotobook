# ScribusSimplePhotobook
This is a bundle of two simple photobook layout generators for scribus.


![screenshot](https://raw.githubusercontent.com/sonejostudios/ScribusSimplePhotobook/master/simple_photobook.png "Layout Example")


## Description
There are 2 scripts with different functions.

1. __Auto-Photobook:__ This will create 9x9 and/or a 4x4 layout with guides and optionally fill them with pictures found in a choosen folder. This script is good to automatically create a whole photo book out of an image collection. This will create a new document on each start.

2. __Simple-Photobook:__ This script needs to be started on each page. It generates the choosen layout on the page.



## Use them in Scribus
1. Download the scripts to your computer
2. Start Scribus (you'll need Scribus >= 1.5.5.) 
3. Go to the menu "Scripter", choose "Execute Script..." and point to the script you want to use.
After this, the last used script can be found in the menu "Scripter/Recent Scripts"
4. Go to the menu "Page" and check "Snap to Guides"
5. Adjust you layouts and move your images as you need



## Auto-Photobook
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

4.
    If "9f" or "4f" is in your mode, you can choose an image folder and an image filter will be prompted.
    Otherwise, set the amount of pages you want to create (default: 10 pages).

5. Wait until it is done...

6. Adjust you layouts and move your images as you need.



## Simple-Photobook

__Usage:__
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


__About image border:__

The image border size adds a border around each image, 
but not around the page (this is set by the page frame size).
So the distance between images is twice the border size,
while the distance to the document's border is only the border size.
If you want everywhere the same borders, set the same number for page frame size and image border size.

Examples (page frame size, image border size):
* Same border everywhere (6mm): 3, 3
* Frameless (with 3mm bleed), no image borders: -3, 0
* Big frame, thin borders: 10, 1


__Tip:__

Set the document's margins like page frame size + image border size,
so you can easily modify the layouts using the margins' and the guides' snapping.
Example: 
* Document's margins = 6mm
* Page frame size = 3mm
* Image border size = 3mm


__Default variable fields:__

Using the option 'v' will create 3 text fields left outside the first page.
Use them to set the default page frame size, the default image border size
and the default layout style.


