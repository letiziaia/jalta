

Plotly.d3.csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv", function(err, rows){

    function unpack(rows, key) {
    return rows.map(function(row) { return row[key]; });
  }
  
  var d = JSON.parse(document.getElementById('seasonal').attributes[1].value);
  
  var data = [{
    type: "scatter",
    mode: "lines",
    name: 'Total sales',
    x: d['x'],
    y: d['y'],
    line: {color: '#17BECF'}
  }]


  
  var layout = {
    title: 'Total sales per day',
    xaxis: {
      autorange: true,
      rangeselector: {buttons: [
          {
            count: 1,
            label: '1m',
            step: 'month',
            stepmode: 'backward'
          },
          {
            count: 6,
            label: '6m',
            step: 'month',
            stepmode: 'backward'
          },
          {step: 'all'}
        ]},
      rangeslider: {},
      type: 'date'
    },
    yaxis: {
      autorange: true,
      type: 'linear'
    }
  };
  
  Plotly.newPlot('seasonal', data, layout);
  })  