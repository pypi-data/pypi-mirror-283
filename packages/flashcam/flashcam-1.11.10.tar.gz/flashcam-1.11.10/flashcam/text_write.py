
#!/usr/bin/env python3

from fire import Fire
from flashcam.version import __version__
import os
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np


#  Code:  ttfname, FSize(pt), KERN, FHieght, FWidth
#Fheight=>shiftUP txt by it
# default  10,0,10,5
fonts_available = {
    "s8":["small_pixel.ttf",8,0,7,5],
    "s6":["small_pixel.ttf",6,0,6,5],
    "pr":["prstartk.ttf",6,-1,6,5],
    "pr4":["prstartk.ttf",10,-1,10,9],
    "fj":["PixelFJVerdana12pt.ttf",4,0,6,5],
    "fj6":["PixelFJVerdana12pt.ttf",6,0,12,6],
    "re":["retganon.ttf",12,0,9,4],
    "p8":["pixelFJ8pt1__.TTF",8,0,6,5] ,
    "p7":["pixelFJ8pt1__.TTF",7,0,6,5] ,
    "ty":["TypographerFraktur-Medium.ttf",14,0,16,7],
    "v1":["visitor1.ttf",10,0,7,5],
    "v14":["visitor1.ttf",14,0,10,7 ],
    "v2":["visitor2.ttf",12,0,6,5],
    "co":["coders_crux.ttf",16,-1,7,5],
#    "ji":["JikiTourai.ttf",10,0,10,6],
#    "ca":["Caracas.ttf",10,0,10,7],
#    "sa":["SAIBA-45.ttf",12,0,10,7],
#    "ni":["NimbusMono-Regular.otf",12,0,9,7],
#    "nib":["NimbusMono-Bold.otf",12,0,9,7],
#    "li":["LiberationMono-Regular.ttf",12,0,10,7],
#    "cu":["COURIERO.TTF",10,0,8,7],
    "di":["digital-7.mono.ttf",10,0,8,5],
    "di99":["digital-7.mono.ttf",120,0,170,15],
    "vt":["VT323-Regular.ttf",12,-1,6,5],
    "vt4":["VT323-Regular.ttf",14,-1,13,5],
    "utfu":[ "Uni_Sans_Thin.otf", 24, 0, 24, 8 ],  # uppercase thin
    "utfo":[ "OpenSans-Regular.ttf", 24, 0, 30, 12 ],
    "utfg":[ "good_times_rg.otf", 24, 0, 24, 8 ], # uppercase - broad
    "utfp":[ "pricedown_bl.otf", 24, 0, 24, 8 ], # uppercase BoldSignature
    "utfh":[ "hemi_head_bd_it.otf", 24, -2, 24, 14 ]
}

LAST_FONT = None

def set_def_font( font ):
    global LAST_FONT
    if font is None: LAST_FONT = "p8"
    if font in fonts_available.keys():
        LAST_FONT = font
    else:
        LAST_FONT = "p8"


def get_def_font():
    global LAST_FONT
    return LAST_FONT


def get_f_width(font = None):
    global LAST_FONT
    mfont = font
    if mfont is None: mfont = LAST_FONT
    if mfont is None: return 5
    if mfont in fonts_available.keys():
        #LAST_FONT = mfont
        return fonts_available[mfont][4]
    else:
        return 5

def get_f_height(font = None):
    global LAST_FONT
    mfont = font
    if mfont is None: mfont = LAST_FONT
    if mfont is None: return 25
    if mfont in fonts_available.keys():
        #LAST_FONT = mfont
        return fonts_available[mfont][3]
    else:
        return 25

#def iprint( frame, drtext, font, position , color_bgra=(100,0,0,0)  ):
# mess - it seems RGB is needed
#
def iprint( frame, drtext, font, position , color_bgra=(0,255,0)  ):
    global LAST_FONT

    mfont = font
    if mfont is None: mfont = LAST_FONT
    if mfont is None: return frame
    if mfont in fonts_available.keys():
        #print("D.... FONT ACCEPTED:", mfont )
        #print("D.... FONT ACCEPTED:", fonts_available[mfont][0] )
        #LAST_FONT = mfont
        # prepare font
        fname = fonts_available[mfont][0]
        fsize = fonts_available[mfont][1]
        fkern = fonts_available[mfont][2]
        fheig = fonts_available[mfont][3]
        fontpath = os.path.expanduser(f"~/.config/flashcam/{fname}")
        font = ImageFont.truetype(fontpath, fsize)
        # draw
        #img_pil = Image.fromarray(frame.astype('uint8'), 'RGB') # sometimes crashes
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil )

        letter_spacing = fkern
        x,y=position
        # Draw each character with custom spacing
        for chara in drtext:
            #print(f"D...  # # fill@draw = {type(frame)}{frame.shape} {color_bgra} {type(color_bgra)} CHAR={chara}/{ord(chara)}/; {(x, y-fheig)}")
            color_bgra = (255,255,255)
            try:
                draw.text((x, y-fheig), str(chara), fill=color_bgra, font=font, align="left")
            except:
                draw.text((x, y-fheig), chara,  font=font, align="left")

            # THIS WORKS ONLY WITH    pillow==9.0.1 ####################
            char_width, _ = draw.textsize(chara, font=font)
            x += char_width + letter_spacing
        frame = np.array(img_pil)
    return frame



def dial(frame, position, radius=50, thickness=10, color=(0, 255, 0), percentage=100):
    """
    AI generated: too many iterations
use with text:
     FO="v14"
     frame = iprint( frame,
             str(round(100*overtextalpha/255)),
             FO,
             position = (post[0]-2*get_f_width(FO)//2,
             post[1] +get_f_height(FO)//2 ),
             color_bgra= (0,255, 0, 255-int(overtextalpha))
            )

    """
    # Convert the image to a PIL Image
    pil_img = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_img)

    # Calculate the bounding box of the circle
    left_up_point = (position[0] - radius, position[1] - radius)
    right_down_point = (position[0] + radius, position[1] + radius)

    # Calculate the start angle based on the percentage for clockwise drawing
    end_angle = 270  # Ending at the top (north)
    start_angle = end_angle - (360 * (percentage / 100.0))

    # Draw the partial circle (arc)
    draw.arc([left_up_point, right_down_point], start=start_angle, end=end_angle, fill=color, width=thickness)

    # Draw a thin full circle as a guide
    guide_thickness = 1  # Set the thickness of the guide circle
    draw.ellipse([left_up_point, right_down_point], outline=color, width=guide_thickness)

    # Convert back to OpenCV image


    frame = np.array(pil_img)
    FO="v14"
    frame = iprint( frame,
                    str( round(percentage)),
                    FO,
                    position = (position[0]-2*get_f_width(FO)//2,
                                position[1] +get_f_height(FO)//2 ),
                    color_bgra= ( color[0],color[1], color[2] )
                   )
    return frame


def signal_strength(image, position, size=50, color=(0, 255, 0), percentage=100):
    """
    by AI:
    """
    ratio = 2.33
    #print( type(position), position[0], position[1] )
    # Calculate the vertices of the triangle
    bottom_left = position
    bottom_right = (position[0] + size, position[1])

    top_right = (position[0] + size, position[1] - int(size/ratio) )

    # Draw the hollow green triangle
    cv2.line(image, bottom_left, bottom_right, (0, 255, 0), 1)
    cv2.line(image, bottom_right, top_right, (0, 255, 0), 1)
    #cv2.line(image, top_right, bottom_left, (0, 255, 0), 1)

    # Calculate the fill level based on the percentage
    fill_level = int(size * (percentage / 100.0))

    # Draw the filled part of the triangle
    if fill_level > 0:
        pts = np.array([[bottom_left,
                         (bottom_left[0] + fill_level, bottom_left[1]),
                         (bottom_left[0] + fill_level, bottom_left[1] - int((fill_level / size) * int(size/ratio)))]], np.int32)
        cv2.fillPoly(image, [pts], (0, 255, 0))

    FO="v14"
    image = iprint( image,
                    str( round(percentage)),
                    FO,
                    position = (position[0] -get_f_width(FO)//2,
                                position[1] -get_f_height(FO) ),
                    color_bgra= ( color[0],color[1], color[2] )
                   )
    return image


def text_box(image, position, box_size=(80,120), color=(0,255,0),split_height=20,  title="Title", values = "rate 123.2 uSv\n tot 220 mSv"):
    # Calculate the corners of the box
    top_left = position
    FO="v14"
    maxw=0
    for i in values.split("\n"):
        a = get_f_width(FO)*(len(str(i))+2)
        if a>maxw: maxw=a

    #xbox_size[1] = maxw
    xbox_size = [ maxw  , get_f_height(FO)* (len(values.split("\n"))+3)  ]

    bottom_left = (position[0], position[1] + xbox_size[1])
    top_right = (position[0] + xbox_size[0], position[1])
    bottom_right = (position[0] + xbox_size[0], position[1] + xbox_size[1])

    # Draw the rectangle for the text box in green
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 1)

    # Draw the horizontal split line in green
    split_line_start = (position[0], position[1] + split_height)
    split_line_end = (position[0] + xbox_size[0], position[1] + split_height)
    cv2.line(image, split_line_start, split_line_end, (0, 255, 0), 1)

    FO = "v14"
    image = iprint( image,
                    str( title),
                    FO,
                    position = (position[0]  +get_f_width(FO),
                                position[1] + 1.2*get_f_height(FO) ),
                    color_bgra= ( color[0],color[1], color[2] )
                   )
    nsk=0
    for i in values.split("\n"):
        image = iprint( image,
                        str( i),
                        FO,
                        position = (position[0] +get_f_width(FO),
                                    position[1] +(nsk+3)* get_f_height(FO) ),
                        color_bgra= ( color[0],color[1], color[2] )
                       )
        nsk+=1


    return image

def main():
    print()

if __name__=="__main__":
    Fire(main)
