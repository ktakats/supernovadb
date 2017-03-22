function plotCurve(indata){

  var data=indata.data;
  /*var data=dat.slice(0,5)
  data[0]["mag_error"]=1.5
  console.log(data[0]["mag_error"])*/
  //Remove previous plot from div
  d3.selectAll('.LC svg').remove();

  var width=600;
  var height=400;
  var margin={top: 50, bottom:50, left: 60, right: 60};

  var x0=[d3.min(data, function(d){return d.MJD})-10, d3.max(data, function(d){return d.MJD;})+10];
  var y0=[d3.min(data, function(d){return d.magnitude})-2, d3.max(data, function(d){return d.magnitude})+2];


  var yScale=d3.scaleLinear()
  .domain(y0)
  .range([0, height]);


  var xScale=d3.scaleLinear()
    .domain(x0)
    .range([0, width]);

  var eb = errorBar()
              .oldXScale(xScale)
              .xScale(xScale)
              .oldYScale(yScale)
              .yScale(yScale)
              .yValue(function(d){return d.magnitude})
              .xValue(function(d){return d.MJD})
              .xError(function(d){return null})
              .yError(function(d){return d.mag_error});



  var canvas=d3.select(".LC").append("svg")
    .attr("class", "plot")
    .attr("width", width+margin.right+margin.left)
    .attr("height", height+margin.top+margin.bottom);



    var tip=d3.select(".LC").append("div")
    .attr("class", "tooltip");

    var brush=d3.brush().on("end", brushended),
        idleTimeout,
        idleDelay=350;

    var gbrush=canvas.append("g")
      .attr("class", "brush")
      .call(brush);

      var errorline = d3.line()
        .x(function(d) { return yScale(d.magnitude-d.mag_error); })
        .y(function(d) { return yScale(d.magnitude+d.mag_error); });
    //data plotting

    var d=gbrush.selectAll("g")
      .data(data)
    var dEnter=d.enter().append("g")

    dEnter.append("path")
      .attr("d", function(d){
        var x1=xScale(d.MJD)+margin.left;
        var y1=yScale(d.magnitude-d.mag_error)+margin.top;
        var x2=xScale(d.MJD)+margin.left;
        var y2=yScale(d.magnitude+d.mag_error)+margin.top;
        return "M"+x1+","+y1 + " L"+ x2+ ","+ y2})
      .style("stroke", function(d){
        if(d.Filter=="B"){return "#4D4A4A"}
        else if(d.Filter=="V"){return "#F53D53"}
        else if(d.Filter=="R"){return "#20AB2C"}
        else{return "#4648F0"}
      })
      .style("stroke-width", "1px")

    dEnter.append("path")
      .attr("d", function(d){
        var x1=xScale(d.MJD)-5+margin.left;
        var y1=yScale(d.magnitude-d.mag_error)+margin.top;
        var x2=xScale(d.MJD)+5+margin.left;
        var y2=yScale(d.magnitude-d.mag_error)+margin.top;
        return "M"+x1+","+y1 + " L"+ x2+ ","+ y2})
      .style("stroke", function(d){
        if(d.Filter=="B"){return "#4D4A4A"}
        else if(d.Filter=="V"){return "#F53D53"}
        else if(d.Filter=="R"){return "#20AB2C"}
        else{return "#4648F0"}
      })
      .style("stroke-width", "1px")

      dEnter.append("path")
        .attr("d", function(d){
          var x1=xScale(d.MJD)-5+margin.left;
          var y1=yScale(d.magnitude+d.mag_error)+margin.top;
          var x2=xScale(d.MJD)+5+margin.left;
          var y2=yScale(d.magnitude+d.mag_error)+margin.top;
          return "M"+x1+","+y1 + " L"+ x2+ ","+ y2})
        .style("stroke", function(d){
          if(d.Filter=="B"){return "#4D4A4A"}
          else if(d.Filter=="V"){return "#F53D53"}
          else if(d.Filter=="R"){return "#20AB2C"}
          else{return "#4648F0"}
        })
        .style("stroke-width", "1px")


    dEnter.append("circle")
          .attr("cx", function(d){return xScale(d.MJD)+margin.left})
          .attr("cy", function(d){return yScale(d.magnitude)+margin.top })
          .attr("r", 6)
          .attr("fill", function(d){
            if(d.Filter=="B"){return "#4D4A4A"}
            else if(d.Filter=="V"){return "#F53D53"}
            else if(d.Filter=="R"){return "#20AB2C"}
            else{return "#4648F0"}
          })
        .on("mouseover", function(d){
          var circ=d3.select(this);
          circ.attr("class", "mouseover");
          circ.transition()
            .delay(100)
            .attr("r", 10)
          tip.transition()
            .delay(100)
            .style("opacity", 0.8);
          tip.html("<span>MJD: "+ d.MJD+"</span> </br> <span>Filter: " + d.Filter+"</span> </br> <span>Mag: " + d.magnitude + "+-" + d.mag_error +"</span> ")
            .style("left", d3.event.pageX + "px")
            .style("top", d3.event.pageY -80 +"px")
            .style("font-size", "1.2em")
          })
        .on("mouseout", function(d){
            var circ=d3.select(this);
            circ.attr("class", "mouseout")
            circ.transition()
              .delay(100)
              .attr("r", 6)
            tip.transition()
              .delay(100)
              .style("opacity", 0)
          })




        /*  d.selectAll("path")
          .data(data)
          .enter()
          .append("path")
          .attr("d", function(d){console.log(d.MJD); return "M"+xScale(d.MJD)+","+yScale(15)+"L"+xScale(55052)+","+yScale(16)})
          .style("stroke-width", "1px")
          .style("stroke", "black")*/






      // add axes
   var axisheight=height+margin.top;
   var axiswidth=margin.left;
   var xAxis=d3.axisBottom(xScale);
   var yAxis=d3.axisLeft(yScale)


   canvas.append("g")
     .call(xAxis)
     .attr("class", "x-axis")
     .attr("transform", "translate("+margin.left+","+axisheight +")");

     canvas.append("g")
       .call(yAxis)
       .attr("class", "y-axis")
       .attr("transform", "translate("+margin.left+","+margin.top+")");

  function brushended(){
    var s = d3.event.selection;
    if (!s){
      if (!idleTimeout) {return idleTimeout = setTimeout(idled, idleDelay);}
      xScale.domain(x0);
      yScale.domain(y0);
    }
    else{
      xScale.domain([s[0][0]-margin.left, s[1][0]-margin.left].map(xScale.invert,xScale))
      yScale.domain([s[0][1]-margin.top, s[1][1]-margin.top].map(yScale.invert,yScale))
      canvas.select(".brush").call(brush.move, null);
    }
    zoom();
  }

  function idled(){
    idleTimeout=null;
  }

  function zoom(){
    var t = canvas.transition().duration(750);
    canvas.select(".x-axis").transition(t).call(xAxis);
    canvas.select(".y-axis").transition(t).call(yAxis);
    canvas.selectAll("circle").transition(t)
      .attr("cx", function(d) {
        var p= xScale(d.MJD)+margin.left;
        if (p<margin.left){return p-margin.left}
        else if (p>width+margin.left){return p+margin.right}
        else{return p}
        })
      .attr("cy", function(d) {
        var p=yScale(d.magnitude)+margin.top;
        if(p>height+margin.bottom){return p+margin.top}
        else if(p<margin.bottom){return p-margin.bottom}
        else{return p;}
        });
  };
};
