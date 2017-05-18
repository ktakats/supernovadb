$("#id_plotbutton").on("click", function(){
  var idlist=getSelectValues('selection');
  var url=window.location.pathname + "query/";
  $.get(url, {'ids': idlist}, function(data){
    data=JSON.parse(data);
    plotSpectrum(data);
  });

  if($(".SP").is(":visible")){
    $(".SP").hide();
    $(this).text("Plot spectra");
  }
  else{
    $(".SP").show();
    $(this).text("Hide spectra");
  }
})

function toggle(source) {
        checkboxes = document.getElementsByName('selection');
        for(var i in checkboxes)
            checkboxes[i].checked = source.checked;
};

function getSelectValues(checkboxName) {
  var checkboxes = document.querySelectorAll('input[name="' + checkboxName + '"]:checked'), values = [];
    Array.prototype.forEach.call(checkboxes, function(el) {
        values.push(el.value);
    });
    return values;
};

//Plot spectra
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

 /* define line*/
  var spectrumline = d3.line()
      .x(function(d) { return xScale(d.wavelength) + margin.left; })
      .y(function(d) { return yScale(d.flux)+margin.top; });

 /*add tooltip div*/
  var tip=d3.select(".SP").append("div")
      .attr("class", "tooltip");

  /*Define brush*/
  var brush=d3.brush().on("end", brushended),
      idleTimeout,
      idleDelay=350;

  /*add svg*/
  var canvas=d3.select(".SP").append("svg")
    .attr("class", "plot")
    .attr("width", width+margin.right+margin.left)
    .attr("height", height+margin.top+margin.bottom);


  /*Add clip-path, so the lines do not go out of the margins*/
  var clip = canvas.append("defs").append("clipPath")
     .attr("id", "clipBox");

  canvas.append('rect') // outline for reference
    .attr('x', margin.left)
    .attr('y', margin.top)
    .attr("width", width)
    .attr("height", height)
    .attr("id", "xSliceBox")
    .attr("fill", "white")

  clip.append("use").attr("xlink:href", "#xSliceBox");


  /*add brush g*/
  canvas.append("g")
    .attr("class", "brush")
    .call(brush)


  /*plot data*/
  var g=canvas.append("g")
  data.forEach(function(dat,i){
    g.append("path")
       .data([dat.spectrum])
       .attr("class", "line")
       .attr("d", spectrumline)
       .attr("clip-path", "url(#clipBox)")
       .attr("stroke", function(d){return colors(i)})
       .attr("stroke-width", "2px")
       .attr("fill", "none")
       .on("mouseover", function(d){
           var l=d3.select(this);
           l.transition()
            .delay(300)
            .attr("stroke-width", "4px")
           tip.transition()
            .delay(300)
            .style("opacity", 0.8)
           tip.html("<span>MJD: "+dat.MJD + "</span>")
            .style("left", d3.event.pageX + "px")
            .style("top", d3.event.pageY -80 +"px")
            .style("font-size", "1.2em")
         })
       .on("mouseout", function(d){
           var l=d3.select(this);
           l.transition()
            .delay(100)
            .attr("stroke-width", "2px")
           tip.transition()
            .delay(100)
            .style("opacity", 0)
         })
    });

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

  // add labels

  canvas.select(".x-axis")
      .append("text")
      .text("Wavelength")
      .attr("text-anchor", "middle")
      .attr("dx", (width)/2)
      .attr("dy", margin.bottom*0.8)
      .style("fill", "black")


  canvas.select(".y-axis")
    .append("text")
    .text("Log10(Flux)")
    .attr("text-anchor", "middle")
    .attr("dx", -height/2)
    .attr("dy", -margin.left*0.7)
    .attr("transform", "rotate(-90)")
    .style("fill", "black")

/*Functions*/
  function brushended(){
      s=d3.event.selection;
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
        canvas.selectAll(".line").transition(t)
          .attr("d", function(d){return spectrumline(d)})
    }

};
