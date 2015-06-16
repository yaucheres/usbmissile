'use strict';

/* Controllers */

var usbmissileApp = angular.module('usbMissile', []);

usbmissileApp.controller('MissileCmd', ['$scope', '$http',
    function ($scope, $http) {
        
        $scope.cmd = function(action) {            
            $http.get('/api/'+action).success(function(data){
                console.log('cmd: '+action);
            })
            .error(function(data, status){
                console.log('status: '+status);
            });
            
        };
                
    }
]);
