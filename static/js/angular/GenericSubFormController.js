App.controller('GenericSubFormController', ['$scope', 'Upload', function ($scope, Upload) {
    $scope.base_endpoint = '/api/'
    $scope.data = {}
    $scope.load_initial_data = function () {
        $.ajax({
            url: `${$scope.end_point}${$scope.item_id}/`
        }).then(function (res) {
            $scope.data = res;
        })
    }

    $scope.init = function (module, model, item_id, parent, parent_id) {
        $scope.module = module;
        $scope.model = model;
        $scope.item_id = item_id;
        $scope.parent_data = {
            class: parent,
            id: parent_id
        }
        $scope.end_point = `${$scope.base_endpoint}${$scope.model}/`;
        $scope.main_url = `/cat/${$scope.model}/`
        if ($scope.item_id) {
            $scope.load_initial_data();
        } else {
            $scope.data = {}
        }
        $scope.data[parent] = parent_id
    }

    $scope.upload_data = function (response = null) {
        let error_manage = function () {
            if (response) {
            }
        };
        let status_code_manage = {
            400: error_manage,
            500: error_manage
        };
        let url = $scope.end_point;
        let method = 'POST'
        if ($scope.data.id) {
            url = `${$scope.end_point}${$scope.data.id}/`
            method = 'PUT'
        }

        $.ajax({
            url: url,
            method: method,
            headers: {"X-CSRFToken": csrfmiddlewaretoken},
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                data: JSON.stringify($scope.data)
            },
            statusCode: status_code_manage
        }).done(function (res) {
            window.location.href = window.location.origin + `/cat/${$scope.parent_data.class}/${$scope.parent_data.id}/detail/`;
        })
    }

    $scope.save = function () {
        $scope.upload_data()
    }

    $scope.init();
}]);