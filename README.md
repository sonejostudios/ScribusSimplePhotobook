# ScribusSimplePhotobook
This is a simple photobook layout generator script for scribus.


![screenshot](https://raw.githubusercontent.com/sonejostudios/ScribusSimplePhotobook/master/simple_photobook.png "Layout Example")


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

About image border:
The image border size adds a border around each image, 
but not around the page (this is set by the page frame size).
So the distance between images is twice the border size,
while the distance to the document's border is only the border size.
If you want everywhere the same borders, a good starting point
is to set the same number for page frame size and image border size.

Examples (page frame size, image border size):
* Same border everywhere (6mm): 3, 3
* Frameless (with 3mm bleed), no image borders: -3, 0
* Big frame, thin borders: 10, 1

Tip:
Set the document's margins like page frame size + image border size,
so you can easily modify the layouts using the margins' and the guides' snapping.
Example: 
* Document's margins = 6mm
* Page frame size = 3mm
* Image border size = 3mm

Default variable fields:
Using the option 'v' will create 3 text fields left outside the first page.
Use them to set the default page frame size, the default image border size
and the default layout style.
