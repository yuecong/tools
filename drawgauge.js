function drawGauge_hit() {
  var gauge_hit = new google.visualization.Gauge(document.getElementById('data_hit_ratio_gauge'));
  var options_hit = {
    width: 400, height: 140,
    redFrom: 0, redTo: 25,
    yellowFrom:25, yellowTo: 50,
    minorTicks: 5
  };
  var hit_5m=0,hit_1h=0;
  if (data_hit_ratio_5m.length > 0) hit_5m = Math.floor(data_hit_ratio_5m[0].value);
  if (data_hit_ratio_1h.length > 0) hit_1h = Math.floor(data_hit_ratio_1h[0].value);
  var data_hit= google.visualization.arrayToDataTable([
               ['Label', 'Value'],
               ['5min hit(%)', hit_5m],
               ['1hour hit(%) ', hit_1h]
              ]);
  gauge_hit.draw(data_hit, options_hit);    
}
function drawGauge_cpu_mem(Jsondata) {
 var gauge_cpu_mem = new google.visualization.Gauge(document.getElementById('cpu_mem_info'));
  var options_cpu_mem = {
    width: 400, height: 140,
    redFrom: 80, redTo: 100,
    yellowFrom:60, yellowTo: 80,
    minorTicks: 5
  };
  var cpu_percent = Jsondata.hits.hits[0]._source.cpu;
  var mem_percent = Jsondata.hits.hits[0]._source.memory;
  var data_cpu_mem= google.visualization.arrayToDataTable([
              ['Label', 'Value'],
               ['CPU(%)', cpu_percent],
               ['Mem(%)', mem_percent]
              ]);
  gauge_cpu_mem.draw(data_cpu_mem, options_cpu_mem); 
}
function drawGauge_network(Jsondata) {
 var gauge_network = new google.visualization.Gauge(document.getElementById('network_info'));
  var options_network = {
    width: 400, height: 140,
    redFrom: 60, redTo: 100,
    yellowFrom:40, yellowTo: 60,
    minorTicks: 5
  };
  var sent_MBps = Jsondata.hits.hits[0]._source.Bps_sent / (1000.0*1000.0);
  var recv_MBps = Jsondata.hits.hits[0]._source.Bps_rcv  / (1000.0*1000.0);
  var data_network= google.visualization.arrayToDataTable([
              ['Label', 'Value'],
               ['Sent(MBps)', sent_MBps],
               ['Recv(MBps)', recv_MBps]
              ]);
  gauge_network.draw(data_network, options_network); 
}
function drawSysInfo() {
  d3.json("sysinfo.json", function(err,Jsondata) {
    drawGauge_cpu_mem(Jsondata);
    drawGauge_network(Jsondata);
  });
}
setInterval(function() {
    drawSysInfo();
  }, 1000*5);