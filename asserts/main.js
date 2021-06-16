var view_mode = 0;
var view_latest = 0;

var markline_y = [];

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
            name: "数值",
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

    let index = 0;

    if ((view_mode == 1) && (view_latest > 0) && (view_latest < data.length)) {
        index = data.length - view_latest;
    }


    for (; index < data.length; index++) {
        option_b7e5870db3d84d4db9639909239acfd9.xAxis[0].data.push(data[index].timestamp);

        if (data[index].data.length != option_b7e5870db3d84d4db9639909239acfd9.series.length) {
            console.warn("数据与图表的通道数不一致", data[index].data.length, option_b7e5870db3d84d4db9639909239acfd9.series.length)
        }

        let l = data[index].data.length;
        if (option_b7e5870db3d84d4db9639909239acfd9.series.length < l) l = option_b7e5870db3d84d4db9639909239acfd9.series.length;

        for (let index2 = 0; index2 < l; index2++) {
            option_b7e5870db3d84d4db9639909239acfd9.series[index2].data.push(data[index].data[index2]);
        }
    }
    option_b7e5870db3d84d4db9639909239acfd9.legend[0].selected = chart_b7e5870db3d84d4db9639909239acfd9.getOption().legend[0].selected;
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
            // connectNulls: true,
            smooth: false,
            data: [],
            markLine: {
                symbol:"none",
                label:{
                    position:"end"
                },
                data : [
                ],
            },
        });
        option_b7e5870db3d84d4db9639909239acfd9.legend[0].data.push(
            data[index].Name
        );
    }
    chart_b7e5870db3d84d4db9639909239acfd9.setOption(
        option_b7e5870db3d84d4db9639909239acfd9
    );
}
