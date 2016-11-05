define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering RulesController module.");

  var controller = ['$scope', 'RulesService', function ($scope,RulesService) {
    Console.group("RulesController entered.");

    $scope.queue = RulesService.query();
  
    $scope.queueHead = {
      name: '名称'
      , term: '期限'
      , status: '状态'
      , operation: '操作'
    };

    $scope.orderByCol = 'name';
    $scope.orderByReversed = false;

    $scope.flipOrderBy = function(col) {
      Console.group("orderByCol", col);
      $scope.orderByReversed = (col == $scope.orderByCol) ? !$scope.orderByReversed : false;
      $scope.orderByCol = col;

      Console.debug("reversed?", $scope.orderByReversed);
      Console.groupEnd();
    }

    $scope.toggle = function(id) {
       Console.group("toggel rule setting", id);
       Console.groupEnd();
    }

    Console.groupEnd();
  }];

  Console.groupEnd();
  return controller;
});
