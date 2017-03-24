function plotSpectrum(indata){
  data=indata.data;
  d3.selectAll('.SP svg').remove();

  /*dimensions*/
  var width=600;
  var height=400;
  var margin={top: 50, bottom:50, left: 60, right: 60};

  /*Default x and y range*/
  var x0=[d3.min(data, function(d){return d3.min(d.spectrum, function(s){return s.wavelength})})-500, d3.max(data, function(d){return d3.max(d.spectrum, function(s){return s.wavelength});})+500];
  var y0=[d3.max(data, function(d){return d3.max(d.spectrum, function(s){return s.flux})})+2, d3.min(data, function(d){return d3.min(d.spectrum, function(s){return s.flux;});})-2]



  /*Scales*/
  var yScale=d3.scaleLinear()
  .domain(y0)
  .range([0, height]);

  var xScale=d3.scaleLinear()
    .domain(x0)
    .range([0, width]);

    var colors=d3.scaleSequential()
      .domain([0,data.length])
      .interpolator(d3.interpolateRainbow);

    var valueline = d3.line()
      .x(function(d) { return xScale(d.wavelength) + margin.left; })
      .y(function(d) { return yScale(d.flux)+margin.top; });

    var tip=d3.select(".SP").append("div")
        .attr("class", "tooltip");

    /*add svg*/
    var canvas=d3.select(".SP").append("svg")
      .attr("class", "plot")
      .attr("width", width+margin.right+margin.left)
      .attr("height", height+margin.top+margin.bottom);


    data.forEach(function(dat,i){
      canvas.append("path")
         .data([dat.spectrum])
         .attr("class", "line")
         .attr("d", valueline)
         .attr("stroke", function(d){return colors(i)})
         .attr("stroke-width", "2px")
         .attr("fill", "none")
         .on("mouseover", function(d){
           var l=d3.select(this);
           l.attr("class", "mouseover");
           l.transition()
            .delay(100)
            .attr("stroke-width", "4px")
           tip.transition()
            .delay(100)
            .style("opacity", 0.8)
           tip.html("<span>MJD: "+dat.MJD + "</span>")
            .style("left", d3.event.pageX + "px")
            .style("top", d3.event.pageY -80 +"px")
            .style("font-size", "1.2em")
         })
         .on("mouseout", function(d){
           var l=d3.select(this);
           l.attr("class", "mouseout");
           l.transition()
            .delay(100)
            .attr("stroke-width", "2px")
           tip.transition()
            .delay(100)
            .style("opacity", 0)
         })
    })

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


}
