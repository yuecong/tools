google.load("visualization", "1", {packages:["table"]});
google.setOnLoadCallback(drawTopRequestTable);
google.setOnLoadCallback(drawTopCacheMissTable);
var cachemissurl_data = new google.visualization.DataTable();
var requesturl_data = new google.visualization.DataTable();

requesturl_data.addColumn('string', 'Request URL');
requesturl_data.addColumn('number', 'Access number');
requesturl_data.addColumn('number', 'cache ratio(avg)(%)');
requesturl_data.addColumn('number', 'content size(bytes)');
requesturl_data.addColumn('number', 'respone time(min)(ms)');
requesturl_data.addColumn('number', 'respone time(avg)(ms)');
requesturl_data.addColumn('number', 'respone time(max)(ms)');

cachemissurl_data.addColumn('string', 'Cache MissURL');
cachemissurl_data.addColumn('number', 'Access number');
cachemissurl_data.addColumn('number', 'content size(bytes)');
cachemissurl_data.addColumn('number', 'respone time(min)(ms)');
cachemissurl_data.addColumn('number', 'respone time(avg)(ms)');
cachemissurl_data.addColumn('number', 'respone time(max)(ms)');

drawTopCacheMissTable_falg=0;
drawTopRequestTable_flag=0;
function drawTopCacheMissTable() {
  var cachemissurl_data_table = new google.visualization.Table(document.getElementById('table_topcachemissurl'));
  cachemissurl_data_table.draw(cachemissurl_data, {showRowNumber: true,sort:'false'});
  drawTopCacheMissTable_falg=1;
}

function drawTopRequestTable() {
  var requesturl_data_table = new google.visualization.Table(document.getElementById('table_toprequesturl'));
  requesturl_data_table.draw(requesturl_data, {showRowNumber: true,sort:'false'});
  drawTopRequestTable_flag=1;
}
function setRequestURLTableData(json_tableData) {
  num_rows = requesturl_data.getNumberOfRows();
  requesturl_data.removeRows(0,num_rows);
  dataSet_top_request_URL = json_tableData.aggregations.top_request_URL.buckets;
  dataSet_top_request_URL.forEach(function(d) {
     requesturl_data.addRow([ d.key, //Request URL
                             +d.doc_count, //Access number
                             +Math.round(d.cache_ratio.value*10000)/100, //Hit ratio
                             +Math.round(d.contentSize.value), //content size
                             +d.spentTime_stats.min, //access time(min)
                             +d.spentTime_stats.max, //access time(max)
                             +Math.round(d.spentTime_stats.avg) //access time(avg)
                             ]);
  });

}
function setCacheMissURLTableData(json_tableData) {
  num_rows = cachemissurl_data.getNumberOfRows();
  cachemissurl_data.removeRows(0,num_rows);
  dataSet_top_cachemiss_URL = json_tableData.aggregations.top_request_URL.buckets;
  dataSet_top_cachemiss_URL.forEach(function(d) {
     cachemissurl_data.addRow([ d.key, //Request URL
                             +d.doc_count, //Access number
                             +Math.round(d.contentSize.value), //content size
                             +d.spentTime_stats.min, //access time(min)
                             +d.spentTime_stats.max, //access time(max)
                             +Math.round(d.spentTime_stats.avg) //access time(avg)
                             ]);
  });
}

function drawTableData(){
  d3.json("toprequestURL.json", function(err,Jsondata) {
    setRequestURLTableData(Jsondata);
    if (drawTopRequestTable_flag>0) drawTopRequestTable(); //make sure all initilization of google chart library is ready.
  });
  d3.json("topchachemissURL.json", function(err,Jsondata) {
    setCacheMissURLTableData(Jsondata);
    if (drawTopCacheMissTable_falg>0) drawTopCacheMissTable(); //make sure all initilization of google chart library is ready.
  });
}

drawTableData();
setInterval(function() {
    drawTableData();
  }, 1000*20);
