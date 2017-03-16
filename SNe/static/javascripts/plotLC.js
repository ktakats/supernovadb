function plotCurve(indata){

  var data=indata.data;
  //Remove previous plot from div
  d3.selectAll('.LC svg').remove();

  var width=500;
  var height=300;
  var margin={top: 100, bottom:50, left: 60, right: 60};

  var yScale=d3.scaleLinear()
  .domain([d3.min(data, function(d){return d.magnitude})-2, d3.max(data, function(d){return d.magnitude})+2])
  .range([0, height]);


  var xScale=d3.scaleLinear()
    .domain([d3.min(data, function(d){return d.MJD})-10, d3.max(data, function(d){return d.MJD;})+10])
    .range([0, width]);





    var canvas=d3.select(".LC").append("svg")
    .attr("class", "plot")
    .attr("width", width+margin.right+margin.left)
    .attr("height", height+margin.top+margin.bottom);

    var tip=d3.select(".LC").append("div")
    .attr("class", "tooltip");

    //data plotting
    canvas.selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
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
          .delay(200)
          .attr("r", 10)
        tip.transition()
          .delay(200)
          .style("opacity", 0.8);
        tip.html("<span>MJD: "+ d.MJD+"</span> </br> <span>Filter: " + d.Filter+"</span> </br> <span>Mag: " + d.magnitude + "+-" + d.mag_error +"</span> ")
          .style({"right": "550px", "top": "50px", "font-size": "1em"})
        })
    .on("mouseout", function(d){
      var circ=d3.select(this);
      circ.attr("class", "mouseout")
      circ.transition()
        .delay(200)
        .attr("r", 6)
      tip.transition()
        .delay(1000)
        .style("opacity", 0)
      });

      // add axes
   var axisheight=height+margin.top;
   var axiswidth=margin.left;

   canvas.append("g")
     .call(d3.axisBottom(xScale))
     .attr("class", "x axis")
     .attr("transform", "translate("+margin.left+","+axisheight +")");

     canvas.append("g")
       .call(d3.axisLeft(yScale))
       .attr("class", "y axis")
       .attr("transform", "translate("+margin.left+","+margin.top+")");


  /*     // add legend
  canvas.append("circle")
    .attr("cx", xScale(55080))
    .attr("cy", yScale(22))
    .attr("r",6)
    .attr("fill", "#F53D53")

  canvas.append("text")
    .text("B")
    .attr("x", xScale(55085))
    .attr("y", yScale(22))

  canvas.append("circle")
    .attr("cx", xScale(55080))
    .attr("cy", yScale(23))
    .attr("r",6)
    .attr("fill", "#4D4A4A")

  canvas.append("text")
    .text("V")
    .attr("x", xScale(55085))
    .attr("y", yScale(23))
*/
};
