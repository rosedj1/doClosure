import numpy
import optparse

def parseOptions():
    global observalbesTags, modelTags, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    parser.add_option('-i', dest='input', type='string', help='input file name')

    global opt, args
    (opt, args) = parser.parse_args()

def GetInterval(fileName):
    mass = [line.strip() for line in open(fileName)]
    mass = [float(x) for x in mass]
#    mass.sort()
    median = numpy.percentile(numpy.array(mass),50)
    down = numpy.percentile(numpy.array(mass),16)
    up = numpy.percentile(numpy.array(mass),84)
    print down,median,up
    print str(median-down) + "/" + str(up-median)


global opt, args
parseOptions()

GetInterval(opt.input)
#GetInterval("m4l_1D_refit.txt")
#GetInterval("m4l_1Debe_reco.txt")
#GetInterval("m4l_1Debe_refit.txt")

