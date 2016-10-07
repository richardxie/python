define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering RulesService module.");

  var service = ['$resource', function ($resource) {
    //var url = 'http://richardxieq-pyproj.daoapp.io:port/pyproj/:website/signin';
    var url = 'http://localhost:port/pyproj/tender/rules';
    return $resource(url, {
       port: ':9902'
       //port: ':80'
    }, {
      query: {method: 'GET', params: {website: 'yt'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
