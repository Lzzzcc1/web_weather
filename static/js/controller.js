//function gettime() {
//	$.ajax({
//		url: "/time",
//		timeout: 10000, //超时时间设置为10秒；
//		success: function(data) {
//			$("#time").html(data)
//		},
//		error: function(xhr, type, errorThrown) {
//
//		}
//	});
//}
//var a;
//window.onload = function(){
//    var obj_lis = document.getElementById("selectCity").getElementsByTagName("li");
//    for(i=0;i<obj_lis.length;i++){
//        obj_lis[i].onclick = function(){
//        	a = this.getAttribute("value")
//        	console.log(a)
//        }
//    }
//}
var city;
var month;
city = ""
month = ""

var obj_city = document.getElementById("selectCity").getElementsByTagName("li");
    for(i=0;i<obj_city.length;i++){
        obj_city[i].onclick = function(){
        	city = this.getAttribute("value")
        	document.getElementById("CurrentCity").text = city
        	get_c1_data({city: city, year_and_month: month})
        	get_l1_data({city: city, year_and_month: month})
        	get_history_data({city: city, year_and_month: month})
        	get_l2_data({city: city, year_and_month: month})
        	get_r1_data({city: city, year_and_month: month})
        	get_r2_data({city: city, year_and_month: month})
        	setInterval(get_l1_data, 1000*60*60)
        	}
    }

var obj_table = document.getElementById("navbaFuture").getElementsByTagName("a");
    for(i=0;i<obj_table.length;i++){
        obj_table[i].onclick = function(){
            var current_city = document.getElementById("CurrentCity").text
            console.log(current_city)
            window.location.href = "/future_weather?city=" + current_city
        	}
    }

var obj_table = document.getElementById("navbaTable").getElementsByTagName("a");
    for(i=0;i<obj_table.length;i++){
        obj_table[i].onclick = function(){
            console.log({city: city, year_and_month: month})
        	get_table_data({city: city, year_and_month: month})
        	}
    }

var obj_follow = document.getElementById("follow").getElementsByTagName("a");
    for(i=0;i<obj_follow.length;i++){
        obj_follow[i].onclick = function(){
        	follow_city({city: city})
        	}
    }


var special = document.getElementById("Special").getElementsByTagName("a");
    for(i=0;i<special.length;i++){
        special[i].onclick = function(){
        	get_special_data()
        	document.getElementById("CurrentCity").text = city
        	get_c1_data({city: city, year_and_month: month})
        	get_l1_data({city: city, year_and_month: month})
        	get_history_data({city: city, year_and_month: month})
        	get_l2_data({city: city, year_and_month: month})
        	get_r1_data({city: city, year_and_month: month})
        	get_r2_data({city: city, year_and_month: month})
        	}
    }

var csv = document.getElementById("export_csv").getElementsByTagName("a");
    for(i=0;i<csv.length;i++){
        csv[i].onclick = function(){
            export_csv({city:city, year_and_month: month})
        	}
    }

var time = document.getElementById("selectMonth").getElementsByTagName("li");
    for(i=0;i<time.length;i++){
        time[i].onclick = function(){
        	month = this.getAttribute("value")
        	document.getElementById("CurrentMonth").text = month
        	get_c1_data({city: city, year_and_month: month})
        	get_l1_data({city: city, year_and_month: month})
        	get_history_data({city: city, year_and_month: month})
        	get_l2_data({city: city, year_and_month: month})
        	get_r1_data({city: city, year_and_month: month})
        	get_r2_data({city: city, year_and_month: month})
        	setInterval(get_l1_data, 1000*60*60)
        	}
    }

function follow_city(params) {
	$.ajax({
		url: "/follow",
		dataType: "text",
        data: params,
        type: "POST",
		success: function(data) {
		    if (data == "ok")
		    {
		        alert('关注成功')
		    }
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

function export_csv(params) {
	$.ajax({
		url: "/export",
		dataType: "text",
        data: params,
        type: "POST",
		success: function(data) {
		    if (data == "ok")
		    {
		        location.href = "/download";
		    }
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

function get_special_data() {
	$.ajax({
		url: "/special",
		success: function(data) {
		    city = data
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

function get_c1_data(params) {
	$.ajax({
		url: "/c1",
		dataType: "json",
        data: params,
		success: function(data) {
			$(".num h1").eq(0).html(data.city)
			$(".num h1").eq(1).html(data.month)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

function get_table_data(params) {
	$.ajax({
        url: "/to_table",
        dataType: "json",
        data: params,
		success: function(data) {
		    var parm = JSON.stringify(data)
			window.location.href = "/table?data=" + parm;
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

function get_history_data(params) {
	$.ajax({
		url: "/history",
		dataType: "json",
        data: params,
		success: function(data) {
			$(".history_data p").eq(0).html(data.ah)
			$(".history_data p").eq(1).html(data.al)
			$(".history_data p").eq(2).html(data.ht)
			$(".history_data p").eq(3).html(data.lt)
			$(".history_data p").eq(4).html(data.aaq)
			$(".history_data p").eq(5).html(data.haq)
			$(".history_data p").eq(6).html(data.laq)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
// 中国地图 ec_center.js
// data: [{"上海":1,"杭州":2,}]
// 折线图
function get_l1_data(params) {
     $.ajax({
            url:"/line",
            dataType: "json",
            data: params,
            success: function(data) {
                option_left1.xAxis.data = data.date
                option_left1.series[0].data = data.highest
                option_left1.series[1].data = data.lowest
                ec_left1.setOption(option_left1)
            },
            error: function(xhr, type, errorThrown) {
            }
	    })
}


function get_l2_data(params) {
	$.ajax({
		url:"/wind",
		dataType: "json",
        data: params,
		success: function(data) {
			option_left2.xAxis.data = data.date
			option_left2.series[0].data = data.wind
			ec_left2.setOption(option_left2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

// 直方
function get_r1_data(params) {
	$.ajax({
		url:"/histogram",
		dataType: "json",
        data: params,
		success: function(data) {
			option_right1.xAxis.data = data.weather
			option_right1.series[0].data = data.count
			ec_right1.setOption(option_right1)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

// 风力天数
function get_r2_data(params) {
	$.ajax({
		url:"/wind_histogram",
		dataType: "json",
        data: params,
		success: function(data) {
			option_right2.xAxis.data = data.wind
			option_right2.series[0].data = data.wind_count
			ec_right2.setOption(option_right2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
//gettime()
get_history_data()
get_c1_data({"city": city, "year_and_month": month})
get_l1_data({"city": city, "year_and_month": month})
get_l2_data({"city": city, "year_and_month": month})
get_r1_data({"city": city, "year_and_month": month})
get_r2_data({"city": city, "year_and_month": month})
//setInterval(gettime, 1000)
setInterval(get_history_data, 1000*60*60)
setInterval(get_c1_data, 1000*60*60)
setInterval(get_l1_data, 1000*60*60)
setInterval(get_l1_data, 1000*60*60)
setInterval(get_r1_data, 1000*60*60)
setInterval(get_r1_data, 1000*60*60)
