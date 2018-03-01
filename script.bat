rem Use .\\script.bat to run script on command line
rem Use http://www.convertcsv.com/json-to-csv.htm to convert the JSON summary file to CSV or XLS
rem DOES NOT PARSE: changeManagement-v2-swagger2.json, paymentMethod-v3-swagger2.json, productOfferingQualification-v2-swagger2.yaml, paymentManagementTMF_v1.0.0_review9.swagger.json^
rem DOES NOT PARSE: prepayBalanceManagement-v3-swagger2.json, promotionManagement-v3-swagger2.json, Service_Ordering_Management.regular.swagger.json, serviceCatalogManagement-v2-swagger2.json


python validator.py -s -l -d ^
 swagger\accountManagement-v3-swagger2.json^
 swagger\addressManagement-v2-swagger2.json^
 swagger\agreementManagement-v2-swagger2.json^
 swagger\alarmManagement-v3-swagger2.json^
 swagger\appointmentManagement-v2-swagger2.json^
 swagger\billingManagement-v2-swagger2.json^
 swagger\communicationManagement-v3-swagger2.json^
 swagger\customerBillManagement-v3-swagger2.json^
 swagger\customerManagement-v3-swagger2.json^
 swagger\communicationManagement-v3-swagger2.json^
 swagger\customerBillManagement-v3-swagger2.json^
 swagger\customerManagement-v3-swagger2.json^
 swagger\documentManagement-v2-swagger2.json^
 swagger\entityCatalogManagement-v3-swagger2.json^
 swagger\geographicAddressManagement-v3-swagger2.json^
 swagger\geographicLocationManagement-v3-swagger2.json^
 swagger\geographicSiteManagement-v3-swagger2.json^
 swagger\loyaltyManagement-v3-swagger2.json^
 swagger\onboardingManagement-v2-swagger2.json^
 swagger\partnershipTypeManagemnet-v3-swagger2.json^
 swagger\partyManagement-v2-swagger2.json^
 swagger\partyRoleManagement-v3-swagger2.json^
 swagger\performanceManagementThreshold-v3-swagger2.json^
 swagger\privacyManagement-v2-swagger2.json^
 swagger\productCatalog-v2-swagger2.json^
 swagger\productInventory-v2-swagger2.json^
 swagger\productOrdering-v2-swagger2.json^
 swagger\quoteManagement-v3-swagger2.json^
 swagger\resourceCatalogManagement-v3-swagger2.json^
 swagger\resourceFunctionActivationConfiguration-v2-swagger2.json^
 swagger\resourceInventoryManagement-v3-swagger2.json^
 swagger\Service_Inventory_Management.regular.swagger.json^
 swagger\Service_Qualification.regular.swagger.json^
 swagger\serviceActivationAndConfiguration-v2-swagger2.json^
 swagger\serviceQualityManagement-v2-swagger2.json^
 swagger\serviceTestManagement-v2-swagger2.json^
 swagger\shipmentTrackingTMF.json^
 swagger\shoppingCart-v3-swagger2.json^
 swagger\slaManagement-v2-swagger2.json^
 swagger\troubleTicket-v2-swagger2.json^
 swagger\usageConsumption-v3-swagger2.json^
 swagger\usageManagement-v2-swagger2.json^
 swagger\userRolesPermissions-v3-swagger2.json