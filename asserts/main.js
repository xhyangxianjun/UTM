var option_b7e5870db3d84d4db9639909239acfd9 = {
    "animation": false,
    // "animationThreshold": 200,
    // "animationDuration": 400,
    // "animationEasing": "cubicOut",
    // "animationDelay": 0,
    // "animationDurationUpdate": 200,
    // "animationEasingUpdate": "cubicOut",
    // "animationDelayUpdate": 0,
    "series": [
        {
            "type": "line",
            "name": "CH1",
            "data": []
        },
        {
            "type": "line",
            "name": "CH2",
            "data": []
        },
        {
            "type": "line",
            "name": "CH3",
            "data": []
        },
        {
            "type": "line",
            "name": "CH4",
            "data": []
        }
    ],
    "legend": [
        {
            "data": [
                "CH1",
                "CH2",
                "CH3",
                "CH4"
            ],
            "selected": {
                "CH1": true,
                "CH2": true,
                "CH3": true,
                "CH4": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0
    },
    "dataZoom": [{
        type: 'slider',
        xAxisIndex: 0,
        filterMode: 'empty'
    }, {
        type: 'inside',
        xAxisIndex: 0,
        filterMode: 'empty'
    }],
    "xAxis": [
        {
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            },
            "data": []
        }
    ],
    "yAxis": [
        {
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            }
        }
    ]
};

function clear_date() {
    option_b7e5870db3d84d4db9639909239acfd9.xAxis[0].data = [];
    option_b7e5870db3d84d4db9639909239acfd9.series[0].data = [];
    option_b7e5870db3d84d4db9639909239acfd9.series[1].data = [];
    option_b7e5870db3d84d4db9639909239acfd9.series[2].data = [];
    option_b7e5870db3d84d4db9639909239acfd9.series[3].data = [];
}

function resize() {
    chart_b7e5870db3d84d4db9639909239acfd9.resize();
}

function set_data(data) {
    clear_date()
    console.log(data)

    for (let index = 0; index < data.length; index++) {
        option_b7e5870db3d84d4db9639909239acfd9.xAxis[0].data.push(data[index].timestamp);

        for (let index2 = 0; index2 < data[index].data.length; index2++) {
            option_b7e5870db3d84d4db9639909239acfd9.series[index2].data.push(data[index].data[index2]);
        }
    }

    option_b7e5870db3d84d4db9639909239acfd9.legend[0].selected = chart_b7e5870db3d84d4db9639909239acfd9.getOption().legend[0].selected;

    chart_b7e5870db3d84d4db9639909239acfd9.setOption(option_b7e5870db3d84d4db9639909239acfd9)
}