# Creates a html report displaying images and confidence score graphs
# Copyright (C) 2019  Edward Poindexter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This file takes the inference output and generates a html page that displays the image and a bar graph of the
top 5 categories and percent confidence.

:Input
 dictionary of image name and top five inference category results

Output:
  resultsReport, generated html page with image and results bar graph
"""
import matplotlib.pyplot as plt
import shutil
import os
import datetime


def createBarGrapgh(resultsDir, imageTitle, categoriesYaxis, scoresXaxis):
    """
    This function takes the category names and confidence levels and plots them in a bargraph. The
    graph is saved as an image file
    :param
    resultsPath: the path and name of the results folder
    imageTitle: Path and Name of image file
    categoriesYaxis: list of top 5 classification categories
    scoresXaxis: list of top 5 confidence scores
    :return:
    saves a bar graph of categories versus scores to resultsDir/resultsGraph/[imageName]_resultsPlot.png
    """
    #TODO fix font sizes on grapgh
    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(categoriesYaxis, scoresXaxis)
    #ax.set_yticks(y_pos)
    ax.set_yticklabels(categoriesYaxis, fontsize=24)
    ax.set_xlabel('Confidence Score', fontsize=20)
    plt.axis([0,1,-1,len(categoriesYaxis)])
    ax.invert_yaxis()
    #TODO add restriction on image path size
    ax.set_title(imageTitle)
    #plt.show()
    #create image from plot
    plotName = resultsDir + "/resultsGraph/"+ imageTitle[imageTitle.rfind('/')+1:imageTitle.rfind('.')] + "_resultPlot.png"
    plt.savefig(plotName, bbox_inches='tight')
    plt.close()

def generateReport(resultsDir, resultsDict):
    """
    This function creates a html report using the image and bargraph
    :param
    resultsDir: the path and name of the results folder
    resultsDict: {'imageName.jpg':['imagePath',processTime,categoryN,confidenceN..categoryN-1, confidenceN-1]}
    :return:
    creates a HTML file with the image and confidence score bar graph in the resultsDir folder
    """
    #copy and rename template
    dstFile = resultsDir + "/results.html"
    curLoc = os.getcwd()
    templatePath = curLoc.replace('\\', '/') + '/resultsTemplate.html'
    shutil.copyfile(templatePath, dstFile)

    #open template an goto first writeable line after <body>
    f = open(dstFile, 'r+')

    # insertPoint = f.readline()
    # while insertPoint != "<body>\n":
    #  insertPoint = f.readline()
    # #f.readline()
    for lines in range(25):
        insertPoint = f.readline()
        if insertPoint == "<body>\n":
            break

    #add project notes to file
    f.write('\n')
    f.write('<p> Inference Results from {}</p>\n'.format(resultsDir))
    # insert images into file
    for k, v in resultsDict.items():
        imageLocation = v[0]
        resultImageName = imageLocation[imageLocation.rfind('/')+1:imageLocation.rfind('.')]
        imageBarGraph = "./resultsGraph/{}_resultPlot.png".format(resultImageName)
        PathFixA = os.path.relpath(imageLocation, resultsDir)
        PathFix = PathFixA.replace('\\', '/')

        f.write('<div class ="imageSet">\n')
        f.write('   <img class ="a" src="{}">\n'.format(PathFix))
        f.write('   <img class ="a" src="{}">\n'.format(imageBarGraph))
        f.write('</div>\n')

    #TODO index into results file correctly instead of appending writes at end of file
    f.write('<p> generated using results report template version 0.1 on {}</p>\n'.format(datetime.datetime.now()))
    f.write('</body>\n')
    f.write('</html>\n')

    #close file
    f.close()
    print('Result Report create at {}'.format(resultsDir))


# import from dictionary
def importDict(resultsDict, resultsDir):
    """
    This function imports the image and inference results from a dictionary of results
    :param
    resultsDict: {'imageName.jpg':['imagePath',processTime,categoryN,confidenceN..categoryN-1, confidenceN-1]}
    resultsDir: the path and name of the results folder
    :return
    a HTML file with the image and confidence score bar graph in the resultsDir folder
    """
    #make results directories if they are not present
    #os.mkdir(resultsDir)
    if not os.path.exists(resultsDir+'/resultsGraph'):
        os.makedirs(resultsDir+'/resultsGraph')

    # step through the dictionary
    for k, v in resultsDict.items():
        # create the bargraph
        yAxis = []
        xAxis = []
        if len(v) >= 12:
            yAxis = v[2:12:2]
            xAxis = v[3:12:2]
        else:
            yAxis = v[2:len(v):2]
            xAxis = v[3:len(v):2]

        createBarGrapgh(resultsDir, v[0], yAxis, xAxis)
    generateReport(resultsDir, resultsDict)


def importDatabase(dbPathAndName): #TODO complete function for database
    """
    This function imports the image and inference results from a database
    :param dbPathAndName: path and name of the database
    :return:
    """
    # pull the image and inference results from the database

    # create the bargraph

    # update the database with the bargrapgh location