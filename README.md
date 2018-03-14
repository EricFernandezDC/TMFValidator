# TMFValidator

Validator for JSON-based Open-API specifications from the TM Forum [http://www.tmforum.org/open-apis]

This Python script parses a named Swagger 2.0 JSON API specification and checks that if conforms to the norms expected of a TM Forum Open-API specification.

Checks scoped for R18.0 APIs include (but not limited to):
* The info node has 'title', 'description' and 'version' attributes and are not empty
* The info.version fits the number format of 'major.minor(.patch)' with no pre/post-fix text
* The 'host' attribute is set to 'serverRoot' (warning if not)
* The 'basePath' starts with '/tmf-api/'
* If the 'basePath' has a major version in the URI, it must match the major version from 'info.version'
* Any path with a GET, offers responses of (at least) 200, 500 and 404 (for specific resources) 
* Any path with a POST, offers responses of (at least) 201 (Created) and 500
* Any path with a DELETE, offers responses of either 202 (Accepted, if async) or 204 (No Content), and 500, and NOT a 201 (Created)
* Any path with a PATCH, offers responses of 200 (Success), 202 (Accepted, if async) or 204 (No Content), 404 and 500
* Every API has a '/hub' resource? (not yet implemented)

Checks being considered for R18.5 APIs may include:
* EntityRef: The EntityRef MUST include 'id' and 'href' attributes, other attributes MAY include: name, @type, @schemaLocation, validFor, role
* Home Document: 
* Linking: 
* (more to follow)


The tool can also be useful in generating tests for each resource within the API. This can be used to generate appropriate Postman scripts.

Use the online tool http://www.convertcsv.com/json-to-csv.htm to convert the output summary files (JSON) to Excel (xls) or CSV formats.
