var DDD = [];

let historyRefuelling = [
    [0, 5],
    [1, 7]
]

let historyTheft = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4]
]


var option_b7e5870db3d84d4db9639909239acfd9 = {
    title: {
        show: false
    },
    animation: false,
    series: [],
    legend: [
        {
            data: ["CH1", "CH2", "CH3", "CH4"],
            show: true,
        },
    ],
    grid: {
        left: "30",
        right: "30",
        top: "50",
    },
    tooltip: {
        trigger: "axis",
        axisPointer: {
            type: "cross",
        },
        // formatter: function (params) {
        //     var chartdate = echarts.format.formatTime('h:m:s.SSS', params[0].value[0]);
        //     var val = '';

        //     for (let index = 0; index < params.length; index++) {
        //         val += '<li style="list-style:none">' + params[index].marker +
        //             params[index].seriesName + '&nbsp;&nbsp;' + params[index].value[1] + '</li>';
        //     }
        //     return chartdate + val;
        // },
    },
    dataZoom: [
        {
            type: "slider",
            xAxisIndex: 0,
            filterMode: "empty",
        },
        {
            type: "inside",
            xAxisIndex: 0,
            filterMode: "empty",
        },
    ],
    xAxis: [
        {
            // "type": "time",
            "boundaryGap": false,
            "nameLocation": "end",
            "nameGap": 10,
            "splitNumber": 5,
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "show": true,
                },
            },
            axisLabel: {
                // rotate: 30,
                // formatter: function (value) {
                //     return echarts.format.formatTime('h:m:s.SSS', new Date(value));
                // }
            },
            data: [],
        },
    ],
    yAxis: [
        {
            type: "value",
            boundaryGap: false,
        },
    ],
};

function clear_date() {
    option_b7e5870db3d84d4db9639909239acfd9.xAxis[0].data = [];

    for (let index = 0; index < option_b7e5870db3d84d4db9639909239acfd9.series.length; index++) {
        option_b7e5870db3d84d4db9639909239acfd9.series[index].data = [];
    }
}

function resize() {
    chart_b7e5870db3d84d4db9639909239acfd9.resize();
}

function set_data(data) {
    clear_date()

    for (let index = 0; index < data.length; index++) {
        option_b7e5870db3d84d4db9639909239acfd9.xAxis[0].data.push(data[index].timestamp);

        for (let index2 = 0; index2 < data[index].data.length; index2++) {
            option_b7e5870db3d84d4db9639909239acfd9.series[index2].data.push(data[index].data[index2]);
        }
    }

    option_b7e5870db3d84d4db9639909239acfd9.legend[0].selected = chart_b7e5870db3d84d4db9639909239acfd9.getOption().legend[0].selected;

    // if (data.length >= 50) {
    //     option_b7e5870db3d84d4db9639909239acfd9.dataZoom[0].startValue = data[data.length - 50].timestamp
    //     option_b7e5870db3d84d4db9639909239acfd9.dataZoom[0].endValue = data[data.length - 1].timestamp
    //     option_b7e5870db3d84d4db9639909239acfd9.dataZoom[1].startValue = data[data.length - 50].timestamp
    //     option_b7e5870db3d84d4db9639909239acfd9.dataZoom[1].endValue = data[data.length - 1].timestamp
    // }

    chart_b7e5870db3d84d4db9639909239acfd9.setOption(option_b7e5870db3d84d4db9639909239acfd9)
}

function set_data_a(data) {
    clear_date();
    // console.log(data)

    for (let index = 0; index < data.length; index++) {
        // console.log("push_data", data[index].data.length, index, data[index]);
        for (let index2 = 0; index2 < data[index].data.length; index2++) {
            option_b7e5870db3d84d4db9639909239acfd9.series[index2].data.push(
                [data[index].timestamp, data[index].data[index2]]
            );
            // console.log("push_data_item", index, index2, option_b7e5870db3d84d4db9639909239acfd9.series[index2].data);
        }
    }


    option_b7e5870db3d84d4db9639909239acfd9.legend[0].selected = chart_b7e5870db3d84d4db9639909239acfd9.getOption().legend[0].selected;

    chart_b7e5870db3d84d4db9639909239acfd9.setOption(
        option_b7e5870db3d84d4db9639909239acfd9
    );
}

function push_data(data) {
    DDD.push(data);
    set_data(DDD);
}

function set_channel(data) {
    option_b7e5870db3d84d4db9639909239acfd9.xAxis[0].data = [];
    option_b7e5870db3d84d4db9639909239acfd9.series = [];
    option_b7e5870db3d84d4db9639909239acfd9.legend[0].data = [];
    DDD = [];

    for (let index = 0; index < data.length; index++) {
        option_b7e5870db3d84d4db9639909239acfd9.series.push({
            type: "line",
            name: data[index].Name,
            sampling: "max",
            // symbol: 'rect',
            smooth: false,
            data: [],
        });
        option_b7e5870db3d84d4db9639909239acfd9.legend[0].data.push(
            data[index].Name
        );
    }
    chart_b7e5870db3d84d4db9639909239acfd9.setOption(
        option_b7e5870db3d84d4db9639909239acfd9
    );
}

var date = [];

var data = [];
var data2 = [];

for (var i = 1; i < 20000; i++) {
    date.push(i);
    //data.push(Math.round((Math.random() - 0.5) * 20 + data[i - 1]));
    data.push(Math.sin(i * 0.001))
    data2.push(Math.cos(i * 0.001))
}

option_a = {
    tooltip: {
        trigger: 'axis',
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        left: 'center',
        text: '大数据量面积图',
    },
    legend: {
        data: ['意向']
    },
    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        "splitLine": {
            "show": true,
            // "type": 'dashed',
            "lineStyle": {
                "show": true,
            },
        },
        data: date
    },
    yAxis: {
        type: 'value',
    },
    dataZoom: [{
        type: 'inside',
        start: 0,
        end: 100
    }, {
        type: "slider",
        start: 0,
        end: 100,
    }],
    series: [{
        name: '模拟数据',
        type: 'line',
        smooth: false,
        sampling: 'average',
        // symbol: 'rect',
        data: data
    }, {
        name: '模拟数据A',
        type: 'line',
        smooth: false,
        sampling: 'average',
        // symbol: 'rect',
        data: data2
    }]
};
