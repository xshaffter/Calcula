App.controller('GenericFormController', ['$scope', 'Upload', function ($scope, Upload) {
    $scope.base_endpoint = '/api/'
    $scope.data = {}
    $scope.load_initial_data = function () {
        $.ajax({
            url: `${$scope.end_point}${$scope.item_id}/`
        }).then(function (res) {
            $scope.data = res;
        })
    }


    $scope.init = function (module, model, item_id, action = "") {
        $scope.module = module;
        $scope.model = model;
        $scope.item_id = item_id;
        $scope.action = action;
        $scope.end_point = `${$scope.base_endpoint}${$scope.model}/`;
        $scope.main_url = `/cat/${$scope.model}/`
        if ($scope.item_id) {
            $scope.load_initial_data();
        } else {
            $scope.data = {}
        }
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
        if ($scope.action) {
            url += $scope.action + '/';
        }

        var reader = new FileReader();
        reader.readAsDataURL($scope.files.adjunto);
        reader.onload = function () {
            $.ajax({
                url: url,
                method: method,
                headers: {"X-CSRFToken": csrfmiddlewaretoken},
                data: {
                    csrfmiddlewaretoken: csrfmiddlewaretoken,
                    data: JSON.stringify($scope.data),
                    adjunto: reader.result
                },
                statusCode: status_code_manage
            }).done(function (res) {
                window.location.href = `${main_url}list/`;
            })
        };
        reader.onerror = function (error) {
            console.log('Error: ', error);
        };

    }

    $scope.save = function () {
        $scope.upload_data()
    }

    $scope.upload_sprite = function (sprite = null) {
        let response;
        if (!sprite) {
            response = Upload.upload({
                url: '/api/sprite/',
                data: {image: $scope.files.sprite}
            })
        } else {
            response = Upload.upload({
                url: '/api/sprite/',
                data: {image: sprite}
            })
        }
        return response;
    }
    $scope.delete_sprite = function (sprite = null) {
        return Upload.upload({
            url: `/api/sprite/${sprite}/delete/`,
        });
    }

    $scope.init();
}]);