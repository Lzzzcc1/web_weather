var ec_right2 = echarts.init(document.getElementById("r2"),"white");

option_right2 = {
	title: {
		text: '风力天数统计',
		textStyle: {
			color: 'black'
		},
		left: 'left'
	},
	// grid: {
	// 	left: 50,
	// 	top: 50,
	// 	right: 0,
	// 	width: '87%',
	// 	height: 320,
	// },
	color: ['#3398DB'],
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'shadow'
		}
	},
	//全局字体样式
	// textStyle: {
	// 	fontFamily: 'PingFangSC-Medium',
	// 	fontSize: 12,
	// 	color: '#858E96',
	// 	lineHeight: 12
	// },
	xAxis: {
		type: 'category',
		//                              scale:true,
		data: []
	},
	yAxis: {
		type: 'value',
		//坐标轴刻度设置
		},
	series: [{
		type: 'bar',
		data: [],
		barMaxWidth: "50%"
	}]
};
ec_right2.setOption(option_right2)
