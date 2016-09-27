define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering SigninService module.");

  var service = ['$resource', function ($resource) {

    return $resource('http://192.16.2.146:port/pyproj/:website/signin', {
       port: ':9902'
    }, {
      query_yt: {method: 'GET', params: {website: 'yt'}, isArray: true},
      query_tzj: {method: 'GET', params: {website: 'tzj'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
