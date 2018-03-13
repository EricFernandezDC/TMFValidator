# TMFValidator

Validator for JSON-based Open-API specifications from the TM Forum [http://www.tmforum.org/open-apis]

This Python script parses a named Swagger 2.0 JSON API specification and checks that if conforms to the norms expected of a TM Forum Open-API specification.

Checks include (but not limited to):
* The info node has a "title", "description" and "version" attributes and are not empty
* The info.version fits the number format of 'major.minor(.patch)' with no pre/post-fix text
* The major version from 'info.version' must match the major version taken from the filename 
* That the "basePath" starts with "/tmf-api/"
* That any path with a GET, offers responses of (at least) 200, 500 and 404 (for specific resources) 
* That any path with a POST, offers responses of (at least) 201 and 500
* That any path with a DELETE, offers responses of either 202 (Accepted) or 204 (No Cotent), and 500
* (more to follow)

The tool can also be useful in generating tests for each resource within the API. This can be used to generate appropriate Postman scripts.

Use the online tool http://www.convertcsv.com/json-to-csv.htm to convert the output summary files (JSON) to Excel (xls) or CSV formats.
