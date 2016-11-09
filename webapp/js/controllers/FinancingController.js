define(['Console'], function (Console) {
  "use strict";
  Console.group("Entering FinancingController module.");

  var controller = ['$scope', 'FinancingService', function ($scope,FinancingService) {
    Console.group("FinancingController entered.");

    $scope.queue = FinancingService.queryme();
  
    $scope.queueHead = ['项目标题','还款总额', '应还日期', '期限', '利率', '状态','操作'];

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
