define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering FinancingService module.");

  var service = ['$resource', 'constant',function ($resource, constant) {
    var url =  constant.url + ':port/pyproj/:user/financing/:title';
    return $resource(url, {
       port: constant.port
    }, {
      queryme: {method: 'GET', params: {user: 'richardxieq'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
