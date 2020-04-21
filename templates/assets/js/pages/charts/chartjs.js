
//=========================
$(function () {

    var options;
    var data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        series: [
            [200, 190, 185, 156, 165, 143, 120, 135, 124, 120, 115, 117],
        ]
    };

    // line chart
    options = {
        height: "300px",
        showPoint: true,
        axisX: {
            showGrid: false
        },

        lineSmooth: false,

        plugins: [
            Chartist.plugins.tooltip({
                appendToBody: true
            }),
        ]
    };
    new Chartist.Line('#line-chart', data, options);

    // bar chart
    options = {
        height: "300px",
        axisX: {
            showGrid: false
        },
        plugins: [
            Chartist.plugins.tooltip({
                appendToBody: true
            }),
        ]
    };
    new Chartist.Bar('#bar-chart', data, options);

    // area chart
    options = {
        height: "300px",
        low: 50,
        showArea: true,
        showLine: false,
        showPoint: true,

        axisX: {
            showGrid: false
        },
        
        lineSmooth: false,
    };
    new Chartist.Line('#area-chart', data, options);


    // multiple chart
    var dataMultiple = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        series: [{
            name: 'series-real',
            data: [1200, 1380, 1320, 1320, 1410, 1295, 1570, 1400, 1555, 2620, 1750, 1900],
        }, {
            name: 'series-projection',
            data: [1240, 1280, 1360, 560, 1199, 1450, 2280, 1523, 1246, 1600, 1457, 1689],
        }]
    };
    options = {
        lineSmooth: false,
        height: "260px",
        low: 500,
        high: 'auto',
        series: {
            'series-projection': {
                showPoint: true,
            },
        },

        options: {
            responsive: true,
            legend: false
        },

        plugins: [
            Chartist.plugins.legend({
                legendNames: ['KCal. Ingested', 'KCal. Burned']
            })
        ]
    };
    new Chartist.Line('#multiple-chart', dataMultiple, options);


    // pie chart
    var dataPie = {
        series: [5, 3, 4]
    };
    var labels = ['Direct', 'Organic', 'Referral'];
    var sum = function (a, b) {
        return a + b;
    };
    new Chartist.Pie('#pie-chart', dataPie, {
        height: "270px",
        labelInterpolationFnc: function (value, idx) {
            var percentage = Math.round(value / dataPie.series.reduce(sum) * 100) + '%';
            return labels[idx] + ' (' + percentage + ')';
        }
    });


    // donut chart
    var dataDonut = {
        labels: ['Fats', 'Proteins', 'Minerals', 'Carbohydrates'],
        series: [20, 10, 30, 40]
    };
    new Chartist.Pie('#donut-chart', dataDonut, {
        height: "270px",
        donut: true,
        donutWidth: 60,
        donutSolid: true,
        startAngle: 270,
        showLabel: true
    });


    // stacked bar chart
    var dataStackedBar = {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        series: [
            [800000, 1200000, 360000, 1300000],
            [200000, 400000, 500000, 300000],
            [100000, 200000, 400000, 600000]
        ]
    };
    new Chartist.Bar('#stackedbar-chart', dataStackedBar, {
        height: "270px",
        stackBars: true,
        axisX: {
            showGrid: false
        },
        axisY: {
            labelInterpolationFnc: function (value) {
                return (value / 1000) + 'k';
            }
        },
        plugins: [
            Chartist.plugins.tooltip({
                appendToBody: true
            }),
        ]
    }).on('draw', function (data) {
        if (data.type === 'bar') {
            data.element.attr({
                style: 'stroke-width: 30px'
            });
        }
    });


    // horizontal bar chart
    var dataHorizontalBar = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        series: [
            [5, 4, 3, 7, 5, 10, 3],
            [3, 2, 9, 5, 4, 6, 4]
        ]
    };
    new Chartist.Bar('#horizontalbar-chart', dataHorizontalBar, {
        height: "270px",
        seriesBarDistance: 15,
        reverseData: true,
        horizontalBars: true,
        axisY: {
            offset: 75
        }
    });
});
