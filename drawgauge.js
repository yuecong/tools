
google.load("visualization", "1", {packages:["gauge"]});
google.setOnLoadCallback(drawGauge);
var gauge_data_hit,hit_5m=0,hit_1h=0;

function drawGauge() {
  var data_hit,data_cpu;
  var options_hit = {
    width: 400, height: 140,
    redFrom: 0, redTo: 25,
    yellowFrom:25, yellowTo: 50,
    minorTicks: 5
  };
  var options_cpu = {
    width: 600, height: 140,
    redFrom: 80, redTo: 100,
    yellowFrom:60, yellowTo: 80,
    minorTicks: 5
  };
  var chart_hit,chart_cpu;
  gauge_data_hit= [['Label', 'Value'],
               ['5min hit', hit_5m],
               ['1hour hit ', hit_1h]
              ];
  gauge_data_cpu= [['Label', 'Value'],
               ['CPU ', 30],
               ['Memmory', 50],
               ['Network', 10]
              ];
  chart_hit = new google.visualization.Gauge(document.getElementById('data_hit_ratio_gauge'));
  chart_cpu = new google.visualization.Gauge(document.getElementById('cpu_info'));
  data_hit = google.visualization.arrayToDataTable(gauge_data_hit);
  data_cpu = google.visualization.arrayToDataTable(gauge_data_cpu);
  chart_hit.draw(data_hit, options_hit);
  chart_cpu.draw(data_cpu, options_cpu);
}

setInterval(function() {
    drawGauge();
  }, 5000);