

function get_pages(actual, maximum) {
    let pages = [];
    let min_page = actual - 3 > 1 ? actual - 3 : 1;
    let max_page = actual + 3 < maximum ? actual + 3 : maximum;
    for (let i = min_page; i <= max_page; i++) pages.push(i)
    return pages;
}

App.controller('GenericListController', ['$scope', function ($scope) {

    $scope.records = [];
    $scope.data = {};

    $scope.headers = [];

    $scope.init = function (module, model) {
        $scope.module = module;
        $scope.model = model;
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
            $scope.load();
        })
    }

    $scope.load = function (page = null) {
        $.ajax({
            url: $scope.end_point,
            method: 'GET',
            data: {
                page: page || $scope.data.page || 1,
                user_id: user_id
            }
        }).done(function (res) {
            $scope.data = res;
            $scope.records = res.results;
            $scope.data.pages = get_pages($scope.data.page, $scope.data.total_pages);
            $scope.$apply();
        })
    }

    $scope.go_previous = function () {
        $scope.load($scope.data.page - 1)
    }
    $scope.go_next = function () {
        $scope.load($scope.data.page + 1)
    }
    $scope.goto = function (page) {
        $scope.load(page)
    }

    $scope.acceed = function (object, direction) {
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