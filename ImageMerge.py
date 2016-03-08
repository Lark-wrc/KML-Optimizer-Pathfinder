from PIL import Image

debug = 0
diffnum = 50

def mergeModeRGB(outfile, base, *images):
    """
    This merges a list of images, with layers of paths and markers, on top of a plain base image. It will then
    output the merged image to the outfile provided. This method only works with images encoded in RGB color,
    which is expected of it's inputs. The method works by creating a new file for the changes, and opening the base
    and a layer. Each pixel in the base is compared with the layer, if they're different enough the layer pixel is
    placed over the original base image pixel that was contained in the new file. This is done for every pixel and
    every layer. Debug information contains the ratio of different to not different pixels in percent form, as well
    as a display of the output after each layer merge.
    :param outfile: The file address to save the output file to.
    :param base: The unmodified image which all the layers will be drawn to. The images MUST line up, which is why
                    the center and zoom are REQUIRED. Those parameters being the same will line up the unchanged pixels
                    correctly so that only the edited pixels pick up as different.
    :param images: Any number of image urls that are layers of the base image. Same center and zoom are a must.
    """

    baseimage = Image.open(base)
    baseimage.save(outfile)
    layeringimage = Image.open(outfile)

    basedata = baseimage.load()
    layeringdata = layeringimage.load()

    for top in images:
        topimage = Image.open(top)
        topdata = topimage.load()
        counter = 0


        for x in range(baseimage.size[0]):
            for y in range(baseimage.size[1]):
                bpix = basedata[x,y]
                tpix = topdata[x,y]
                #print x, y, bpix, tpix, baseimage.mode, baseimage.format
                if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                    layeringdata[x,y] = tpix
                    counter += 1

        if debug: print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
            360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
        if debug: layeringimage.show()

    print ""
    layeringimage.save(outfile)


def blkDiff(base, images, outfile="DifferenceFile.png"):
    """
    This method will change the color of any pixel that is different between a base image and another provided
    image. This works in the same way as mergeRGB, which does mean the inputs need to be RGB format. You can use this
    to visually see the detected differences between two images.
    :param base: The first image to compare. It does have to be at the same center and zoom as the below image.
    :param images: the image to compare to base.
    :param outfile: The file to write the color marked image to.
    :return:
    """
    baseimage = Image.open(base)
    baseimage.save(outfile)
    layeringimage = Image.open(outfile)

    basedata = baseimage.load()

    layeringdata = layeringimage.load()

    topimage = Image.open(images)
    topdata = topimage.load()
    counter = 0

    for x in range(baseimage.size[0]):
        for y in range(baseimage.size[1]):
            bpix = basedata[x,y]
            tpix = topdata[x,y]
            if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                layeringdata[x,y] = (0,0,0,255)
                counter += 1

    if debug: print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
        360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
    if debug: layeringimage.show()

    if debug: print ""
    layeringimage.save(outfile)

def convertPtoRGB(*images):
    """
    This method takes any number of images and converts the from P color mode to RGB mode. RGB is required by the
    merge methods above. The files are saved to a different file, same prefix, but .con being placed at the end.
    :param images: The images that need to be converted. They are expected to be in P color mode, though other modes
            may convert cleanly.
    :return: A list of the new file locations, since the file names have been changed.
    """
    ret = []
    for image in images:
        img = Image.open(image)
        im = img.convert("RGBA")
        ret.append(image[:-4]+'.con'+image[-4:])
        im.save(image[:-4]+'.con'+image[-4:])
    return ret

class MergeGenerator(object):
    
    def __init__(self, outfile, base):
        base = convertPtoRGB(base)[0]
        baseimage = Image.open(base)
        baseimage.save(outfile)
        self.outfile = outfile
        self.base = base

    def add(self, new):
        """
        :param outfile: The file address to save the output file to.
        :param base: The unmodified image which all the layers will be drawn to. The images MUST line up, which is why
                        the center and zoom are REQUIRED. Those parameters being the same will line up the unchanged pixels
                        correctly so that only the edited pixels pick up as different.
        :param images: Any number of image urls that are layers of the base image. Same center and zoom are a must.
        """
    
        baseimage = Image.open(self.base)
        trackedimage = Image.open(self.outfile)
        layeringimage = Image.open(new)
    
        basedata = baseimage.load()
        trackeddata = trackedimage.load()
        layeringdata = layeringimage.load()
        
        counter = 0
        for x in range(baseimage.size[0]):
            for y in range(baseimage.size[1]):
                bpix = basedata[x,y]
                tpix = layeringdata[x,y]
                if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                    trackeddata[x,y] = tpix
                    counter += 1

        if debug: print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
            360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
        if debug: trackedimage.show()
    
        trackedimage.save(self.outfile)
        

if __name__ == "__main__":
    import os
    os.chdir("Inputs\Static Maps")
    #mergeModeRGB("Input 1.png", "Input 2.png", "Input 3.png")
    print ""
    convertPtoRGB("Base.png", "Blue 1.png", "Blue 2.png")
    mergeModeRGB("Outfile.png", "Base.con.png", "Blue 1.con.png", "Blue 2.con.png")
    convertPtoRGB("Base.png", "Red 1.png", "Red 2.png")
    mergeModeRGB("Outfile.png", "Base.con.png", "Red 1.con.png", "Red 2.con.png")
    #blkDiff("Outfile.png", "Merged Output.png")