

angular.module('myApp', []).controller('managerController', ['$scope', function($scope, $http, $filter) {
	
	$scope.pathname = window.location.pathname.split('/')
	$scope.getAppManagers = '/api/mangerapp/' + $scope.pathname[$scope.pathname.length-2]+ '/'
	$scope.app
	$scope.showLoading = true
	$scope.getHostsUrl = '/api/hosts/'
	$scope.getGroupsUrl = '/api/groups/'
	$scope.hostList = []
	$scope.groupList = []
	
	$scope.configConditions = [
	                          {"name": "When app is inactive"},
	                          {"name": "Status OK to CRITICAL"},
	                          {"name": "Status CRITICAL to Ok"},
	                          {"name": "Status Ok to WARN"},
	                          {"name": "WARN Ok to CRITICAL"},
	]
	
	$scope.initData = function(){
		$.getJSON($scope.getAppManagers, {}, function(data) {
			$scope.$apply(function() {
				$scope.app = data
				$scope.showLoading = false
				console.log(data)
			})
		}).error(function(xhr, status, error) {
			console.log('Init wrong!');
		});
		$scope.getGroups()
		$scope.getHosts()
	}
	
	$scope.getHostNameByid = function(hostid){
		if($scope.hostList != null){
			for(var i=0; i<$scope.hostList.length; i++){
				if(hostid == $scope.hostList[i].id){
					return $scope.hostList[i].name
				}
			}
		}
		return "null"
	}
	
	$scope.getGroups = function(){
		$.getJSON($scope.getGroupsUrl, {}, function(data) {
			$scope.$apply(function() {
				$scope.groupList = data
			})
		}).error(function(xhr, status, error) {
			console.log('Init wrong!');
		});
	}
	
	$scope.getHosts = function(){
		$.getJSON($scope.getHostsUrl, {}, function(data) {
			$scope.$apply(function() {
				$scope.hostList = data
			})
		}).error(function(xhr, status, error) {
			console.log('get host wrong!');
		});
	}
}]);

$(document).ready(function() {
	setInterval(function() {
		$('.selectpicker').selectpicker('refresh');
		$(".description-temp").on("click", function(){
			$("#editAcitonAndCondition").click()
		});
	}, 1000);
});