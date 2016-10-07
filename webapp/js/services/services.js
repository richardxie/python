define([
  // Standard Libs
  'Console'       // lib/console/console
  , 'Underscore'  // lib/underscore/underscore

  // Custom Services
  , 'services/DataService'
  , 'services/SigninService'
  , 'services/RulesService'
], function(Console, _, ds, si, rules) {
  "use strict";
  Console.group("Entering Service module.");
  Console.info("DataService", ds);
  Console.info("SigninService", si);
  Console.info("SigninService", rules);

  var services = {
    DataService: ds,
    SigninService: si,
    RulesService: rules
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
