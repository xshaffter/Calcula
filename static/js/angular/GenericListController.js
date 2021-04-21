App.controller('GenericListController', ['$scope', function ($scope) {

    $scope.main_url = main_url;
    $scope.end_point = end_point;
    $scope.module = module;

    $scope.records = [];
    $scope.data = {};

    $scope.headers = [];

    $scope.init = function () {
        $.ajax({
            url: '/api/modeldata/',
            data: {
                module: module
            }
        }).done(function (res) {
            $scope.headers = res.headers;
            $scope.actions = res.actions;
            $.ajax({
                url: end_point,
            }).done(function (res) {
                $scope.data = res;
                $scope.records = res;
                $scope.$apply();
            })
        })
    }

    $scope.acceed = function(object, direction) {
        let accessors = direction.replaceAll('[', '.').replaceAll(']', '').split('.')
        let value = false;
        accessors.forEach(accessor => {
            if (!value) {
                value = object[accessor];
            } else {
                value = value[accessor];
            }
        });
        return value;
    }

    $scope.init();
}]);