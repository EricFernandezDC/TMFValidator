# TMFValidator

Validator for JSON-based Open-API specifications from the TM Forum [http://www.tmforum.org/open-apis]

This Python script parses a named Swagger 2.0 JSON API specification and checks that it conforms to the norms expected of a TM Forum Open-API specification.

Checks scoped for R18.0 APIs include (but not limited to):
* The info node has 'title', 'description' and 'version' attributes and are not empty
* The info.version fits the number format of 'major.minor(.patch)' with no pre/post-fix text
* The 'host' attribute is set to 'serverRoot'
* The 'basePath' starts with '/tmf-api/'
* If the 'basePath' has a major version in the URI, it must match the major version from 'info.version'
* Every API has a '/hub' resource
* With respect to HTTP response codes:

|        | MUST                                         | SHOULD   | MUST NOT | Design Guide 3.0 Ref     |
|--------|----------------------------------------------|----------|----------|--------------------------|
| GET    | (200 or 206 {partial}), 400, 404, 405, 500   | 401, 403 |          | Part 1: Pages 26, 28, 39 |
| POST   | (201 or 202), 400, 404, 405, 409, 500        | 401, 403 |          | Part 1: Page 56          |
| PATCH  | (200 or 202 or 204), 400, 404, 405, 409, 500 | 401, 403 |          | Part 1: Pages 50, 60     |
| PUT    | (200 or 202 or 204), 400, 404, 405, 409, 500 | 401, 403 |          | Part 1: Page 46          |
| DELETE | (200 or 202 or 204), 400, 404, 405, 500      | 401, 403 |    201   | Part 1: Page 69          |

Checks being considered for R18.5 APIs may include:
* A successful GET (response-code 200) for a specific resource {id} must return a single instance (not an array)
* Any 'operationId' attribute value must follow typical programming naming conventions (unique, no spaces)
* Consistent Error body representation of user and application specific error codes (when used), as per GD-3.0 Part-1, Page-20
* Each error response should be described and consistent, such as:
* * '404' : { 'description' : 'Party Not Found', 'schema' : {'$ref': '#/definitions/Error'} }
* EntityRef: The EntityRef MUST include 'id' and 'href' attributes, other attributes MAY include: name, @type, @schemaLocation, validFor, role

Other additions being considered in the future:
* Home Document: 
* Linking: 
* Consistency to support automated code-generation, such as:
* * 'info.version' needs three degrees: major.minor.patch
* * Using dot.notation breaks the generator, such as (in params): { "name": "validFor.endDateTime", "format": "date-time", ... }
* * Swagger can be case-insensitive in some contexts, but the generator is case-sensitive

The tool can also be useful in generating tests for each resource within the API. This can be used to generate appropriate Postman scripts.

Use the online tool http://www.convertcsv.com/json-to-csv.htm to convert the output summary files (JSON) to Excel (xls) or CSV formats.
