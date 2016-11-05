define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering RulesService module.");

  var service = ['$resource', 'constant',function ($resource, constant) {
    var url =  constant.url + ':port/pyproj/tender/rule';
    return $resource(url, {
       port: constant.port
    }, {
      query: {method: 'GET', params: {website: 'yt'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
