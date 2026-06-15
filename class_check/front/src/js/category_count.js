var CategoryInfo = function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));

    $.ajax({
        url: "/check_count/",
        type: 'POST',
        data: {},
        success: function (result) {
            if (result['code'] == 200) {
                option = {
                    title: {
                        text: '检测分布',
                        subtext: '',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left'
                    },
                    series: [
                        {
                            name: '',
                            type: 'pie',
                            radius: '50%',
                            data: result['data'],
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

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            } else {
                alert(result['message']);
            }
        }
    });
};


$(function () {
    var handler = new CategoryInfo();
});