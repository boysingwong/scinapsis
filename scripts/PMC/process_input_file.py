from contextlib import closing
from lxml import etree
import codecs
import os
import shutil
import sys
import tarfile
import urllib2
import parse_xml

backupDir = 'F:\\scinapsis_PMC_backup'
# backupDir = 'D:\\GitHub\\scinapsis\\scripts\\PMC\\zip_files'

def main(argv):
    process_input_file(0)

def process_input_file(mode):       # mode: 0 - normal, 1 = rerun
    # read input file
    pmc_list_file = "input_file.txt"
    with codecs.open(pmc_list_file) as f:
        lines = f.read().splitlines()

        lineNb = 0
        for line in lines:
            lineNb = lineNb + 1
            print line

            # TODO: sample check for first 50 runs
            # if lineNb > 50:
            #     break

            # step 1: get pmc_id from file
            pmc_id = line

            # step 2: open url and retrieve related information
            url = "http://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC" + pmc_id

            response = urllib2.urlopen(url)
            html = response.read()
            root = etree.fromstring(html)

            isOpenAccess = False
            tarAddress = ""
            pdfAddress = ""
            tarElement = root.xpath("//record/link[@format='tgz']/@href")
            pdfElement = root.xpath("//record/link[@format='pdf']/@href")
            if len(tarElement) > 0:
                tarAddress = tarElement[0]
            else:
                isOpenAccess = True
            if len(pdfElement) > 0:
                pdfAddress = pdfElement[0]

            if isOpenAccess:        # not continue process on this file
                errElement = root.xpath("//error")
                if len(errElement) > 0:
                    errMsg = errElement[0].text + "\n"
                    with open("readfile_ error.log", 'a') as w:
                        w.write(errMsg)
                    continue

            # step3: ftp get file from ncbi
            print tarAddress
            print pdfAddress
            dldFilename = pmc_id +'.tar.gz'

            if mode == 0:
                with closing(urllib2.urlopen(tarAddress)) as r:
                    with open(dldFilename, 'wb') as f:
                        shutil.copyfileobj(r, f)
                        f.close()
            elif mode == 1:
                srcFile = backupDir + "\\" + dldFilename
                destDir = os.getcwd()
                if os.path.isfile(srcFile):
                    shutil.move(srcFile, destDir)
                else:
                    continue

            # step4 extract file to specific file path and ready to process
            # if os.path.exists('temp'):
            #     os.mkdir('temp')
            removeDirContent('temp')        # remove temp content
            tar = tarfile.open(dldFilename)
            tar.extractall('temp')
            tar.close()

            xmlFilename = ""
            for root, dirs, files in os.walk("temp"):
                for file in files:
                    if file.endswith(".nxml"):
                        xmlFilename = os.path.join(root, file)

            # step 4: process_xml with inputs: pmc_id, xmlFilename, pdfFilename
            parse_xml.process_xml(pmc_id, xmlFilename, pdfAddress)

            # step 5: remove directory and temp directory
            removeDirContent('temp')        # remove temp content

            shutil.copy(dldFilename, backupDir)
            os.remove(dldFilename)

def removeDirContent(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception, e:
            print e

if __name__ == "__main__":
    main(sys.argv[1:])