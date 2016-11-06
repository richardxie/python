define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering FinancingService module.");

  var service = ['$resource', 'constant',function ($resource, constant) {
    var url =  constant.url + ':port/pyproj/financing';
    return $resource(url, {
       port: constant.port
    }, {
      query: {method: 'GET', params: {website: 'yt'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
