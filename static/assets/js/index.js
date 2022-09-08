$(function () {
    initBur();
    initcake();

})

function initBur() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('Chart1'));
// 指定图表的配置项和数据
    var option = {
        title: {
            text: '项目统计表'
        },
        tooltip: {},
        legend: {
            data: [],
            bottom: 0
        },
        xAxis: {
            data: []
        },
        yAxis: {},
        series: []
    }
    $.ajax({
        url: '/user/chart/',
        type: 'get',
        dataType: 'JSON',
        success: function (res) {
            // 使用刚指定的配置项和数据显示图表。
            if (res.status) {
                option.legend.data = res.legend;
                option.xAxis.data = res.xAxis;
                option.series = res.series;
            }
            myChart.setOption(option);


        }


    })


}

function initcake() {
    var chartDom = document.getElementById('Chart2');
    var myChart = echarts.init(chartDom);
    var option = {
        title: {
            text: '项目分布区域占比',
            subtext: '项目分布',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            bottom: 0
        },
        series: [
            {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: [],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    $.ajax({
        url: '/user/cake/',
        type: 'get',
        dataType: 'JSON',
        success: function (res) {
            if (res.status) {
                option.series[0].data = res.series
                option && myChart.setOption(option);

            }

        }
    })


}


$(function () {
    $("#media1").attr('src', '/test_resp/?path=/media/video.mp4');
})


window.onload = function hiddle_col() {
    $('.breadcrumb-wrapper').attr("hidden", true);
}
