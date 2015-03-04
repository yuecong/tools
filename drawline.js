//data will be used for scale and Unit, data1 will only be used for drawing for simple implementation
function drawNewLineChart(chartInfo,data,data1,isUpdate) {
/*var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
    */
    var aa = chartInfo.margin.top;

    var margin = chartInfo.margin,
    width = chartInfo.position.width - margin.left - margin.right,
    height = chartInfo.position.height - margin.top - margin.bottom;

    var x = d3.time.scale()
    .range([0, width]);

    var y = d3.scale.linear()
    .range([height, 0]);

    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

    var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });

    var svg,g_xaxis,g_yaxis,g_path_line,g_path_line1;
    var domain_data;
  if (isUpdate == false)  { //create new document
    svg = d3.select("#chart_container").append("svg")
    .attr("id",chartInfo.name)
    .attr("width", (width + margin.left + margin.right) +"px")
    .attr("height", (height + margin.top + margin.bottom)+"px")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    //Title
    svg.append("text")
    .attr("x",width/2)
    .style("text-anchor", "middle")
    .style("font","bold 16px Verdana, Helvetica, Arial, sans-serif")
    .text(chartInfo.title.title)    
  } else {
    svg = d3.select("#"+chartInfo.name);
  }
  domain_data =data
  if (data1) { //Add data and data1 into one array
    domain_data= data.concat(data1);
  }
  x_max = d3.max(domain_data, function(d) { return d.date; });
  x_min = new Date();
  x_min.setTime(x_max.getTime() - chartInfo.timeTicks*10*60*1000); // 10 ticks per indicated intervals
  x.domain([x_min,x_max]);
  
  y_max = d3.max(domain_data, function(d) { return d.value; });
  y.domain([0,y_max*1.2]);
  if (isUpdate == false) {
    g_xaxis = svg.append("g");
    g_yaxis = svg.append("g");
    g_path_line = svg.append("path");
  } else {
    g_xaxis=svg.select("#xAxis_"+chartInfo.name);
    g_yaxis=svg.select("#yAxis_"+chartInfo.name);
    g_path_line = svg.selectAll("#data_"+chartInfo.name);
  }
  g_xaxis
  .attr("class", "x axis")
  .attr("id","xAxis_"+chartInfo.name)
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis)
  if (isUpdate == false) {
    g_xaxis
    .append("text")
    .attr("x", width + 6)
    .attr("y", -6)
    .style("text-anchor", "end")
    .text(chartInfo.title.xAxis);
  }
  //Y Axis
  g_yaxis
  .attr("class", "y axis")
  .attr("id","yAxis_"+chartInfo.name)
  .call(yAxis)
  if (isUpdate == false) {
    g_yaxis
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text(chartInfo.title.yAxis);
  }
  g_path_line
  .attr("id","data_"+chartInfo.name)
  .datum(data)
  .attr("class", "line")
  .attr("d", line);

  if (data1) {
    if (isUpdate == false) {
      g_path_line1 = svg.append("path") 
    }  else {
      g_path_line1 = svg.select("#data1_"+chartInfo.name)
    }
    g_path_line1
    .attr("id","data1_"+chartInfo.name)
    .datum(data1)
    .attr("class", "line1")
    .attr("d", line);
  }
}

chart_hit_ratio_5m= {
  "margin" : {"top" : 20,"right" : 20,"bottom" : 30,"left" : 30},
  "position" : {"x" : 480,"y" : 0,"width" : 480,"height" : 250 },
  "title": {"xAxis": "Time","yAxis":"Hit Ratio(%)","title":"Cache Hit Ratio(5 minutes avarage)"},
  "name": "chart_hit_ratio_5m",
  "timeTicks" : 5
}
chart_access_5m= {
  "margin" : {"top" : 20,"right" : 20,"bottom" : 30,"left" : 40},
  "position" : {"x" : 480,"y" : 0,"width" : 480,"height" : 250 },
  "title": {"xAxis": "Time","yAxis":"Access(Times)","title":"Access Number(5 minutes avarage)"},
  "name": "chart_access_5m",
  "timeTicks" : 5
}
chart_request_size_5m= {
  "margin" : {"top" : 20,"right" : 20,"bottom" : 30,"left" : 40},
  "position" : {"x" : 480,"y" : 0,"width" : 480,"height" : 250 },
  "title": {"xAxis": "Time","yAxis":"Content Size(MB)","title":"Content Size(5 minutes avarage)"},
  "name": "chart_request_size_5m",
  "timeTicks" : 5
}
chart_hit_ratio_1h= {
  "margin" : {"top" : 20,"right" : 20,"bottom" : 30,"left" : 30},
  "position" : {"x" : 480,"y" : 0,"width" : 480,"height" : 250 },
  "title": {"xAxis": "Time","yAxis":"Hit Ratio(%)","title":"Cache Hit Ratio(1 hour avarage)"},
  "name": "chart_hit_ratio_1h",
  "timeTicks" : 60 // 60 minutes
}
chart_access_1h= {
  "margin" : {"top" : 20,"right" : 20,"bottom" : 30,"left" : 40},
  "position" : {"x" : 480,"y" : 0,"width" : 480,"height" : 250 },
  "title": {"xAxis": "Time","yAxis":"Access(Times)","title":"Access Number(1 hour avarage)"},
  "name": "chart_access_1h",
  "timeTicks" : 60 // 60 minutes
}
chart_request_size_1h= {
  "margin" : {"top" : 20,"right" : 20,"bottom" : 30,"left" : 40},
  "position" : {"x" : 480,"y" : 0,"width" : 480,"height" : 250 },
  "title": {"xAxis": "Time","yAxis":"Content Size(GB)","title":"Content Size(1 hour avarage)"},
  "name": "chart_request_size_1h",
  "timeTicks" : 60 // 60 minutes
}


var data_hit_ratio_5m=[];
var data_access_5m=[];
var data_access_hit_5m=[]; 
var data_request_size_hit_5m=[];
var data_request_size_5m=[];

var data_hit_ratio_1h=[];
var data_access_1h=[];
var data_access_hit_1h=[]; 
var data_request_size_hit_1h=[];
var data_request_size_1h=[]; 


function getData(Jsondata){
  var cnt =0;
  var MAX_DATA_NUM = 10;  
  var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S.%LZ").parse;

  //Clean all array with setting their length to be 0
  data_hit_ratio_5m.length =0;
  data_access_5m.length =0;
  data_access_hit_5m.length =0;
  data_request_size_hit_5m.length =0;
  data_request_size_5m.length =0;
  data_hit_ratio_1h.length =0;
  data_access_1h.length =0;
  data_access_hit_1h.length =0;
  data_request_size_hit_1h.length =0;
  data_request_size_1h.length =0;

  //5 Minutes data retrive
  dataSet_5m = Jsondata.aggregations.accessTime_5m.buckets;
  dataSet_5m.forEach(function(d) {
    if (cnt < MAX_DATA_NUM) {
        //data_hit_ratio_5m  Cache hit ratio per 5 minutes
        data_hit_ratio_5m.push({"date":parseDate(d.key_as_string),"value":+d.hit_ratio.value*100});
        //data_access_5m total access number per 5 minutes
        data_access_5m.push({"date":parseDate(d.key_as_string),"value":+d.doc_count});
        //hit access number per 5 minutes
        dataSet_5m_size_access = d.size_access_info.buckets ;
        request_size_cache_hit_5m_tmp_val =0.0;
        data_access_hit_5m_tmp_val=0;
        request_size_5m_tmp_val=0;
        dataSet_5m_size_access.forEach(function(dd) {
          if  ( dd.key == 1) {
            //in case of cache hit happen
            data_access_hit_5m_tmp_val +=dd.doc_count;
            request_size_cache_hit_5m_tmp_val = +dd.sum_cache_size.value/1000.0/1000.0;
          } 
          if  ( dd.key == 0) {
            request_size_5m_tmp_val = request_size_cache_hit_5m_tmp_val + (dd.sum_cache_size.value/1000.0/1000.0);
          }
        });
        data_access_hit_5m.push({"date":parseDate(d.key_as_string),"value": data_access_hit_5m_tmp_val});
        data_request_size_hit_5m.push({"date":parseDate(d.key_as_string),"value":request_size_cache_hit_5m_tmp_val});
        data_request_size_5m.push({"date":parseDate(d.key_as_string),"value":request_size_5m_tmp_val});
      }
      cnt++;
    }
    );
  //1 Hour data retrive  
  cnt =0;
  dataSet_1h = Jsondata.aggregations.accessTime_1h.buckets;
  dataSet_1h.forEach(function(d) {
    if (cnt < MAX_DATA_NUM) {
        //data_hit_ratio_1h  Cache hit ratio per 1 hour
        data_hit_ratio_1h.push({"date":parseDate(d.key_as_string),"value":+d.hit_ratio.value*100});
        //data_access_1h total access number per 1 hour
        data_access_1h.push({"date":parseDate(d.key_as_string),"value":+d.doc_count});
        //hit access number per hour
        dataSet_1h_size_access = d.size_access_info.buckets ;
        request_size_cache_hit_1h_tmp_val =0.0;
        data_access_hit_1h_tmp_val=0;
        request_size_1h_tmp_val=0;
        dataSet_1h_size_access.forEach(function(dd) {
          if  ( dd.key == 1) {
            //in case of cache hit happen
            data_access_hit_1h_tmp_val +=dd.doc_count;
            request_size_cache_hit_1h_tmp_val = +dd.sum_cache_size.value/1000.0/1000.0/1000.0;
          } 
          if  ( dd.key == 0) {
            request_size_1h_tmp_val = request_size_cache_hit_1h_tmp_val + (dd.sum_cache_size.value/1000.0/1000.0/1000.0);
          }
        });
        data_access_hit_1h.push({"date":parseDate(d.key_as_string),"value": data_access_hit_1h_tmp_val});
        data_request_size_hit_1h.push({"date":parseDate(d.key_as_string),"value":request_size_cache_hit_1h_tmp_val});
        data_request_size_1h.push({"date":parseDate(d.key_as_string),"value":request_size_1h_tmp_val});
      }
      cnt++;
    }
    );
}

start_time_chart =Date.now();
tmp_cnt_chart=0;
enable_update_flag_chart =1;

function drawChartData(){
  if (enable_update_flag_chart == 0) return;
  if ((Date.now() - start_time_chart < 5 * 1000) && (tmp_cnt_chart >0)) return;
  isUpdate = false;
  if (tmp_cnt_chart >0) isUpdate = true;
  d3.json("cache_info1.json", function(err,Jsondata) {
    getData(Jsondata);
    //for gauge drawing
    if (data_hit_ratio_5m.length > 0) hit_5m = Math.floor(data_hit_ratio_5m[0].value);
    if (data_hit_ratio_1h.length > 0) hit_1h = Math.floor(data_hit_ratio_1h[0].value);
    //5 minutes chart
    drawNewLineChart(chart_hit_ratio_5m,data_hit_ratio_5m,null,isUpdate);
    drawNewLineChart(chart_access_5m,data_access_5m,data_access_hit_5m,isUpdate); 
    drawNewLineChart(chart_request_size_5m,data_request_size_5m,data_request_size_hit_5m,isUpdate);
    //1 hour chart
    drawNewLineChart(chart_hit_ratio_1h,data_hit_ratio_1h,null,isUpdate);
    drawNewLineChart(chart_access_1h,data_access_1h,data_access_hit_1h,isUpdate); 
    drawNewLineChart(chart_request_size_1h,data_request_size_1h,data_request_size_hit_1h,isUpdate);
    tmp_cnt_chart++;
    enable_update_flag_chart =1;
    start_time_chart =Date.now();
    });
  enable_update_flag_chart =0;
}

d3.timer(drawChartData);
