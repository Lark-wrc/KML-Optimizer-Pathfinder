from PIL import Image


def merge(base, *images):
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
                if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                    newdata[x,y] = tpix
                    counter += 1

        print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
            360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
        #newimage.show()

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

if __name__ == "__main__":
    import os
    os.chdir("C:\Users\Research\Documents")
    merge("Input 1.png", "Input 2.png", "Input 3.png")
    blkDiff("Outfile.png", "Merged Output.png")