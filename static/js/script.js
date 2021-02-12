

	var probHist ;
	// file reader
	//var reader = new FileReader();

	var reader = []

	//bind container for probability histograms
	var probabilityPane = d3.select(".central-pane").select(".probability-histograms");

	//initialize settigns
	var settings = new Settings();

	//bind container for Data View
	var dataPane = d3.select("#data-samples");//.select(".data-table");

	//bind container for Feature View
	var featurePane = d3.select("#feature-view");

	//initialize and setup slider for zooming in/out probabilities
	var probabilitySlider = document.getElementById('probability-zoom');
	  noUiSlider.create(probabilitySlider, {
	   start: settings.probLimits,
	   behaviour: 'drag-tap',
	   connect: true,
	   tooltips : true,
	   step: settings.stepProb,
	   range: {
	     'min': settings.minProb,
	     'max': settings.maxProb
	   }
	  });

	//initialize and setup slider for increase or decrease in histogram bins
	var binSlider = document.getElementById('rebin');
	  noUiSlider.create(binSlider, {
	   	start: settings.probbins,
	   	connect : 'lower',
	   	tooltips : true,
	   	format: wNumb({
	        decimals: 0,
	        thousand: ',',
	    }),
	   	step: settings.stepBins,
	   	range: {
		     'min': settings.minBins,
		     'max': settings.maxBins
	   	}
	  });

	//initialize and setup slider for filtering out high TPs (above 0.5)
	var tpSlider = document.getElementById('filter-high-tp');
	noUiSlider.create(tpSlider, {
	   	start: settings.probtpDefaultFilter,
	   	connect : 'lower',
	   	tooltips : true,

	   	step: 0.01,
	   	range: {
		     'min': settings.mintpFilter,
		     'max': settings.maxtpFilter
	   	}
	});

	function vis(data) {

		if (probHist != undefined)
		{
			// console.log("Apply Setting")
			var m = new Model(data)
			probHist.data = m.data
			probHist.applySettings()
		} else {
			// console.log("Create Viso")
			var m = new Model(data)
			initInterface(m.data)
		}

	}

	//initialize and setup slider for filtering out low TNs (below 0.5)
	var tnSlider = document.getElementById('filter-low-tn');
	noUiSlider.create(tnSlider, {
	   	start: settings.probtnDefaultFilter,
	   	connect : 'upper',
	   	tooltips : true,

	   	step: 0.01,
	   	range: {
		     'min': settings.mintnFilter,
		     'max': settings.maxtnFilter
	   	}
	});


	d3.selectAll(".collapsible-body").selectAll(".clear").attr("disabled", "disabled");

	renderVisualizations = function(file,i){
		reader[i] = new FileReader()
		reader[i].readAsText(file)

		// reader[i].addEventListener("load", function(){parseFile(i);}, false)
		// if (file) {
		// 	reader[i].readAsText(file)
		// }

	}



	var models = []
	function parseFile(i){


		if (probHist == undefined)
			{
				// console.log("in if : " + i)
				initInterface(models[i].data)
			}
		else
			{
				probHist.data = models[i].data
				// console.log("in else :" + i)
				probHist.applySettings(function(){
					console.log("Done")
				});
			}
	}


	/*d3.selectAll(".input-file").on("change" , function(){
		// renderVisualizations(this.files[0]);

		var formData = new FormData();
		formData.append('file', this.files[0]);

		$.ajax({
            type : "POST",
            url : "http://127.0.0.1:5000/upload",
			data: formData,
            cache: false,
            async: false,
			processData: false,
			contentType: false,
            success : function (data) {
            	console.log(data)
			},
            error: function (XMLHttpRequest, textStatus, errorThrown) {
            	console.log(XMLHttpRequest)
			}
        });

		/!*
		reader = new Array(this.files.length);
		console.log("reader start")
		for(var i = 0 ; i < this.files.length;i++)
		{
			//console.log(i)
			renderVisualizations(this.files[i],i);
		}

		setTimeout(function() {
			console.log("create model")
			for(var i = 0 ; i < reader.length;i++)
			{
				// console.log(i)
				var data = d3.csv.parse(reader[i].result);
				models.push(new Viso(data))
			}

			console.log("vis start")
			for(var j  = 0 ; j < models.length; j++)
			{
				parseFile(j)
			}
			console.log("vis finish")

		  }, 3000);
		*!/






		// for (i=0;i < this.files.length ; i++)
		// {
		// 	console.log(i)
		// 	setTimeout(function() {
		// 		renderVisualizations(this.files[i]);
		// 		console.log("run " + i);
		// 	}, 2000 + 200 * i);
		// }
		// mfiles = this.files




		//   setTimeout(function() {
		// 	renderVisualizations(mfiles[2]);
		//   }, 2600);


	});
*/
	// read data and init again
	changeDataset = function(){
		d3.csv("data/out.csv", function (error, data) {
			if(error){
				 $('#file-error-modal').openModal();
			}
			else initInterface(data);
		});
	}

	//changeDataset()

	i = 100 ;
	d3.select(".new-data").on("click", function(d){
		$('#file-upload-modal').openModal();
	});

	initInterface = function(data){



		for(ii = 0 ; ii<1;ii++)
		{
			_self = this;
			//prepare data model do all basic calculations about data
			//var model = new Viso(data[ii]);

			tabs = d3.select("ul.tabs")

			tabs.append("li")
				.attr("class" , "tab col s4")
					.append("a")
					.attr("href" , "#conf-mat")
					.text("Matrix")

			if (data.features.length > 0){
				tabs.append("li")
					.attr("class" , "tab col s4")
						.append("a")
						.attr("href" , "#feature-view")
						.text("Features")
				d3.select("#feature-view").classed("dont-display", false)
			}
			else{
				d3.select("#feature-view").classed("dont-display", true)
			}

			tabs.append("li")
				.attr("class" , "tab col s4")
					.append("a")
					.attr("href" , "#data-samples")
					.text("Samples")

			if (data.images != -1){
				tabs.append("li")
					.attr("class" , "tab col s4")
						.append("a")
						.attr("href" , "#image-browser")
						.text("Images")
				d3.select("#image-browser").classed("dont-display", false)
			}
			else{
				d3.select("#image-browser").classed("dont-display", true)
			}

			$('ul.tabs').tabs();
			d3.select("#conf-mat").style("display", "initial")

			// initialize data table
			var table = new Table(data , settings);

			//initialize Features Box Plots
			var boxPlots = new BoxFeatures(data , settings)

			//initialize class probability histograms

			probHist = new ProbHist(data , settings, _self);

			//initialize summary class histograms
			var classhist = new classHist(data , settings, _self);

			//initialize confusion Matrix
			var confmat = new confMatrix(data , settings, _self);

			//initialise image browser
			var img = new imageBrowser(data , settings)

			//initialize selection overlaps
			this.overlaps = new Overlaps(data , settings, table, boxPlots, probHist, classhist, confmat, img);

			// action listener for TP switch
			d3.select(".switch-tp").on("change", function(d){
				settings.probDataOptions.tp = this.checked;
				probHist.applySettings();
				if(settings.switchesOnSummary) classHist.applySettings();
			});

			// action listener for FP switch
			d3.select(".switch-fp").on("change", function(d){
				settings.probDataOptions.fp = this.checked;
				probHist.applySettings();
				if(settings.switchesOnSummary) classHist.applySettings();
			});

			// action listener for TN switch
			d3.select(".switch-tn").on("change", function(d){
				settings.probDataOptions.tn = this.checked;
				probHist.applySettings();
				if(settings.switchesOnSummary) classHist.applySettings();
			});

			// action listener for FN switch
			d3.select(".switch-fn").on("change", function(d){
				settings.probDataOptions.fn = this.checked;
				probHist.applySettings();
				if(settings.switchesOnSummary) classHist.applySettings();
			});

			//reset the probabilty slider and rebin slider
			d3.select(".reset").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					bins = 10;
					probs = [0.00 , 1.00];
					binSlider.noUiSlider.set(bins);
					probabilitySlider.noUiSlider.set(probs);
					tpSlider.noUiSlider.set(settings.probtpDefaultFilter);
					tnSlider.noUiSlider.set(settings.probtnDefaultFilter);
					settings.probtpFilter = settings.probtpDefaultFilter;
					settings.probtnFilter = settings.probtnDefaultFilter;
					settings.probbins = bins;
					settings.probLimits = probs;
					probHist.applySettings();
				}
			});

			d3.select(".clear").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					overlaps.overlapDeactivate();
				}
			});

			// apply new probability window and rebin settings to histograms
			d3.select(".apply").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					settings.probtpFilter = Number(tpSlider.noUiSlider.get());
					settings.probtnFilter = Number(tnSlider.noUiSlider.get());
					settings.probbins = Number(binSlider.noUiSlider.get());
					settings.probLimits = probabilitySlider.noUiSlider.get().map(Number);

					$.ajax({
						url: 'http://127.0.0.1:5000/run?id=out',
						type: 'post',
						dataType: 'json',
						contentType: 'application/json',
						success: function (data) {
							probHist.applySettings(data);
						},
						data: JSON.stringify({Settings : {probLimits : settings.probLimits , probtnFilter : settings.probtnFilter , probtpFilter : settings.probtpFilter, probbins : settings.probbins, boxIQR: settings.boxIQR}})
					});


				}
			});

			d3.select(".prev").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					table.slideData(0);
				}
			});

			d3.select(".next").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					table.slideData(1);
				}
			});

			d3.select(".first").on("click" , function(){
					table.slideData(-1);
			});

			d3.select(".last").on("click" , function(){
					table.slideData(2);
			});

			d3.select(".img-prev").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					img.slideData(0);
				}
			});

			d3.select(".img-next").on("click" , function(){
				if(!d3.select(this).classed("disabled")){
					img.slideData(1);
				}
			});

			d3.select(".img-first").on("click" , function(){
					img.slideData(-1);
			});

			d3.select(".img-last").on("click" , function(){
					img.slideData(2);
			});

			d3.selectAll(".with-gap").on("change", function(d){
				mode = d3.select('input[name="mat-mode"]:checked').property("id");
				if(mode == "size-mode") settings.matrixMode = 1;
				else if (mode == "fill-mode") settings.matrixMode = 0;
				confmat.applySettings();
			});

			d3.select("#diagonal").on("change", function(d){
				settings.matrixDiagonals = this.checked;
				confmat.applySettings();
			});
		}

	}





