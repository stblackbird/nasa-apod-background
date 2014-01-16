#!/usr/bin/env python
"""
desktop_nasa.py

DESCRIPTION
Gets the latest image of the day from NASA, http://apod.nasa.gov/apod/,
gets the description for that image, resize image, write description to it
and set it as the background in Gnome.

INSTALLATION
To make this work you will need to set a valid font path, a download folder
which should exist and change the resolution variables to that of your screen.
Furthermore if you want this to automatically update your desktop you should add
this script to cron jobs, or to startup applications. Also download all needed
python libraries.

ON UBUNTU JUST RUN

sudo apt-get install python-imaging

then go to
System -> Preferences -> Startup Applications
then add script like this
python /dir/to/script/desktop_nasa.x.x.py

ALSO SET VARIABLE
DOWNLOAD = '/home/stathis/.backgrounds/'
to a directory that script can use

For any suggestions, improvements, bugs feel free to contact me at
stmayridopoulos@hotmail.com

Based on a script of Christian Stefanescu, http://0chris.com

intelli_draw method from:
http://mail.python.org/pipermail/image-sig/2004-December/003064.html
"""
import commands
import urllib
import urllib2
import re
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

# Configurable Settings
# FONTS
FONT_PATH = '/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf'
FONT_SIZE = 20
FONT_COLOR = (255, 255, 255)
# Select False if you don't want any description
GET_IMAGE_ONLY = False
# Future Option
# Valid values are [top, bottom, left, right]
# text_positioning = 'top'
NASA_POD_SITE = 'http://apod.nasa.gov/apod/'
DOWNLOAD = os.getenv("HOME") + '/.backgrounds/'
# This is default resolution, if dynamic method doesn't work
RESOLUTION_X, RESOLUTION_Y = 1920, 1080
# globals
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


# FUNCTIONS

def download_site(url):
    ''' Download contents from url and return it. '''
    opener = urllib2.build_opener()
    req = urllib2.Request(url)
    response = opener.open(req)
    reply = response.read()
    return reply

def get_resolution():
    ''' Get desktop resolution.
       xrandr  | grep \* | cut -d' ' -f4'''
    command = "xrandr  | grep \* | cut -d' ' -f4"
    status, output = commands.getstatusoutput(command)
    ret = output.split('x')
    try:
        ret[0] = int(ret[0])
        ret[1] = int(ret[1])
    except:
        return ['', '']
    return ret
    

def get_img_title(text):
    ''' Get the image title from site contents. '''
    ret_value = ''
    title_regex = '\<b\> (.*?) \<\/b\>'
    try:
        reg = re.search(title_regex, text)
    except sre_constants.error:
        pass
    try:
        ret_value = reg.group(1)
    except AttributeError:
        return False
    return ret_value
    

def get_img_description(text):
    ''' Get the image description from site contents. '''
    descr_regex = '\<b\> Explanation: \<\/b\>(.*)\<p\> \<center\>'
    try:
        reg = re.search(descr_regex, text, re.DOTALL)
    except sre_constants.error:
        pass
#   Next filter links, \', newline character before returning
    try:
        raw_descr = reg.group(1)
    except AttributeError:
        return ''
# Delete Newline characters
    ret_value = re.sub('\n',' ', raw_descr)
# Delete all html tags
    ret_value = re.sub('\<.*?\>', '', ret_value)
# Ignore multiple spaces
    ret_value = re.sub('\s+', ' ', ret_value)
    return ret_value

def get_image(text):
    ''' Get image url from text and save it to an temp image file. 
        Return both filenames, temp and real. '''
    reg = re.search('<a href="(image.*?)"',text, re.DOTALL)
    if 'http' in reg.group(1):
        # Contains url
        file_url = reg.group(1)
    else:
        # Contains relative img path
        file_url = NASA_POD_SITE + reg.group(1)
    filename = os.path.basename(file_url)
    remote_file = urllib.urlopen(file_url)
    (temp_filename, instance) = urllib.urlretrieve(file_url)
    return temp_filename, filename

def intelli_draw(drawer, text, font, containerWidth):
    ''' Figures out how many lines (and at which height in px) are needed to 
        print
        the given text with the given font on an image with the given size.

        Source:
        http://mail.python.org/pipermail/image-sig/2004-December/003064.html
    '''
    words = text.split()
    lines = []
    lines.append(words)
    finished = False
    line = 0
    while not finished:
        thistext = lines[line]
        newline = []
        innerFinished = False
        while not innerFinished:
            if drawer.textsize(' '.join(thistext), font)[0] > containerWidth:
                newline.insert(0, thistext.pop(-1))
            else:
                innerFinished = True
        if len(newline) > 0:
            lines.append(newline)
            line = line + 1
        else:
            finished = True
    tmp = []
    for i in lines:
        tmp.append(' '.join(i))
    lines = tmp
    (width, height) = drawer.textsize(lines[0], font)
    return (lines, width, height)

def create_image_text(save_to, temp_image, text):
    '''  '''
    image = Image.open(temp_image)
    (img_width, img_height) = image.size
    # resize to desktop resolution
    # should keep propotions of original image!
    prop_x = float(RESOLUTION_X) / img_width
    prop_y = float(RESOLUTION_Y) / img_height
    prop = min(prop_x, prop_y)
    # Those are the resolutions of the new image
    res_x = int(img_width * prop)
    res_y = int(img_height * prop)
    image = image.resize((res_x, res_y), Image.ANTIALIAS)
    # Add a black background
    background = Image.new('RGB', (RESOLUTION_X, RESOLUTION_Y), (0, 0, 0))
    bg_w, bg_h = background.size
    offset = ((bg_w - res_x) / 2, (bg_h - res_y) / 2)
    background.paste(image, offset)
    if text == '':
        # we just want the image
        pass
    else:
        # I don't want text to occupy image from edge to edge
        text_margin = 0.025  # 10% left and 10% right
        (img_width, img_height) = background.size
        text_margin_pix = text_margin * img_width
        img_width = int( img_width - 2 * text_margin_pix)
        draw = ImageDraw.Draw(background)
        lines, tmp, h = intelli_draw(draw, text, font, img_width)
        j = 0
        for i in lines:
            draw.text((0 + text_margin_pix, 0 + j * h + text_margin_pix),  # where to draw (start @ (0,0))
                    i,  # actual line
                    font=font,  # font to use
                    fill=FONT_COLOR)  # text color
            j = j + 1
    fhandle = open(save_to, 'w')
    background.save(fhandle, 'JPEG')

def set_gnome_wallpaper(file_path):
    command = "gsettings set org.gnome.desktop.background picture-uri file://" + file_path
    status, output = commands.getstatusoutput(command)
    return status
    

if __name__ == '__main__':
    # create download directory
    if not os.path.exists(os.path.expanduser(DOWNLOAD)):
        os.makedirs(os.path.expanduser(DOWNLOAD))

    screen_resolution = get_resolution()
    if screen_resolution:
        [RESOLUTION_X, RESOLUTION_Y] = screen_resolution

    site_contents = download_site(NASA_POD_SITE)
    if GET_IMAGE_ONLY == False:
        title = get_img_title(site_contents)
        title = title + ': '
        description = get_img_description(site_contents)
    else:
        title = ''
        description = ''
    temp_filename, filename = get_image(site_contents)
    create_image_text(DOWNLOAD + filename, temp_filename, title + description)
    status = set_gnome_wallpaper(DOWNLOAD + filename)
