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
city = document.getElementById("CurrentCity").text
var date;
date = document.getElementById("CurrentDate").text

var obj_city = document.getElementById("selectCity").getElementsByTagName("li");
    for(i=0;i<obj_city.length;i++){
        obj_city[i].onclick = function(){
        	city = this.getAttribute("value")
        	document.getElementById("CurrentCity").text = city
        	get_l1_data({city: city})
        	get_r1_data({city: city})
        	get_r2_data({city: city})
        	get_current_data({city: city, date: date})
        	setInterval(get_l1_data, 1000*60*60)
        	}
    }

var obj_city = document.getElementById("selectDate").getElementsByTagName("li");
    for(i=0;i<obj_city.length;i++){
        obj_city[i].onclick = function(){
        	date = this.getAttribute("value")
        	document.getElementById("CurrentDate").text = date
        	get_current_data({city: city, date: date})
        	setInterval(get_l1_data, 1000*60*60)
        	}
    }

var csv = document.getElementById("export_csv").getElementsByTagName("a");
    for(i=0;i<csv.length;i++){
        csv[i].onclick = function(){
            export_csv({city:city, date:date})
        	}
    }

var csv = document.getElementById("navbaReturn").getElementsByTagName("a");
    for(i=0;i<csv.length;i++){
        csv[i].onclick = function(){
            window.location.href = "/index"
        	}
    }

function get_current_data(params) {
	$.ajax({
		url: "/current_data",
		dataType: "json",
        data: params,
        type: "POST",
		success: function(data) {
		    console.log(data)
			$(".current_data p").eq(0).html(data.date)
			$(".current_data p").eq(1).html(data.lt)
			$(".current_data p").eq(2).html(data.ht)
			$(".current_data p").eq(3).html(data.weather)
			$(".current_data p").eq(4).html(data.humidity)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

function export_csv(params) {
	$.ajax({
		url: "/export_future",
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


function get_l1_data(params) {
     $.ajax({
            url:"/future_line",
            dataType: "json",
            type: "POST",
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



// 直方
function get_r1_data(params) {
	$.ajax({
		url:"/future_histogram",
		dataType: "json",
		type: "POST",
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

function get_r2_data(params) {
	$.ajax({
		url:"/humidity_line",
		dataType: "json",
		type: "POST",
        data: params,
		success: function(data) {
		    console.log(data)
			option_right2.xAxis.data = data.date
			option_right2.series[0].data = data.humidity
			ec_right2.setOption(option_right2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}



get_l1_data({"city": city})
get_r1_data({"city": city})
get_r2_data({"city": city})
get_current_data({"city": city, "date": date})
//setInterval(gettime, 1000)
setInterval(get_l1_data, 1000*60*60)
setInterval(get_r1_data, 1000*60*60)

