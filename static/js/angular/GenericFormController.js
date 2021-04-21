App.controller('GenericFormController', ['$scope', 'Upload', function ($scope, Upload) {
    $scope.add_stat = function (stat_list) {
        if (!$scope.data[stat_list]) {
            $scope.data[stat_list] = [];
        }
        stat_list = $scope.data[stat_list];
        let all_filled = !(stat_list.length && stat_list.some(stat => !stat.stat && !stat.amount));
        if (stat_list.length < $scope.allowed_stats.length && all_filled) {
            stat_list.push(
                {
                    stat: '',
                    quantity: 0,
                    actions: ['delete',]
                },
            )
        } else {

        }
    }

    $scope.remove_stat = function (stat_list, stat) {
        $scope.data[stat_list] = $scope.data[stat_list].filter(stat_it => stat_it.stat !== stat.stat)
    }

    $scope.add_drop = function (drop_list) {
        console.log($scope.data[drop_list])
        if (!$scope.data[drop_list]) {
            $scope.data[drop_list] = [];
        }
        drop_list = $scope.data[drop_list];
        let all_filled = !(drop_list.length && drop_list.some(drop => !drop.drop && !drop.amount));
        if (drop_list.length < $scope.allowed_drops.length && all_filled) {
            drop_list.push(
                {
                    item: '',
                    min_quantity: 0,
                    max_quantity: 0,
                    probability: 0,
                    actions: ['delete',]
                },
            )
        } else {

        }
    }

    $scope.remove_drop = function (drop_list, drop) {
        $scope.data[drop_list] = $scope.data[drop_list].filter(drop_it => drop_it.item !== drop.item)
    }

    $scope.load_initial_data = function () {
        $.ajax({
            url: `${end_point}${item_id}/`
        }).then(function (res) {
            $scope.data = res;
            let sprite = res.item ? res.item[0].sprite_image : res.entity[0].sprite_image;
            fetch(sprite)
                .then(res => res.blob())
                .then(blob => {
                    $scope.files = {
                        sprite: blob,
                        selected: {
                            sprite: false
                        }
                    }
                    $scope.$apply();
                });
        })
    }

    $scope.init = function () {
        $.ajax({
            url: '/api/stat/'
        }).done(function (res) {
            $scope.allowed_stats = res;
            $.ajax({
                url: '/api/item/'
            }).done(function (res) {
                $scope.allowed_drops = res;
                if (item_id) {
                    $scope.load_initial_data();
                } else {
                    $scope.data = {
                        item: [{}],
                        entity: [{}],
                    }
                }
            });

        })
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

    $scope.upload_data = function (response = null) {
        if (response) {
            if (Object.keys($scope.data.item[0]).length > 0) {
                $scope.data.item[0].sprite = response.data.id;
            } else {
                $scope.data.entity[0].sprite = response.data.id;
            }
        }
        let error_manage = function () {
            if (response) {
                $scope.delete_sprite(response.data.id);
            }
        };
        let status_code_manage = {
            400: error_manage,
            500: error_manage
        };
        let url = end_point;
        let method = 'POST'
        if ($scope.data.id) {
            url = `${end_point}${$scope.data.id}/`
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
            window.location.href = `${main_url}list/`;
        })
    }

    $scope.save = function () {
        if ($scope.files.selected.sprite) {
            $scope.upload_sprite()
                .then($scope.upload_data);
        } else {
            $scope.upload_data()
        }
    }

    $scope.init();
}]);