define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering SigninService module.");

  var service = ['$resource', 'constant',function ($resource, constant) {
    var url = constant.url + ':port/pyproj/:website/signin';
    return $resource(url, {
       port: constant.port
    }, {
      query_yt: {method: 'GET', params: {website: 'yt'}, isArray: true},
      query_tzj: {method: 'GET', params: {website: 'tzj'}, isArray: true},
    });

  }];

  Console.groupEnd();
  return service;
});
