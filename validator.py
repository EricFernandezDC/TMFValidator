import logging
import json
import os
import urllib.request
import argparse

# Parse command line 
parser = argparse.ArgumentParser(description='TMF Validator application')
# Required argument fileName
parser.add_argument('fileName', metavar='fileName', nargs=1,
                    help='swagger file to be processed')
# Additional argument for debug purposes
parser.add_argument('-d', '--debug', dest='debug', action='store_const',
                    const=1, default=0,
                    help='triggers debug log mode')
# Additional argument for debug levels
parser.add_argument('-e', '--error', dest='error', action='store_const',
                    const=1, default=0,
                    help='triggers error debug log mode')
# Get arguments as args, access through args.fileName and args.debug
args = parser.parse_args()
#print(args.fileName, args.debug)
fileName = ''.join(args.fileName)
logFile = "validator.log"

# Set logging output file, stream, format and level
def setupLogging(logFile):
    # Set up logger
    log = logging.getLogger("API Validator")
    log.setLevel(logging.DEBUG)
    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    #ch.setLevel(logging.ERROR)
    ch.setLevel(logging.INFO)
    #formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')
    formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(ch)

    # Create file handler which logs even debug messages
    if(args.debug == 1):
        fh = logging.FileHandler(logFile)
        fh.setLevel(logging.DEBUG)
        if(args.error == 1):
            fh.setLevel(logging.ERROR)
        fh.setFormatter(formatter)
        log.addHandler(fh)
    
    return log


def loadSwagger(filename):
    obj = {}
    # From a URL
    # url = urllib.request.urlopen('http://site.com/sample.json')
    # obj = json.load(url)

    # From a file
    log.info("API Specification is " +filename)
    if (os.path.exists(filename)):
        #log.debug("File [" +filename+ "] exists")
        if (os.access(filename, os.R_OK)):
            log.debug("File [" +filename+ "] exists and is readable")
        else:
            log.critical("File [" +filename+ "] is not readable")
            exit()
    else:
        log.critcal("File [" +filename+ "] does not exist")
        exit()

    try:
        with open(filename, 'r') as fp:
            obj = json.load(fp)
    except ValueError:
        log.critical("Error loading and parsing file")
        exit()

    return obj


log = setupLogging(logFile)
obj = loadSwagger(fileName)
#obj = loadSwagger("tmf_api_servicecatalog_swagger_v1_2.json")
#obj = loadSwagger("Resource_Inventory_Management.regular.swagger.json")

log.debug("Using Swagger file format " +obj["swagger"])
info = obj["info"]
log.debug("Found info node " +json.dumps(info))

if (info["title"]):
    log.info("Found info.title: " +info["title"])
else:
    log.error("info node has no title")

if (info["description"]):
    log.info("Found info.description: " +info["description"])
else:
    log.error("info node has no description")

if (info["version"]):
    if (info["version"] == "2.0"):
        log.warn("info.version is 2.0 - is this the Swagger file format version or the API specification version?")
    else:
        log.info("Found info.version: " +info["version"])
else:
    log.info("info node has no version")

# "host": "biologeek.orange-labs.fr",
if (obj["host"]):
    hostname = obj["host"]
    log.info("Found host [" +hostname+ "] What should this be set to?")

# "basePath": "/tmf-api/resourceInventoryManagement",
if (obj["basePath"]):
    basePath = obj["basePath"]
    if (basePath.startswith("/tmf-api/")):
        log.info("basePath correctly starts with [/tmf-api/]")
        # Perhaps validate that the resource name comes next?
    else:
        log.error("basePath [" +basePath+ "] does not start with [/tmf-api]")

    if (basePath.find("/v2") != -1):
        log.error("basePath [" +basePath+ "] contains an explicit version number")

paths = obj["paths"]
for path in paths:
    method = paths[path]
    for operation in method.keys():
        log.info("Can use a [" +operation+ "] on path [" +path+ "]")
        uri = "http://" +hostname +basePath +path
        operationDetails = method[operation]
        params = operationDetails["parameters"]

        for param in params:
            if "required" in param:
                if (param["required"] == True):
                    if "type" in param:
                        primaryKey = uri.replace("{id}", "{id: " +param["type"]+ "}")
                        log.info("\n  # Mandatory test: " +param["description"]+ "\n  curl -" +operation+ " " +primaryKey)
                else:
                    # Optional param - test if it is a query param
                    if "in" in param:
                        if (param["in"] == "query"):
                            if "description" in param:
                                log.info("\n  # Optional test: " +param["description"]+ "\n  curl -" +operation+ " " +uri+ "?" +param["name"]+ "=" +param["type"])
