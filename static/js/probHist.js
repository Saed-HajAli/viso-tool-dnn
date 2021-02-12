function ProbHist(model , settings , parent){

   this.settings = new Settings();
  var _self = this;
  this.data = [] ;
  //this.data.push(model.data);
  this.classNames = model.classNames;
  this.newData = [model.histsPreparedData];
  this.histData = []
  this.max = {
    right : model.histsBounds.maxRight,
    left : model.histsBounds.maxLeft
  }


  pane = settings.probPane;

  var x, y, xAxis, yAxis, yAxis2;

  w=(pane.node().getBoundingClientRect().width - 30)/4;
  var margin = {
    top: 20,
    right: 20,
    bottom: 20,
    left: 20
  },

  width = Math.max(198,w) - margin.left - margin.right,
  height = Math.max(200,w) - margin.top - margin.bottom;

  d3.selection.prototype.moveToFront = function() {  
    return this.each(function(){
      this.parentNode.appendChild(this);
    });
  };  

  var tipTP = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<span>Probability:</span> <span>" + d.lowProb + " - " + + d.probability + "</span><br><span>TP:</span> <span>" + d.tp + "</span>";
            })
  var tipFP = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<span>Probability:</span> <span>" + d.lowProb + " - " + + d.probability + "</span><br><span>FP:</span> <span>" + d.fp + "</span>";
            })
  var tipFN = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<span>Probability:</span> <span>" + d.lowProb + " - " + d.probability + "</span><br><span>FN:</span> <span>" + d.fn + "</span>";
            })
  var tipTN = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<span>Probability:</span> <span>" + d.lowProb + " - " + + d.probability + "</span><br><span>TN:</span> <span>" + d.tn + "</span>";
            })

  // prepare bin boundaries acc to no of bins
  this.getBinValues = function(){
      bins = settings.probbins;
      array = [];
      k = (settings.probLimits[1] - settings.probLimits[0])/bins;
      num=0;
      for(i=1;i<=bins;i++){
        num = i*k;
        num = Math.round((settings.probLimits[0] + num) * 100) / 100;
        array.push( num);
      }
      return array;
  }

  // prepare histogram data into bins and assign it to property -> histData[]
  this.prepareData = function(data) {
      // data = this.data;


      for (ii = 0; ii < data.length; ii++)
      {
          classes = this.classNames;
          bins = settings.probbins;
          //this.newData = [];
          newDataTemp = [];
          this.max.right = this.max.left = 0;
          binValues = this.getBinValues();


          for (i = 0, len = classes.length; i < len; i++) {
              name = "L-" + classes[i];
              prob = "P-" + classes[i];

              preparedData = [];
              for (j = 0, lenj = binValues.length; j < lenj; j++) {
                  l = (j == 0) ? (settings.probLimits[0]) : Math.round((binValues[j - 1] + 0.01) * 100) / 100;
                  preparedData.push({
                      name: classes[i],
                      lowProb: l,
                      probability: binValues[j], // upper value for all buckets
                      tn: 0,
                      tp: 0,
                      fn: 0,
                      fp: 0,
                  });
              }
              for (j = 0, lenj = data[ii].length; j < lenj; j++) {
                  for (k = 0, lenk = preparedData.length; k < lenk; k++)
                  {
                      if (data[ii][j][name].toLowerCase() == "tn" && data[ii][j][prob] < settings.probtnFilter) {
                          break;
                      }


                          if (data[ii][j][name].toLowerCase() == "tp" && data[ii][j][prob] > settings.probtpFilter) {
                              break;
                          }

                          if (settings.probDataOptions[data[ii][j][name].toLowerCase()] &&
                              data[ii][j][prob] >= preparedData[k].lowProb && data[ii][j][prob] <= preparedData[k].probability) {
                              preparedData[k][data[ii][j][name].toLowerCase()]++;
                              break;
                          }
                      }
                  }

                  newDataTemp.push(preparedData);
                  this.max.left = Math.max(this.max.left, d3.max(preparedData, function (d) {
                      return (d.tn + d.fn);
                  }));
                  this.max.right = Math.max(this.max.right, d3.max(preparedData, function (d) {
                      return (d.tp + d.fp);
                  }));
                  //console.log("prep: ")
                  //console.log(newDataTemp)
              }
              this.newData.push(newDataTemp);
       }
  }

  // make all probibility histograms
  this.makeHistograms = function(){
    pane = settings.probPane;
    pane.selectAll("*").remove();

    for(ii=0;ii<this.newData.length;ii++)
    {
        this.histData = []
        for(i=0,len=(this.newData[ii]).length; i<len ; i++){
                this.histData[i] = this.newData[ii][i];
        }

        scl = Math.max(this.max.left , this.max.right);
        x = d3.scale.linear()
                .domain([-scl , scl]).nice()
                .rangeRound([0, width]);

        y = d3.scale.ordinal()
                .domain(((this.histData)[0]).map(function(d){ return d.probability;}))
                .rangeRoundBands([height , 0] , 0.1);

        xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .ticks(5)
                    .tickSize(0.3)
                    .tickFormat(function(d){
                      f = Math.abs(d);
                      if(f>=1000) return(Math.round(f/1000) + "K");
                      else return f;
                    });

        yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .tickValues(y.domain().filter(function(d,i){
                      if(i == 0 || i == (settings.probbins-1)) return true;
                      return false;
                    }))
                    .tickSize(0)
                    .tickPadding(3);

        yAxis2 = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .tickFormat("")
                    .tickSize(0.3);

        var svg = pane.selectAll(".svg-probHist")
                  .data(this.histData)
                  .enter().append("svg")
                  .attr("class" , "svg-probHist")
                  .attr("width" , width + margin.left + margin.right)
                  .attr("height" , height + margin.top + margin.bottom)
                  .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        svg.call(tipTP);
        svg.call(tipFP);
        svg.call(tipFN);
        svg.call(tipTN);

        console.log(this.histData);

        svg.append("text")
                  .attr("class" , "class-label")
                  .attr("x" , "0")
                  .attr("y" , -12)
                  .attr("dy" , ".5em")
                  .text(function(d , i){return (d[0].name)});

        var tp = svg.selectAll(".bar-tp")
                  .data(function(d){return d;})
                  .enter().append("rect")
                  .attr("class" , function(d){ return d.name+" bar-tp bar";})
                  .attr("x" , function(d){return x(0);})
                  .attr("y" , function(d){return y(d.probability);})
                  .attr("width" , function(d){return Math.abs(x(d.tp) - x(0));})
                  .attr("height" , function(d){return y.rangeBand()});

        var fp = svg.selectAll(".bar-fp")
                  .data(function(d){return d;})
                  .enter().append("rect")
                  .attr("class" , function(d){return d.name+" bar-fp bar";})
                  .attr("x" , function(d){return x(d.tp);})
                  .attr("y" , function(d){return y(d.probability);})
                  .attr("width" , function(d){return Math.abs(x(d.fp) - x(0));})
                  .attr("height" , function(d){return y.rangeBand()});

        var fn = svg.selectAll(".bar-fn")
                  .data(function(d){return d;})
                  .enter().append("rect")
                  .attr("class" , function(d){return d.name+" bar-fn bar";})
                  .attr("x" , function(d){return x(-d.fn);})
                  .attr("y" , function(d){return y(d.probability);})
                  .attr("width" , function(d){return Math.abs(x(d.fn) - x(0));})
                  .attr("height" , function(d){return y.rangeBand()});

        var tn = svg.selectAll(".bar-tn")
                  .data(function(d){return d;})
                  .enter().append("rect")
                  .attr("class" , function(d){return d.name+" bar-tn bar";})
                  .attr("x" , function(d){return x(-d.fn-d.tn);})
                  .attr("y" , function(d){return y(d.probability);})
                  .attr("width" , function(d){return Math.abs(x(d.tn) - x(0));})
                  .attr("height" , function(d){return y.rangeBand()});

        svg.append("g")
          .attr("class" , "x axis")
          .attr("transform" , "translate(0," + height + ")")
          .call(xAxis);

        svg.append("g")
          .attr("class" , "y axis")
          .attr("transform" , "translate(0,0)")
          .call(yAxis);

        svg.append("g")
          .attr("class" , "y axis2")
          .attr("transform" , "translate(" + x(0) +",0)")
          .call(yAxis2);
    }
    
  }
  
  this.bindEvents = function() {

      d3.selectAll(".bar-tp")      
        .on('mouseover', tipTP.show)
        .on('mouseout', tipTP.hide)
        .on("click" , function(){
          if(!(d3.select(this).classed("filled-gray"))){
            obj = d3.select(this).data()[0]
            settings.oca = obj.name;
            settings.ocp = "all";
            settings.opl = obj.lowProb;
            settings.oph = obj.probability;
            settings.ors = "tp";
            parent.overlaps.overlapActivate(2);
          }
      });

      d3.selectAll(".bar-tn")
        .on('mouseover', tipTN.show)
        .on('mouseout', tipTN.hide)
        .on("click" , function(){
          if(!(d3.select(this).classed("filled-gray"))){
            obj = d3.select(this).data()[0]
            settings.oca = obj.name;
            settings.ocp = "all";
            settings.opl = obj.lowProb;
            settings.oph = obj.probability;
            settings.ors = "tn";
            parent.overlaps.overlapActivate(2);
          }
      });

      d3.selectAll(".bar-fp")
        .on('mouseover', tipFP.show)
        .on('mouseout', tipFP.hide)
        .on("click" , function(){
          if(!(d3.select(this).classed("filled-gray"))){
            obj = d3.select(this).data()[0]
            settings.oca = obj.name;
            settings.ocp = "all";
            settings.opl = obj.lowProb;
            settings.oph = obj.probability;
            settings.ors = "fp";
            parent.overlaps.overlapActivate(2);
          }
      });

      d3.selectAll(".bar-fn")
        .on('mouseover', tipFN.show)
        .on('mouseout', tipFN.hide)
        .on("click" , function(){
          if(!(d3.select(this).classed("filled-gray"))){
            obj = d3.select(this).data()[0]
            settings.oca = obj.name;
            settings.ocp = "all";
            settings.opl = obj.lowProb;
            settings.oph = obj.probability;          
            settings.ors = "fn";
            parent.overlaps.overlapActivate(2);
          }
      });
  }

  //this.prepareData(this.data);
  this.makeHistograms();
  this.bindEvents();

  this.applySettings = function(data){
    pane= settings.probPane;

    if (data != undefined)
        this.newData = [data.histsPreparedData];

    this.max.left = this.max.right = 0 ;
    for(k = 0 ; k < this.newData[0].length ; k++)
    {
     this.max.left = Math.max(this.max.left, d3.max(this.newData[0][k], function (d) {
          tmpTN = d.tn;
          tmpFN = d.fn;
          if (!settings.probDataOptions.tn) tmpTN = 0 ;
          if (!settings.probDataOptions.fn) tmpFN = 0 ;
          return (tmpTN + tmpFN);
      }));
      this.max.right = Math.max(this.max.right, d3.max(this.newData[0][k], function (d) {
          tmpTP = d.tp;
          tmpFP = d.fp;
          if (!settings.probDataOptions.tp) tmpTP = 0 ;
          if (!settings.probDataOptions.fp) tmpFP = 0 ;
          return (tmpTP + tmpFP);
      }));
    }

    var svg,tp,fn,fp,tn,transitionScale;


    for (ii=0;ii<this.newData.length;ii++)
    {
        scl = Math.max(this.max.left , this.max.right);
        x = d3.scale.linear()
                .domain([-scl , scl]).nice()
                .rangeRound([0, width]);

        y = d3.scale.ordinal()
                .domain(((this.newData[ii])[0]).map(function(d){ return d.probability;}))
                .rangeRoundBands([height , 0] , 0.1);

        xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .ticks(5)
                    .tickSize(0.3)
                    .tickFormat(function(d){
                      f = Math.abs(d);
                      if(f>=1000) return(Math.round(f/1000) + "K");
                      else return f;
                    });

        yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .tickValues(y.domain().filter(function(d,i){
                      if(i == 0 || i == (settings.probbins-1)) return true;
                      return false;
                    }))
                    .tickSize(0)
                    .tickPadding(3);

        yAxis2 = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .tickFormat("")
                    .tickSize(0.3);


        svg = pane.selectAll("svg.svg-probHist")
                  .data(this.newData[ii])

            svg = svg.select("g");

            transitionScale = svg.transition().duration(this.settings.duration * (ii+1));

                                transitionScale.select(".x.axis")
                                .call(xAxis);

                                transitionScale.select(".y.axis")
                                .call(yAxis)

                                transitionScale.select(".y.axis2")
                                .call(yAxis2)


            tp = svg.selectAll(".bar-tp")
                  .data(function(d){
                      return d;
                  })


                  tp.enter().append("rect")
                  .attr("class" , function(d){
                      return d.name+" bar-tp bar";})

                  tp.transition().duration(this.settings.duration * (ii+1))/*.each('end', function(d){

                  })*/
                  .attr("x" , function(d){return x(0);})
                  .attr("y" , function(d){ return y(d.probability);})
                  .attr("width" , function(d){
                      tmpTP = d.tp ;
                      if (!settings.probDataOptions.tp)
                          tmpTP = 0 ;
                      if (tmpTP > Settings.probtpFilter)
                          tmpTP = 0 ;

                      return Math.abs(x(tmpTP) - x(0));
                  })
                  .attr("height" , function(d){return y.rangeBand()});
                  tp.exit().remove();

                  fp = svg.selectAll(".bar-fp")
                      .data(function(d){ return d;})

                      fp.enter().append("rect")
                      .attr("class" , function(d){return d.name+" bar-fp bar";})

                      fp.transition().duration(this.settings.duration * (ii+1))
                      .attr("x" , function(d){
                        tmpTP = d.tp ;
                        if (!settings.probDataOptions.tp)
                            tmpTP = 0 ;
                        return x(tmpTP);
                      })
                      .attr("y" , function(d){

                        return y(d.probability);
                      })
                      .attr("width" , function(d){
                        tmpFP = d.fp ;
                        if (!settings.probDataOptions.fp)
                            tmpFP = 0 ;
                          return Math.abs(x(tmpFP) - x(0));
                      })
                      .attr("height" , function(d){return y.rangeBand()});

                      fp.exit().remove();



                 fn = svg.selectAll(".bar-fn")
              .data(function(d){return d;})

              fn.enter().append("rect")
              .attr("class" , function(d){return d.name+" bar-fn bar";})

              fn.transition().duration(this.settings.duration * (ii+1))
              .attr("x" , function(d){
                  tmpFN = d.fn ;
                if (!settings.probDataOptions.fn)
                    tmpFN = 0 ;
                  return x(-tmpFN);
              })
              .attr("y" , function(d){return y(d.probability);})
              .attr("width" , function(d){
                   tmpFN = d.fn ;
                if (!settings.probDataOptions.fn)
                    tmpFN = 0 ;
                  return Math.abs(x(tmpFN) - x(0));
              })
              .attr("height" , function(d){return y.rangeBand()});

              fn.exit().remove();


             tn = svg.selectAll(".bar-tn")
              .data(function(d){d.tn = 0; return d;})

              tn.enter().append("rect")
              .attr("class" , function(d){return d.name+" bar-tn bar";})

              tn.transition().duration(this.settings.duration * (ii+1))
              .attr("x" , function(d){
                tmpFN = d.fn ;
                tmpTN = d.tn ;
                if (!settings.probDataOptions.fn)
                    tmpFN = 0 ;
                 if (!settings.probDataOptions.tn)
                    tmpTN = 0 ;

                  if (tmpTN < Settings.probtnFilter)
                    tmpTN = 0 ;
                  return x(-tmpFN-tmpTN);
              })
              .attr("y" , function(d){return y(d.probability);})
              .attr("width" , function(d){
                  tmpTN = d.tn ;
                  if (!settings.probDataOptions.tn)
                    tmpTN = 0 ;
                  return Math.abs(x(tmpTN) - x(0));
              })
              .attr("height" , function(d){return y.rangeBand()})

              tn.exit().remove();

        this.bindEvents();
    }


  }

  this.overlap = function(nowdata){
    pane = settings.probPane;
    //this.prepareData(nowdata);
      this.newData = [model.histsPreparedData]

    var svg = pane.selectAll("svg")
              .data(this.newData[0])

    groups = svg.select("g");

    var tp = groups.selectAll(".overlap-tp")
              .data(function(d){return d;})
              .enter().append("rect")
              .attr("class" , function(d){return d.name+" overlap-tp overlap";})
              .attr("x" , function(d){return x(0);})
              .attr("y" , function(d){return y(d.probability);})
              .attr("width" , function(d){return Math.abs(x(d.tp) - x(0));})
              .attr("height" , function(d){return y.rangeBand()})
              .on('mouseover', tipTP.show)
				.on('mouseout', tipTP.hide);

    var fp = groups.selectAll(".overlap-fp")
              .data(function(d){return d;})
              .enter().append("rect")
              .attr("class" , function(d){return d.name+" overlap-fp overlap";})
              .attr("x" , function(d){return x(d.tp);})
              .attr("y" , function(d){return y(d.probability);})
              .attr("width" , function(d){return Math.abs(x(d.fp) - x(0));})
              .attr("height" , function(d){return y.rangeBand()})
              .on('mouseover', tipFP.show)
				.on('mouseout', tipFP.hide);

    var fn = groups.selectAll(".overlap-fn")
              .data(function(d){return d;})
              .enter().append("rect")
              .attr("class" , function(d){return d.name+" overlap-fn overlap";})
              .attr("x" , function(d){return x(-d.fn);})
              .attr("y" , function(d){return y(d.probability);})
              .attr("width" , function(d){return Math.abs(x(d.fn) - x(0));})
              .attr("height" , function(d){return y.rangeBand()})
              .on('mouseover', tipFN.show)
				.on('mouseout', tipFN.hide);

    var tn = groups.selectAll(".overlap-tn")
              .data(function(d){return d;})
              .enter().append("rect")
              .attr("class" , function(d){return d.name+" overlap-tn overlap";})
              .attr("x" , function(d){return x(-d.fn-d.tn);})
              .attr("y" , function(d){return y(d.probability);})
              .attr("width" , function(d){return Math.abs(x(d.tn) - x(0));})
              .attr("height" , function(d){return y.rangeBand()})
              .on('mouseover', tipTN.show)
				.on('mouseout', tipTN.hide);




              
  }
}// end of class