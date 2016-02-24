from PIL import Image


def mergeModeRGB(base, *images):
    diffnum = 50

    baseimage = Image.open(base)
    baseimage.save("Outfile.png")
    newimage = Image.open("Outfile.png")

    basedata = baseimage.load()

    newdata = newimage.load()

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
                    newdata[x,y] = tpix
                    counter += 1

        print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
            360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
        newimage.show()

    print ""
    newimage.save("Outfile.png")


def blkDiff(base, images):
    baseimage = Image.open(base)
    baseimage.save("Outfile.png")
    newimage = Image.open("Outfile.png")

    basedata = baseimage.load()

    newdata = newimage.load()

    topimage = Image.open(images)
    topdata = topimage.load()
    counter = 0
    diffnum = 50

    for x in range(baseimage.size[0]):
        for y in range(baseimage.size[1]):
            bpix = basedata[x,y]
            tpix = topdata[x,y]
            if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                newdata[x,y] = (0,0,0,255)
                counter += 1

    print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
        360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
    newimage.show()

def convertPtoRGB(*images):
    for image in images:
        img = Image.open(image)
        im = img.convert("RGBA")
        #im.show()
        im.save(image[:-4]+".con.png")

if __name__ == "__main__":
    import os
    os.chdir("C:\Users\Research\Documents\Maps Static Downloads")
    #mergeModeRGB("Input 1.png", "Input 2.png", "Input 3.png")
    print ""
    convertPtoRGB("Base.png", "Blue 1.png", "Blue 2.png")
    mergeModeRGB("Base.con.png", "Blue 1.con.png", "Blue 2.con.png")
    convertPtoRGB("Base.png", "Red 1.png", "Red 2.png")
    mergeModeRGB("Base.con.png", "Red 1.con.png", "Red 2.con.png")
    #blkDiff("Outfile.png", "Merged Output.png")