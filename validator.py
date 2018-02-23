import logging
import json
import os
import urllib.request
import argparse
import time
import collections


def parseCommandLine():
    # Parse command line
    parser = argparse.ArgumentParser(description='TMF Validator application')
    # Required argument fileName
    parser.add_argument('fileName', metavar='fileName', nargs='+',
                        help='swagger file to be processed')
    # Additional argument for debug purposes
    parser.add_argument('-d', '--debug', dest='debug', action='store_const',
                        const=1, default=0,
                        help='triggers debug mode')
    # Additional argument for debug logs
    parser.add_argument('-l', '--log', dest='log', action='store_const',
                        const=1, default=0,
                        help='triggers debug log mode')
    # Additional argument for ctk output
    parser.add_argument('-c', '--ctk', dest='ctk', action='store_const',
                        const=1, default=0,
                        help='triggers ctk')
    # Additional argument for summary log
    parser.add_argument('-s', '--summary', dest='sumlog', action='store_const',
                        const=1, default=0,
                        help='outputs summary log')
    # Get arguments as args, access through args.fileName and args.debug
    args = parser.parse_args()
    # args.fileName seems to be a (possible) list of names
    #print(args.fileName, args.debug)
    return args

# Set logging output file, stream, format and level


def setupLogging(debug, log):
    # Set up logger
    log = logging.getLogger("API Validator")
    if (debug == 1):
        # Turn on all debug output
        log.setLevel(logging.DEBUG)
    else:
        # Just leave the errors on (doesn't seem to be a .WARN)
        log.setLevel(logging.INFO)
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
        logFile = 'logs/validator' + \
            str(time.strftime("%d-%m-%Y_%H-%M-%S"))+'.log'
        fh = logging.FileHandler(logFile)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    return log


def loadSwagger(filename):
    obj = {}
    # From a URL
    if "http" in filename:
        req = urllib.request.urlopen(filename)
        obj = json.loads(req.read().decode())
    else:
        # From a file
        log.info("API Specification is " + filename)
        if (os.path.exists(filename)):
            #log.debug("File [" +filename+ "] exists")
            if (os.access(filename, os.R_OK)):
                log.debug("File [" + filename + "] exists and is readable")
            else:
                log.critical("File [" + filename + "] is not readable")
                exit()
        else:
            log.critcal("File [" + filename + "] does not exist")
            exit()

        try:
            with open(filename, 'r') as fp:
                obj = json.load(fp)
        except ValueError:
            log.critical("Error loading and parsing file [" + filename+"]")
            exit()

    return obj


args = parseCommandLine()
log = setupLogging(args.debug, args.log)
# args.fileName seems to be a (possible) list of names

obj_list = []
for x in args.fileName:
    summary = collections.OrderedDict()
    obj = loadSwagger(x)
    summary = {"File Name": x}
    log.debug("Using Swagger file format " + obj["swagger"])
    info = obj["info"]
    log.debug("Found info node " + json.dumps(info))

    if (info["title"]):
        log.info("Found info.title: " + info["title"])
        summary["Title"] = "PASS"
    else:
        log.error("info node has no title")
        summary["Title"] = "WARN"
    if (info["description"]):
        log.info("Found info.description: " + info["description"])
        summary["Description"] = "PASS"
    else:
        log.error("info node has no description")
        summary["Description"] = "WARN"

    if (info["version"]):
        if (info["version"] == "2.0"):
            log.warn(
                "info.version is 2.0 - is this the Swagger file format version or the API specification version?")
            summary["API Version"] = "WARN"
        else:
            log.info("Found info.version: " + info["version"])
            summary["API Version"] = "PASS"
    else:
        log.info("info node has no version")
        summary["API Version"] = "WARN"

    # "host": "biologeek.orange-labs.fr",
    if (obj["host"]):
        hostname = obj["host"]
        log.info("Found host [" + hostname + "] What should this be set to?")

    # "basePath": "/tmf-api/resourceInventoryManagement",
    if (obj["basePath"]):
        basePath = obj["basePath"]
        if (basePath.startswith("/tmf-api/")):
            log.info("basePath correctly starts with [/tmf-api/]")
            summary["BasePath"] = "PASS"
            # Perhaps validate that the resource name comes next?
        else:
            log.error("basePath [" + basePath +
                      "] does not start with [/tmf-api]")
            summary["BasePath"] = "FAIL"

        if (basePath.find("/v2") != -1):
            log.error("basePath [" + basePath +
                      "] contains an explicit version number")
    paths = obj["paths"]
    for path in paths:
        method = paths[path]
        for operation in method.keys():
            log.info("Can use a [" + operation + "] on path [" + path + "]")
            uri = "http://" + hostname + basePath + path
            operationDetails = method[operation]
            params = operationDetails["parameters"]
            if args.ctk == 1:
                for param in params:
                    if "required" in param:
                        if (param["required"] == True):
                            if "type" in param:
                                primaryKey = uri.replace(
                                    "{id}", "{id: " + param["type"] + "}")
                                log.info(
                                    "\n  # Mandatory test: " + param["description"] + "\n  curl -" + operation + " " + primaryKey)
                        else:
                            # Optional param - test if it is a query param
                            if "in" in param:
                                if (param["in"] == "query"):
                                    if "description" in param:
                                        log.info("\n  # Optional test: " + param["description"] + "\n  curl -" +
                                                 operation + " " + uri + "?" + param["name"] + "=" + param["type"])
    summary["Time"] = time.strftime("%H:%M:%S")
    summary["Date"] = time.strftime("%d/%m/%Y")
    obj_list.append(summary)

if args.sumlog == 1:
    with open('logs/summary'+str(time.strftime("%d-%m-%Y_%H-%M-%S"))+'.json', "w+") as f:
        json.dump(obj_list, f)
        #f.write("\n")
    f.closed
