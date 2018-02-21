import logging
import json
import os
import urllib.request
import argparse

def parseCommandLine():
    # Parse command line 
    parser = argparse.ArgumentParser(description='TMF Validator application')
    # Required argument fileName
    parser.add_argument('fileName', metavar='fileName', nargs=1,
                    help='swagger file to be processed')
    # Additional argument for debug purposes
    parser.add_argument('-d', '--debug', dest='debug', action='store_const',
                    const=1, default=0,
                    help='triggers debug mode')
    # Additional argument for debug levels
    parser.add_argument('-l', '--log', dest='log', action='store_const',
                    const=1, default=0,
                    help='triggers debug log mode')
    # Get arguments as args, access through args.fileName and args.debug
    args = parser.parse_args()
    # args.fileName seems to be a (possible) list of names
    #print(args.fileName, args.debug)
    return args

# Set logging output file, stream, format and level
def setupLogging(debug,log):
    # Set up logger
    log = logging.getLogger("API Validator")
    if (debug == 1):
        # Turn on all debug output
        log.setLevel(logging.DEBUG)
    else:
        # Just leave the errors on (doesn't seem to be a .WARN)
        log.setLevel(logging.ERROR)
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
    if(args.log == 1):
        logFile="validator.log"
        fh = logging.FileHandler(logFile)
        fh.setLevel(logging.DEBUG)
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
        log.critical("Error loading and parsing file [" +filename+"]")
        exit()

    return obj

args = parseCommandLine()
log = setupLogging(args.debug,args.log)

# args.fileName seems to be a (possible) list of names
obj = loadSwagger(args.fileName[0])

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
