# TMFValidator

Validator for JSON-based Open-API specifications from the TM Forum [http://www.tmforum.org/open-apis]

This Python script parses a named Swagger 2.0 JSON API specification and checks that if conforms to the norms expected of a TM Forum Open-API specification.

Checks scoped for R18.0 APIs include (but not limited to):
* The info node has 'title', 'description' and 'version' attributes and are not empty
* The info.version fits the number format of 'major.minor(.patch)' with no pre/post-fix text
* The 'host' attribute is set to 'serverRoot' (warning if not)
* The 'basePath' starts with '/tmf-api/'
* If the 'basePath' has a major version in the URI, it must match the major version from 'info.version'
* Every API has a '/hub' resource
* With respect to HTTP response codes:

|        | MUST                                         | SHOULD              | MUST NOT | Design Guide 3.0 Ref     |
|--------|----------------------------------------------|---------------------|----------|--------------------------|
| GET    |  (200 or 206 {partial}), 400, 404, 405, 500  |       401, 403      |          | Part 1: Pages 26, 28, 39 |
| POST   |     (201 or 202), 400, 404, 405, 409, 500    |       401, 403      |          | Part 1: Page 56          |
| PATCH  | (200 or 202 or 204), 400, 404, 405, 409, 500 |       401, 403      |          | Part 1: Pages 50, 60     |
| PUT    | (200 or 204), 400, 404, 405, 409, 500        |       401, 403      |          | Part 1: Page 46          |
| DELETE | (200 or 202 or 204)                          | (202 or 204 or 200) |    201   | Part 1: Page 69          |

Checks being considered for R18.5 APIs may include:
* Consistent Error body representation of user and application specific error codes (when used), as per GD-3.0 Part-1, Page-20
* EntityRef: The EntityRef MUST include 'id' and 'href' attributes, other attributes MAY include: name, @type, @schemaLocation, validFor, role
* Home Document: 
* Linking: 
* (more to follow)


The tool can also be useful in generating tests for each resource within the API. This can be used to generate appropriate Postman scripts.

Use the online tool http://www.convertcsv.com/json-to-csv.htm to convert the output summary files (JSON) to Excel (xls) or CSV formats.
