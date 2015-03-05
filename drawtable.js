var cachemissurl_data =null;
var requesturl_data =null;

function drawTopRequestTable(json_tableData) {
   if (requesturl_data == null) {
    requesturl_data =new google.visualization.DataTable();
    requesturl_data.addColumn('string', 'Request URL');
    requesturl_data.addColumn('number', 'Access number');
    requesturl_data.addColumn('number', 'cache ratio(avg)(%)');
    requesturl_data.addColumn('number', 'content size(bytes)');
    requesturl_data.addColumn('number', 'respone time(min)(ms)');
    requesturl_data.addColumn('number', 'respone time(avg)(ms)');
    requesturl_data.addColumn('number', 'respone time(max)(ms)');
  } 
  var requesturl_data_table = new google.visualization.Table(document.getElementById('table_toprequesturl'));
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
  requesturl_data_table.draw(requesturl_data, {showRowNumber: true,sort:'false'});
}

function drawTopCacheMissTable(json_tableData) {
  if (cachemissurl_data == null) {
    cachemissurl_data = new google.visualization.DataTable();
    cachemissurl_data.addColumn('string', 'Cache MissURL');
    cachemissurl_data.addColumn('number', 'Access number');
    cachemissurl_data.addColumn('number', 'content size(bytes)');
    cachemissurl_data.addColumn('number', 'respone time(min)(ms)');
    cachemissurl_data.addColumn('number', 'respone time(avg)(ms)');
    cachemissurl_data.addColumn('number', 'respone time(max)(ms)');
  }  
  var cachemissurl_data_table = new google.visualization.Table(document.getElementById('table_topcachemissurl'));
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
  cachemissurl_data_table.draw(cachemissurl_data, {showRowNumber: true,sort:'false'});
}

function drawTableData(){
  d3.json("toprequestURL.json", function(err,Jsondata) { drawTopRequestTable(Jsondata);});
  d3.json("topchachemissURL.json", function(err,Jsondata) {drawTopCacheMissTable(Jsondata);});
}

setInterval(function() {
    drawTableData();
  }, 1000*5);
