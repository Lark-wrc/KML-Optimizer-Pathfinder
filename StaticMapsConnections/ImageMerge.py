from PIL import Image
from Observations.Observer import Observable

debug = 0
diffnum = 50

class Merger(Observable):
    
    def __init__(self, outfile, base):
        """
        `Author`: Bill Clark

        This class is basically the same method as mergemodeRGB, now the contained mergeAll method.
        The add method is almost identical. The reason for this class is that it allows for urls to be
        added incrementally with ease. Given an instance where you want to merge urls to the same outfile
        based off the same base image, but don't have the urls all at once, this method allows for any number
        of add calls to merge images to the output. This comes with over head, saving the image to the
        outfile location after each individual merge, but certain situations really need this kind of functionality.

        `outfile`: The file address to save the output file to.

        `base`: The unmodified image which all the layers will be drawn to. The images MUST line up, which is why
            the center and zoom are REQUIRED. Those parameters being the same will line up the unchanged pixels
            correctly so that only the edited pixels pick up as different.
        """

        super(Merger, self).__init__()
        self.mcount = 0
        base = self.convertAll(base)
        self.baseimage = Image.open(base[0])
        self.basedata = self.baseimage.load()
        self.baseimage.save(outfile)
        self.outfile = outfile
        self.base = base
        self.setStatus("Initialized.")

    def merge(self, new):
        """
        `Author`: Bill Clark

        Given a new image, with layers of paths and markers, on top of a plain base image. It will then
        output the merged image to the outfile provided. This method only works with images encoded in RGB color,
        which is expected of it's inputs. The method works by opening the tracked changes file, and opening the base
        and the new image. Each pixel in the base is compared with the new image, if they're different enough the new
        pixel is placed over the original base image pixel that was contained in the tracked file. This is done for
        every pixel. Debug information contains the ratio of different to not different pixels in percent form, as well
        as a display of the output after each layer merge.

        `new`: A image with the same center and zoom as the class baseimage, which has lines or markers on it. It
                    will be merged with the tracked outfile.
        """

        trackedimage = Image.open(self.outfile)
        topimage = Image.open(new)

        trackeddata = trackedimage.load()
        topdata = topimage.load()
        
        counter = 0
        for x in range(self.baseimage.size[0]):
            for y in range(self.baseimage.size[1]):
                bpix = self.basedata[x,y]
                tpix = topdata[x,y]
                if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                    trackeddata[x,y] = tpix
                    counter += 1

        if debug: print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
            360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
        if debug: trackedimage.show()

        self.mcount += 1
        self.setStatus("{} images merged successfully.".format(self.mcount), self.mcount)
        trackedimage.save(self.outfile)

    def mergeAll(self, *images):
        """
        `Author`: Bill Clark

        This merges a list of images, with layers of paths and markers, on top of a plain base image. It will then
        output the merged image to the outfile provided. This method only works with images encoded in RGB color,
        which is expected of it's inputs. The method works by creating a new file for the changes, and opening the base
        and a layer. Each pixel in the base is compared with the layer, if they're different enough the layer pixel is
        placed over the original base image pixel that was contained in the new file. This is done for every pixel and
        every layer. Debug information contains the ratio of different to not different pixels in percent form, as well
        as a display of the output after each layer merge.

        `images`: Any number of image urls that are layers of the base image. Same center and zoom are a must.
        """

        trackedimage = Image.open(self.outfile)

        trackeddata = trackedimage.load()
        count = 0
        for top in images:
            topimage = Image.open(top)
            topdata = topimage.load()
            counter = 0


            for x in range(self.baseimage.size[0]):
                for y in range(self.baseimage.size[1]):
                    bpix = self.basedata[x,y]
                    tpix = topdata[x,y]
                    if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                        trackeddata[x,y] = tpix
                        counter += 1

            if debug: print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
                360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
            if debug: trackedimage.show()
            count += 1
            self.mcount += 1
            self.setStatus("Merging {} of {} Images".format(count, len(images)))

        print ""
        self.setStatus("{} Images Merged Successfully.".format(self.mcount), self.mcount)
        trackedimage.save(self.outfile)

    def convertAll(self, *images):
        """
        `Author`: Bill Clark

        This method takes any number of images and converts the from P color mode to RGB mode. RGB is required by the
        merge methods above. The files are saved to a different file, same prefix, but .con being placed at the end.

        `images`: The images that need to be converted. They are expected to be in P color mode, though other modes
                may convert cleanly.

        `return`: A list of the new file locations, since the file names have been changed.
        """
        ret = []
        count = 0
        for image in images:
            img = Image.open(image)
            im = img.convert("RGBA")
            ret.append(image[:-4]+'.con'+image[-4:])
            im.save(image[:-4]+'.con'+image[-4:])
            self.setStatus("Converting {} of {} Images.".format(count, len(images)), self.mcount)
            count += 1
        self.setStatus("{} Images Converted Successfully.".format(count), self.mcount)
        return ret

    def blkDiff(self, images):
        """
        `Author`: Bill Clark

        This method will change the color of any pixel that is different between the base image and another provided
        image. This works in the same way as mergeRGB, which does mean the inputs need to be RGB format. You can use
        this to visually see the detected differences between two images.

        `images`: the image to compare to base.

        `outfile`: The file to write the color marked image to.
        """

        trackedimage = Image.open(self.outfile)
        trackeddata = trackedimage.load()

        topimage = Image.open(images)
        topdata = topimage.load()
        counter = 0

        for x in range(self.baseimage.size[0]):
            for y in range(self.baseimage.size[1]):
                bpix = self.basedata[x,y]
                tpix = topdata[x,y]
                if abs(bpix[0] - tpix[0]) > diffnum or abs(bpix[1] - tpix[1]) > diffnum or abs(bpix[2] - tpix[2]) > diffnum:
                    trackeddata[x,y] = (0,0,0,255)
                    counter += 1

        if debug: print "Different Pixels:", counter, repr(round((counter/360000.)*100,2)) + '%', " Same Pixels:", \
            360000-counter, repr(round(((360000-counter)/360000.)*100,2)) + '%'
        if debug: trackedimage.show()

        if debug: print ""
        trackedimage.save(self.outfile)

if __name__ == "__main__":
    diffnum = 120
    debug = 1
    image1 = 'C:\Users\localadmin\Documents\Code Repositories\IntelliJ\SoftwareEng_Team5\Images\Example 2 Picture 1.jpg'
    image2 = 'C:\Users\localadmin\Documents\Code Repositories\IntelliJ\SoftwareEng_Team5\Images\Example 2 Picture 2.jpg'
    m = Merger('Outputs\ImF.png', image1)
    m.blkDiff(image2)
    # m.merge(image2)
