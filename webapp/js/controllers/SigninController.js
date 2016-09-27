define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering SigninController module.");

  var controller = ['$scope', 'SigninService', function ($scope,SigninService) {
    Console.group("SigninController entered.");

    $scope.queue = SigninService.query_yt();
  
    $scope.queueHead = {
      id: 'ID'
      , status: 'Status'
      , name: 'Name'
    };

    $scope.orderByCol = 'id';
    $scope.orderByReversed = false;

    $scope.flipOrderBy = function(col) {
      Console.group("orderByCol", col);
      $scope.orderByReversed = (col == $scope.orderByCol) ? !$scope.orderByReversed : false;
      $scope.orderByCol = col;

      Console.debug("reversed?", $scope.orderByReversed);
      Console.groupEnd();
    }

    Console.groupEnd();
  }];

  Console.groupEnd();
  return controller;
});
