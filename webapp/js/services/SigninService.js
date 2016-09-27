define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering SigninService module.");

  var service = ['$resource', function ($resource) {
    var url = 'http://richardxieq-pyproj.daoapp.io:port/pyproj/:website/signin';
    //var url = 'http://192.16.2.146:port/pyproj/:website/signin';
    return $resource(url, {
       //port: ':9902'
       port: ':80'
    }, {
      query_yt: {method: 'GET', params: {website: 'yt'}, isArray: true},
      query_tzj: {method: 'GET', params: {website: 'tzj'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
