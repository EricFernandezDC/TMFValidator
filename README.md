# TMFValidator

Validator for JSON-based Open-API specifications from the TM Forum [http://www.tmforum.org/open-apis]

This Python script parses a named Swagger 2.0 JSON API specification and checks that if conforms to the norms expected of a TM Forum Open-API specification.

Checks include (but not limited to):
* The info node has a "title", "description" and "version" attributes
* That the "basePath" starts with "/tmf-api/"
* That the "basePath" does NOT contain an explicit version number
* (more to follow)

The tool can also be useful in generating tests for each resource within the API. This can be used to generate appropriate Postman scripts.

Use the online tool http://www.convertcsv.com/json-to-csv.htm to convert the output summary files (JSON) to Excel (xls) or CSV formats.