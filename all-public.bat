rem Use .\\script.bat to run script on command line
rem Use http://www.convertcsv.com/json-to-csv.htm to convert the JSON summary file to CSV or XLS
rem Using local Service_Inventory_Management.regular.swagger.json due to "\v2\Release" causing invalid escape (\v) character
rem Using local paymentManagementTMF_v1.0.0_review9.json due to non UTF-8 encoding (loaded and resaved from http://editor.swagger.io/)
rem Using local shipmentTracking_v10_Jan18_SwaggerValidatorPassed.json due to non UTF-8 encoding (loaded and resaved from http://editor.swagger.io/)

py validator.py -s -l -d ^
    https://raw.githubusercontent.com/tmforum-apis/TMF641_ServiceOrder/master/Service_Ordering_Management.regular.swagger.json ^
    Service_Inventory_Management.regular.swagger.json ^
    paymentManagementTMF_v1_0_0.json ^
    shipmentTracking_v10_Jan18_SwaggerValidatorPassed.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF645_ServiceQualification/master/serviceQualification.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF646_AppointmentManagement/master/Appointment.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF622_ProductOrder/master/Product_Ordering_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF677_UsageConsumption/master/Usage_Consumption.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF679_ProductOfferingQualification/master/Product_Offering_Qualification_Management.regular.swagger.json ^
    "https://raw.githubusercontent.com/tmforum-apis/TMF672_UserRolesPermissions/master/UserRoles&Permissions_v1draft3_swagger_Released.json" ^
    https://raw.githubusercontent.com/tmforum-apis/TMF674_GeographicSite/master/GeographicSite_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF678_CustomerBill/master/CustomerBill_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF635_UsageManagement/master/TMF635_UsageManagement_swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF629_CustomerManagement/master/Customer_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF666_AccountManagement/master/Account_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF651_AgreementManagement/master/Agreement_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF669_PartyRole/master/Party_Role_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF668_PartnershipType/master/Partnership_Type_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF653_ServiceTestManagement/master/Service_Test_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF655_ChangeManagement/master/Change_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF657_ServiceQualityManagement/master/Service_Quality_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF671_Promotion/master/Promotion_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF680_Recommendation/master/Recommendation_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF681_Communication/master/Communication_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF691_FederatedIdentity/master/FederatedId_v11draft2_14thJune14_SwaggerValidatorPassed.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF632_PartyManagement/master/Party_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF675_GeographicLocation/master/GeographicLocation.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF673_GeographicAddress/master/GeographicAddress_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF648_QuoteManagement/master/Quote_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF620_ProductCatalog/master/TMF620_Product_Catalog_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum/TMFAPISWAGGER/develop/serviceActivationAndConfiguration/v2/swagger2.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF641_ServiceOrder/master/Service_Ordering_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF633_ServiceCatalog/master/TMF633_Service_Catalog_Management.admin.swagger_R17.5.json ^
    https://raw.githubusercontent.com/tmforum/TMFAPISWAGGER/develop/alarmManagement/v3/swagger2.json ^
    https://raw.githubusercontent.com/tmforum/TMFAPISWAGGER/develop/documentManagement/v2/swagger2.json ^
    https://raw.githubusercontent.com/tmforum/TMFAPISWAGGER/develop/entityCatalogManagement/v3/swagger2.json ^
    https://raw.githubusercontent.com/tmforum/DSPRIVACY/master/tmforum-Privacy-1.0-swagger-3.json ^
    https://raw.githubusercontent.com/tmforum-apis/WIP_TMF664_ResourceFunctionActivationConfiguration/master/ResourceFunctionActivationAndConfiguration.swagger.1.5.0.json ^
    https://raw.githubusercontent.com/tmforum-apis/WIP_TMF656_ServiceProblemManagement/master/Service_Problem_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/WIP_TMF623_SLAManagement/master/SLAManagement.swagger.2.0.json ^
    https://raw.githubusercontent.com/tmforum/DSPRIVACY/master/tmforum-Privacy-1.0-swagger-3.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF658_LoyaltyManagement/master/Loyalty_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF683_PartyInteraction/master/partyInteractionManagement_TMF_v1.0.0Review2.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF676_PaymentManagement/master/paymentManagementTMF_v1.0.0_review9 ^
    https://raw.githubusercontent.com/tmforum-apis/WIP_TMF649_PerformanceManagementThresholding/master/Perfromance_Management_Threshold.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF654_PrepayBalanceManagement/master/PrepayBalanceManagement_R17_v204.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF637_ProductInventory/master/Product_Inventory_Management.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF634_ResourceCatalog/master/TMF634_Resource_Catalog_Management.admin.swagger-R17.0.0.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF639_ResourceInventory/master/Resource_Inventory_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF652_ResourceOrderManagement/master/Resource_Ordering_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF685_ResourcePool/master/Resource_Pool_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF638_ServiceInventory/master/Service_Inventory_Management.regular.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF684_ShipmentTracking/master/shipmentTracking_v10_Jan18_SwaggerValidatorPassed.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF663_ShoppingCart/master/Shopping_Cart_Management.admin.swagger.json ^
    https://raw.githubusercontent.com/tmforum-apis/TMF621_TroubleTicket/master/Trouble_Ticket.swagger.json 