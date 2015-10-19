/**
 *
 */

angular.module('myApp', []).controller('myController', function($scope, $http, $filter) {
	$scope.getCountGroupsUrl = '/api/count/groups/'
	$scope.getAppListByGroupUrl = '/api/apps/'
	$scope.getAppHistoryUrl = '/api/history/'
	$scope.getAppStatisticsUrl = '/api/statistics/'
	$scope.countGroups
	$scope.currentGroup
	$scope.filterApp = ''
	$scope.appList = []
	$scope.defaultItemPerPage = 2
	$scope.defautPage = 1


	$scope.header = [ {
		"name" : "status",
		"displayName" : "Status",
		"colClass" : "col-lg-1"
	}, {
		"name" : "host",
		"displayName" : "Host",
		"colClass" : "col-lg-2"
	}, {
		"name" : "name",
		"displayName" : "Name",
		"colClass" : "col-lg-6"
	}, {
		"name" : "lastupdate",
		"displayName" : "Last Active",
		"colClass" : "col-lg-2"
	} , {
		"name" : "operation",
		"displayName" : "",
		"colClass" : "col-lg-1"
	} ];
	
	$scope.pageation = {
			'currentPage' : $scope.defautPage ,
			"itemPerPage" : $scope.defaultItemPerPage,
			"totalnum" : 0,
			'pages': [],
	}
	
	// Update currentPagination method
	$scope.pagenationTo = function(n){
			$scope.pageation.currentPage = n;
	}
	
	$scope.changeSorting = function(header) {
		column = header["name"]
		if ($scope.sort.column == column) {
			$scope.sort.descending = !$scope.sort.descending;
		} else {
			$scope.sort.column = column;
			$scope.sort.descending = false;
		}
	};
	
	// Custom sorting function
	$scope.customSort = function(app){
		return app[$scope.sort.column]
	};

	$scope.sort = {
		column : 'status',
		descending : false
	};

	$scope.getAppsByFilter = function(){
		applist = $scope.appList
		if($scope.filterApp){
			applist = $filter("filter")($scope.appList, $scope.filterApp)
		}
		//Recalculate page number
		pages = [];
		for (var i = 1; (i -1) * $scope.pageation.itemPerPage < applist.length; i ++) {
			pages.push(i);
		}
		$scope.pageation.pages = pages
		$scope.pageation.totalnum = applist.length
		return applist
	}
	
	$scope.drawDetails = function(app, $event){
		if ($($event.target).is("td")) {
			chartContainer = $($event.target).closest("tr").next("tr");
			chartContainer.toggle();
			$.getJSON($scope.getAppHistoryUrl, {"appid": app.id}, function(data) {
				$scope.$apply(function() {
					drawHistory(chartContainer, app, data);
				})
			}).error(function(xhr, status, error) {
			});
		}
		$scope.highChartsDrawing(app, chartContainer)
		if(app.message != null && app.message.length>2){
			$scope.getInformation(app, $event)
		}
	}
	
	$scope.getInformation = function(app, $event){
		chartContainer = $($event.target).closest("tr").next("tr");
		message = app.message.replace(/\r\n/g, "<BR>")
		message = message.replace(/\n/g, "<BR>");
		chartContainer.find("[name='information']").html(message);
	}

	$scope.getNavCss = function(countgroup){
		if (countgroup.statistics.critical > 0){
			return "icon-critical"
		}else if(countgroup.statistics.warn > 0){
			return "icon-warn"
		}else{
			return 'icon-ok'
		}
	}
	
	$scope.getClassByStatus = function(status){
		if(status == "OK"){ 
			return "glyphicon-ok-circle "
		}else if(status == "CRITICAL"){
			return "glyphicon-remove-circle "
		}else if(status == "WARN"){
			return "glyphicon-exclamation-sign "
		}
	}
	
	$scope.changeGroup = function(group){
		$scope.currentGroup = group
		$scope.getCountGroupsDatas()
		$scope.getAppLlist(group)
	}
	
	$scope.getAppLlist = function(gorup){
		$.getJSON($scope.getAppListByGroupUrl, {"groupid": gorup.id}, function(data) {
			$scope.$apply(function() {
				$scope.appList = data
			})
		}).error(function(xhr, status, error) {
		});
	}
	
	$scope.isCurrentGroup = function(countgroup){
		if($scope.currentGroup == null && $scope.countGroups != null){
			$scope.changeGroup($scope.countGroups[0])
		}
		if(countgroup.uniqueName == $scope.currentGroup.uniqueName){
			return "active"
		}
	}
	
	$scope.getCountGroupsDatas = function(){
		$http({
			  method: 'GET',
			  url: $scope.getCountGroupsUrl
			}).then(function successCallback(response) {
				$scope.countGroups = response.data
				
			  }, function errorCallback(response) {
			  });
	}
	
	$scope.initData = function(){
		$scope.getCountGroupsDatas()
	}
	
	$scope.highChartsDrawing = function(app, chartContainer, date){
		subtitle = ''
		chartContainer.find("#highCharts").html("<img height='60px;' src='../../static/images/loading.gif' />")
		$.getJSON($scope.getAppStatisticsUrl + app.id, date, function(data) {
			$scope.$apply(function() {
				chartContainer.find("#highCharts").html("")
				width = chartContainer.width() - 20;
				height = 250
				if(data.length > 1 || date != null){
					chartContainer.find("#searchDates").show()
					statisticsData_list = []
					for (var i=0;i<data.length; i++){
						datas = angular.fromJson(data[i].statistics)
						for (property in datas) {
							havaSameData = false
							for(var j=0;j<statisticsData_list.length;j++){
								if(statisticsData_list[j].name == property){
									havaSameData = true
									statisticsData_list[j].data.push([data[i].time * 1000, datas[property]])
								}
							}
							if(!havaSameData){
								statisticsData_list.push({"pointWidth": 12, "name": property, "data": [[data[i].time * 1000, datas[property]]]})
							}
						}
					}
					if(date != null && statisticsData_list.length<1){
						subtitle = ' No data'
						height = 50
						drawHighChart(chartContainer.find("#highCharts"), statisticsData_list, width, height, subtitle);
					}else{
						drawHighChart(chartContainer.find("#highCharts"), statisticsData_list, width, height, subtitle);
					}
				}
			})
		}).error(function(xhr, status, error) {
			alertify.error('Get App statistics Wrong!');
		});
	}

});

function drawHistory(chartContainer, app, data){
	var historyString = "History:  "
	historyList = data.reverse()
	for(var key in historyList){
		var status = historyList[key]['status']
		var time = historyList[key]['time']
		if(key == historyList.length-1){
			historyString += "<span data-toggle='tooltip' class='label label-default icon-"+status+"' title='"+time+"'>"+status+"</span></br>"
		}else{
			historyString += "<span data-toggle='tooltip' class='label label-default icon-"+status+"' title='"+time+"'>"+status+"</span><span class='glyphicon glyphicon-arrow-right app-glyphicon-right arrow'></span>"
		}
	}
	chartContainer.find("#statushistory").html(historyString);
}

function drawHighChart(chartContainer, datas, width, height,  title){
	chartContainer.highcharts({
		chart : {
			//type: 'column',
			type: 'spline',
			//type:'area',
			//type:'scatter',
			width : width,
			height : height,
		 zoomType: 'x',
            resetZoomButton: {
                position: {
                    x: 0,
                    y: 0
                }
            }
		},
	        title: {
	            text: title
	        },
	        subtitle: {
	        	text: ""
	        },
	        xAxis: {
	        	type: 'datetime',
	        	labels: {  
                    step: 4,   
                    formatter: function () {  
                        return Highcharts.dateFormat('%Y/%m/%d %H:%M:%S', this.value);  
                    }  
                }  
	        },
	        yAxis: {
	            min: 0,
	            title: {
	                text: ''
	            },
	        },
	        tooltip: {
	        	 formatter: function() {
	                    return '<b>'+ this.series.name +'</b><br/>'+
	                    Highcharts.dateFormat('%Y/%m/%d %H:%M:%S', this.x) +'= '+ this.y +' ';;
	            }
	        },
	        series: datas
	    });
};
