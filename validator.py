import logging
import json
import os
import urllib.request
import argparse
import time
import collections
import re               # Regular Expression


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
        log.info("******************************************************\nAPI Specification is " + filename)
        if (os.path.exists(filename)):
            if (os.access(filename, os.R_OK)):
                log.debug("File [" + filename + "] exists and is readable")
            else:
                log.critical("File [" + filename + "] is not readable")
                exit()
        else:
            log.critical("File [" + filename + "] does not exist")
            exit()

        try:
            with open(filename, 'r') as fp:
                obj = json.load(fp)
        except ValueError as e:
            log.critical("Error loading and parsing file [" + filename+ "]")
            log.critical(e)
            obj = 0

    return obj

def checkResponseCodes(path, method, responses, must = {}, should = {}, mustNot = {}):
    log.info("Method [" +method+ "] on path [" +path+ "] must have codes [" +str(must)+ "], should have codes [" +str(should)+ "] and must not have codes [" +str(mustNot)+ "]")
    log.info("Responses [" +str(responses)+ "]")

    summary = "PASS"
    # Check for the MUST HAVE response codes
    for mustCode in must:
        if (str(mustCode) not in responses):
            log.error("The [" +method+ "] on [" +path+ "] MUST HAVE a response of [" +str(mustCode)+ "]")
            summary = "FAIL: "+method+ " missing " +str(mustCode)
        else:
            log.info("The [" +method+ "] on [" +path+ "] correctly included a MUST HAVE response of [" +str(mustCode)+ "]")

    # Check for the SHOULD HAVE response codes
    for shouldCode in should:
        if (str(shouldCode) not in responses):
            log.warn("The [" +method+ "] on [" +path+ "] SHOULD HAVE a response of [" +str(shouldCode)+ "]")
            summary = "WARN: "+method+ " missing " +str(shouldCode)
        else:
            log.info("The [" +method+ "] on [" +path+ "] correctly included a SHOULD HAVE response of [" +str(shouldCode)+ "]")

    # Check for the MUST NOT HAVE response codes
    for badCode in mustNot:
        if (str(badCode) in responses):
            log.error("The [" +method+ "] on [" +path+ "] MUST NOT have a response of [" +str(badCode)+ "]")
            summary = "FAIL: "+method+ " had " +str(shouldCode)
        else:

            log.info("The [" +method+ "] on [" +path+ "] correctly did NOT have a response of [" +str(badCode)+ "]")

    return summary

args = parseCommandLine()
log = setupLogging(args.debug, args.log)
# args.fileName is a (possible) list of names

obj_list = []
for fileName in args.fileName:
    summary = collections.OrderedDict()
    obj = loadSwagger(fileName)
    if obj==0:
        summary["File Name"] = fileName
        summary["ERROR"] = "File cannot be parsed, is it a valid JSON file?"
        obj_list.append(summary)
    else:
        summary = {"File Name": fileName}
        log.debug("Using Swagger file format " + obj["swagger"])
        info = obj["info"]
        log.debug("Found info node " + json.dumps(info))

        if (info["title"] and len(info["title"]) > 0):
            log.info("Found info.title: " + info["title"])
            summary["Title"] = "PASS"
        else:
            log.error("General: info node has no title")
            summary["Title"] = "FAIL: No Title"

        if (info["description"] and len(info["description"]) > 0):
            log.info("Found info.description: " + info["description"])
            summary["Description"] = "PASS"
        else:
            log.error("General: info node has no description")
            summary["Description"] = "FAIL: No Description"

        basePath = ""
        if (obj["basePath"]):
            basePath = obj["basePath"]
            if (basePath.startswith("/tmf-api/")):
                log.info("basePath correctly starts with [/tmf-api/]")
                summary["BasePath"] = "PASS"
                # Perhaps validate that the resource name comes next?
            else:
                log.error("General: basePath [" + basePath + "] does not start with [/tmf-api/]")
                summary["BasePath"] = "FAIL: No /tmf-api/"

        if (info["version"]):
            versionValue = info["version"]
            # Look for 'major.minor(.patch)' with no pre/post-fix text 
            versionFormat = re.search("^(\d+).\d+(.\d+)*$", versionValue)
            if (versionFormat == None):
                log.error("General: info.version [" +versionValue+ "] does not match the format \'major.minor(.patch)\'")
                summary["API Version"] = "FAIL: Bad Format"
            else:
                log.info("info.version [" +versionValue+ "] matches the format \'major.minor(.patch)\'")
                # This should be the major version of the API, taken from the info.version string
                apiMajorVersion = versionFormat.group(1)
                # What is the API major version, taken from the basePath attribute
                basePathVersion = re.search(".*/v(\d)(/)?", basePath, re.IGNORECASE)
                if (basePathVersion):
                    basePathMajorVersion = basePathVersion.group(1)
                    log.info("basePath: Taking major API version number from the basePath [" +basePath+ "] as [" +basePathMajorVersion+ "]")
                else:
                    log.info("basePath: Cannot extract a major API version number from the basePath [" +basePath+ "] - assume \'v1\'")
                    basePathMajorVersion = "1"

                log.info("basePath [" +basePath+ "] major version is [" +basePathMajorVersion+ "]. info.version says it is [" +apiMajorVersion+ "]")
                if (basePathMajorVersion == apiMajorVersion):
                    log.info("Major versions from the basePath [" +basePathMajorVersion+ "] and info.version [" +apiMajorVersion+ "] are the same!")
                    summary["API Version"] = "PASS"
                else:
                    log.error("Major versions from the basePath [" +basePathMajorVersion+ "] and info.version [" +apiMajorVersion+ "] are not the same!")
                    summary["API Version"] = "FAIL: [" +basePathMajorVersion+ "-vs-" +apiMajorVersion+ "]"
        else:
            log.info("info node has no version")
            summary["API Version"] = "WARN: No Version"

        # Many have  { "host": "biologeek.orange-labs.fr" }
        if (obj["host"]):
            hostname = obj["host"]
            if (hostname != "serverRoot"):
                log.error("host [" +hostname+ "] SHOULD be set to \'serverRoot\'")
                summary["host"] = "WARN: [" +hostname+ "] not \'serverRoot\'"
            else:
                log.info("Found host [" + hostname + "] correctly set to \'serverRoot\'")
                summary["host"] = "PASS"

        # DG-P1-Pg18: “REST APIs MUST support the “application/json” media type by default.”
        if ("consumes" in obj and "produces" in obj):
            log.info("Found [consumes [" +str(obj["consumes"])+ "]] and [produces [" +str(obj["produces"])+ "]] attributes")
            if (str(obj["consumes"]).index("application/json") and
                str(obj["produces"]).index("application/json")):
                log.info("DG3-1-18: Found [consumes] and [produces] attributes supporting 'application/json'")
                summary["DG3-1-18: JSON"] = "PASS"
            else:
                log.error("DG3-1-18: [consumes] and [produces] attributes do not mention 'application/json'")
                summary["DG3-1-18: JSON"] = "FAIL: No JSON support"
        else:
            log.error("DG3-1-18: The [consumes] and/or [produces] attributes (to support 'application/json') are missing")
            summary["DG3-1-18: JSON"] = "FAIL: Missing attributes"

        paths = obj["paths"]
        # Every API should have a '/hub' resource for event management
        if ("/hub" in paths):
            summary["Event Hub"] = "PASS"
        else:
            log.error("No '/hub' resource listed")
            summary["Event Hub"] = "FAIL: No hub resource"

        for path in paths:
            method = paths[path]
            for operation in method.keys():
                uri = "http://" + hostname + basePath + path
                operationDetails = method[operation]
                if "parameters" in operationDetails:
                    params = operationDetails["parameters"]
                else:
                    log.info("Operation [" +operation+ "] on uri [" +uri+ "] has no parameters defined")
                    params = {}

                if "responses" in operationDetails:
                    # log.info("Responses found for operation [" +operation+ "] on [" +path+ "]")
                    # Assume an initial PASS, to be over-written later by any FAIL
                    if ("DG3-1-Pg26: GET Responses" not in summary):
                        summary["DG3-1-Pg26: GET Responses"] = "PASS"

                    if (operation == "get"):
                        # Testing listed response codes for HTTP-GET (note some are tested separately)
                        summary["GET Responses"] = checkResponseCodes(path, operation, operationDetails["responses"], { 400, 405, 500 }, { 401, 403 }, { 201, 202 })

                        # DG3-1-Pg26: “If there are no matching resource then a 404 Not Found must be returned.”
                        # If the path ends with a specific resource identifier (like ".../party/{roleId}") then do a 404 response check
                        specificResource = re.compile(".*{.*}$")
                        if (specificResource.match(path)):
                            if ("404" in operationDetails["responses"]):
                                log.info("A 404 response code was correctly listed for the [" +operation+ "] of [" +path+ "]")
                            else:
                                log.error("A 404 response code was not listed for the [" +operation+ "] of [" +path+ "]")
                                summary["GET Responses"] = "FAIL: Missing 404"
                        else:
                            log.info("Skipping 404 response check [" +operation+ "] on [" +path+ "] - Assumed to be a collection")

                         # Any get must offer (at least) 200 (Ok) or 206 (Partial response)
                        if ("200" in operationDetails["responses"] or "206" in operationDetails["responses"]):
                            log.info("A 200 (Ok) or 206 (Partial) response code was correctly listed for the [" +operation+ "] of [" +path+ "]")
                        else:
                            log.error("Neither a 200 (Ok) or 206 (Partial) response code was listed for the [" +operation+ "] of [" +path+ "]")
                            summary["GET Responses"] = "FAIL: Missing 200/206 response"

                    if (operation == "post"):
                        summary["POST Responses"] = checkResponseCodes(path, operation, operationDetails["responses"], { 400, 404, 405, 409, 500 }, { 401, 403 }, { })

                         # Any post must offer (at least) 201 (Created) or 202 (Accepted: async)
                        if ("201" in operationDetails["responses"] or "202" in operationDetails["responses"]):
                            log.info("A 201 (Created) or 202 (Accepted) response code was correctly listed for the [" +operation+ "] of [" +path+ "]")
                        else:
                            log.error("Neither a 201 (Created) or 202 (Accepted) response code was listed for the [" +operation+ "] of [" +path+ "]")
                            summary["POST Responses"] = "FAIL: Missing 201/202 response"

                    if (operation == "patch"):
                        summary["PATCH Responses"] = checkResponseCodes(path, operation, operationDetails["responses"], { 400, 404, 405, 409, 500 }, { 401, 403 }, {})
                         # Any patch must offer (at least) 200 (Ok), 202 (Accepted, if async) or 204 (No Content)
                        if ("200" in operationDetails["responses"] or "202" in operationDetails["responses"] or "204" in operationDetails["responses"]):
                            log.info("A 200 (Ok), 202 (Accepted) or 204 (No Content) response code was correctly listed for the [" +operation+ "] of [" +path+ "]")
                        else:
                            log.error("Neither a 200 (Ok), 202 (Accepted) or 204 (No Content) response code was listed for the [" +operation+ "] of [" +path+ "]")
                            summary["PATCH Responses"] = "FAIL: Missing 200/202/204 response"

                    if (operation == "put"):
                        summary["PUT Responses"] = checkResponseCodes(path, operation, operationDetails["responses"], { 400, 404, 405, 409, 500 }, { 401, 403 }, {})

                         # DG-3.0 Section-1 Page-46: Any put must offer (at least) 200 (Ok), 202 (Accepted, if async) or 204 (No Content)
                        if ("200" in operationDetails["responses"] or "202" in operationDetails["responses"] or "204" in operationDetails["responses"]):
                            log.info("A 200 (Ok), 202 (Accepted) or 204 (No Content) response code was correctly listed for the [" +operation+ "] of [" +path+ "]")
                        else:
                            log.error("Neither a 200 (Ok), 202 (Accepted) or 204 (No Content) response code was listed for the [" +operation+ "] of [" +path+ "]")
                            summary["PUT Responses"] = "FAIL: Missing 200/202/204 response"

                    if (operation == "delete"):
                        summary["DELETE Responses"] = checkResponseCodes(path, operation, operationDetails["responses"], { 400, 404, 405, 500 }, { 401, 403 }, { 201 })
                         # Any delete must offer (at least) 200 (Ok), 202 (Accepted, if async) or 204 (No Content)
                        if ("200" in operationDetails["responses"] or "202" in operationDetails["responses"] or "204" in operationDetails["responses"]):
                            log.info("A 200 (Ok), 202 (Accepted) or 204 (No Content) response code was correctly listed for the [" +operation+ "] of [" +path+ "]")
                        else:
                            log.error("Neither a 200 (Ok), 202 (Accepted) or 204 (No Content) response code was listed for the [" +operation+ "] of [" +path+ "]")
                            summary["DELETE Responses"] = "FAIL: Missing 200/202/204 response"
                else:
                    log.error("DG3-1-Pg26: No responses attribute found for operation [" +operation+ "] for path [" +path+ "]")
                    summary["DG3-1-Pg26: Responses"] = "FAIL: Missing responses"

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