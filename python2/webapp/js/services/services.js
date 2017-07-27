define([
  // Standard Libs
  'Console'       // lib/console/console
  , 'Underscore'  // lib/underscore/underscore

  // Custom Services
  , 'services/DataService'
  , 'services/SigninService'
  , 'services/RulesService'
  , 'services/FinancingService'
], function(Console, _, ds, si, rules, financing) {
  "use strict";
  Console.group("Entering Service module.");
  Console.info("DataService", ds);
  Console.info("SigninService", si);
  Console.info("SigninService", rules);
  Console.info("FinancingService", financing);

  var services = {
    DataService: ds,
    SigninService: si,
    RulesService: rules,
    FinancingService: financing
  };
  Console.info("Registered services: ", services);

  var initialize = function (angModule) {
    _.each(services,function(service,name){
      angModule.factory(name,service);
    })
    Console.debug("Custom services initialized.");
  }

  Console.groupEnd();
  return {
    initialize: initialize
  };
});
