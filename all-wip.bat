rem Use .\\script.bat to run script on command line
rem Use http://www.convertcsv.com/json-to-csv.htm to convert the JSON summary file to CSV or XLS
rem NOT A VALID FILE: changeManagement-v2-swagger2.json, productOfferingQualification-v2-swagger2.yaml, paymentManagementTMF_v1.0.0_review9.swagger.json^
rem NOT A VALID FILE: prepayBalanceManagement-v3-swagger2.json, promotionManagement-v3-swagger2.json, Service_Ordering_Management.regular.swagger.json, serviceCatalogManagement-v2-swagger2.json


py validator.py -s -l -d ^
  https://raw.githubusercontent.com/tmforum-apis/TMF671_Promotion/master/Promotion_Management.admin.swagger.json