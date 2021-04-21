var App = angular.module('App', ['ngFileUpload']);

App.config(function($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    });

App.filter('reverse', function() {
    return function(items) {
        return items.slice().reverse();
    };
});