App.controller('GenericListController', ['$scope', function ($scope) {

    $scope.records = [];
    $scope.data = {};

    $scope.headers = [];

    $scope.init = function (module) {
        $scope.module = module;
        $scope.model = module.replaceAll(' ', '').replaceAll('s', '').toLowerCase();
        $scope.end_point = `/api/${$scope.model}/`;
        $scope.main_url = `/cat/${$scope.model}/`
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
}]);