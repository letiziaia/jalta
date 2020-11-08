var data=JSON.parse(document.getElementById('topproduct').attributes[1].value);
Highcharts.chart('topproduct', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: `Top ${data["number"]} popular products`
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Top products',
        colorByPoint: true,
        data: data['data']
    }]
});

data = JSON.parse(document.getElementById('byhour').attributes[1].value)['data'];
Highcharts.chart('byhour', {

    chart: {
        type: 'column'
    },

    title: {
        text: 'Total transaction value by hour by weekday'
    },

    xAxis: {
        categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    },

    yAxis: {
        allowDecimals: false,
        min: 0,
        title: {
            text: 'Total amount, euro'
        },
        tickPixelInterval: 10
    },

    tooltip: {
        formatter: function () {
            return '<b>' + this.x + '</b><br/>' +
                this.series.name + ': ' + this.y + '<br/>' +
                'Total: ' + this.point.stackTotal;
        }
    },

    plotOptions: {
        column: {}
    },

    series: data
});

data = JSON.parse(document.getElementById('itemset0').attributes[1].value)['data'];
Highcharts.chart('itemset0', {
    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<h5>{chartTitle}</h5>' +
                '<div>{chartSubtitle}</div>' +
                '<div>{chartLongdesc}</div>' +
                '<div>{viewTableButton}</div>'
        }
    },
    series: [{
        type: 'wordcloud',
        data: data,
        name: 'Occurrences'
    }],
    title: {
        text: ''
    }
});

data = JSON.parse(document.getElementById('itemset1').attributes[1].value)['data'];
Highcharts.chart('itemset1', {
    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<h5>{chartTitle}</h5>' +
                '<div>{chartSubtitle}</div>' +
                '<div>{chartLongdesc}</div>' +
                '<div>{viewTableButton}</div>'
        }
    },
    tooltip: {
        enabled: false
    },
    series: [{
        type: 'wordcloud',
        data: data,
        name: 'Occurrences'
    }],
    title: {
        text: ''
    }
});

data = JSON.parse(document.getElementById('itemset2').attributes[1].value)['data'];
Highcharts.chart('itemset2', {
    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<h5>{chartTitle}</h5>' +
                '<div>{chartSubtitle}</div>' +
                '<div>{chartLongdesc}</div>' +
                '<div>{viewTableButton}</div>'
        }
    },
    series: [{
        type: 'wordcloud',
        data: data,
        name: 'Occurrences'
    }],
    title: {
        text: ''
    }
});