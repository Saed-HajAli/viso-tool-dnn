function Settings(){

    // define panes
    // Frontend
    this.confPane = d3.select(".confusion-matrix");
    this.tablePane = d3.select(".data-table");
    this.pagerPane = d3.select(".pager")
    this.featurePane = d3.select(".box-plots");
    this.histPane = d3.select(".class-histogram");
    this.probPane = d3.select(".probability-histograms");
    this.imgPane = d3.select(".browser");
    this.imgPagerPane = d3.select(".img-pager");
    this.tabbedPane = d3.select(".tabbed-view");


  	// state of data switches
    // Frontend
  	this.probDataOptions = {
  	    tp : true,
  	    tn : true,
  	    fp : true,
  	    fn : true
  	}


    //tn filter slider value
    // Frontend
    this.probtnDefaultFilter = 0.10;

    //tp filter probability value
    // Frontend
    this.probtpDefaultFilter = 1.00;

        // Frontend
    this.mintnFilter = 0.0;
    // Frontend
    this.mintpFilter = 0.5;
    // Frontend
    this.maxtnFilter = 0.5;
    // Frontend
    this.maxtpFilter = 1.0;


    // Frontend
    this.imgSize = 15;


  	// To change the interface values

  	// max bins value on slider
    // Frontend
  	this.maxBins = 30;

  	// min bins value on slider
    // Frontend
  	this.minBins = 1;

  	// bin slider step
    // Frontend
  	this.stepBins = 1;

  	// min probability value on slider
    // Frontend
  	this.minProb = 0.00;

  	// max probability value on slider
    // Frontend
  	this.maxProb = 1.00;

  	// probability slider step
    // Frontend
  	this.stepProb = 0.01;
    // Frontend
    this.duration = 200

    // Frontend
    this.matrixDiagonals = true;

    // 0 : color scale ; fixed dimensions
    // 1 : fixed color ; dimension scale
    // Frontend
    this.matrixMode = 0;

    // Frontend
    this.tableSize = 500;

    // -------------------------------------------------------------------------------------------------------------------- //

	//probability limits
    // Backend
  	this.probLimits = [0.00 , 1.00];

  	//tn filter slider value
    // Backend
  	this.probtnFilter = 0.10;

  	//tp filter probability value
    // Backend
  	this.probtpFilter = 1.00;

  	// bins count in probability histograms
    // Backend
  	this.probbins = 10;

    // Backend
    this.boxIQR = 1.5;

    // Backend
    this.opl = 0.00;
    this.oph = 1.00;
    this.oca = "all";
    this.ocp = "all";
    this.ors = "all"; 

    // -------------------------------------------------------------------------------------------------------------------- //

    // //Apply switches on summary
    // this.switchesOnSummary = true;

    // //Apply switches on summary
    // this.filtersOnSummary = true;

    this.imgCurrentPage = 1;

    this.tableCurrentPage = 1;

}