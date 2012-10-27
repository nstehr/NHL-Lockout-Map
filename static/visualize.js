function CountryModel() {
    this.countryName = ko.observable();
    this.count = ko.observable();
    this.players = ko.observableArray();

	ko.bindingHandlers.kendoGrid.options = {
	        sortable: true,
	        pageable: {pageSize: 10},
	    };

}

var viewModel = new CountryModel();

// Activates knockout.js
ko.applyBindings(viewModel);

$.getJSON('static/data.json', function(data) {
    $.getJSON('static/europe.json', function(countries){
	countryData = data.countries;
	renderMap(countries,countryData);
	//initialize the table to all of Europe
	initViewModel(countryData);
	
});
    
});
/**
countries: the geo-points for the countries
countryData: the player data for each country
*/
function renderMap(countries,countryData){
	
	var xy = d3.geo.mercator().scale([3000]).translate([400,900]);
	var path = d3.geo.path().projection(xy)
	
	var chartWidth = 850; 
	var chartHeight = 768;
	
	var viz = d3.select("#map").append("svg")
	     .attr("class", "Blues")
	     .attr("width", chartWidth)
	     .attr("height", chartHeight)
	     .attr("transform", "translate(-300,0)");
	//based on population example
    var quantize = d3.scale.quantile().domain([0, 12]).range(d3.range(9));
	
	viz.append("g")
	.attr("transform", "translate(-300,0)")
	.selectAll("path")
    .data(countries.features)
    .enter().append("path")
    .attr("d", path)
    .attr("class", function(d) { 
	         //some countries don't have any players, so undefined check  
	         var countryValue = countryData[d.properties.CntryName];
	         var count = 0;
	         if(countryValue){
	             count = countryValue.count;
	           }
	         var val = "q" + quantize(count) + "-9"; 
	         return val;  
	     })
    
    .attr("stroke", "antiquewhite")
    .on("click",function(d,i){
	         var countryValue = countryData[d.properties.CntryName];
	         updateViewModel(d.properties.CntryName,countryValue);
	            
	});

}

function initViewModel(countryData){
	viewModel.countryName("Europe");
	var totalPlayerCount = 0;
	var allPlayers = [];
	$.each(countryData, function(countryName,value){
	    totalPlayerCount = totalPlayerCount + value.count;	
	    allPlayers = allPlayers.concat(value.players);
	});
	viewModel.count(totalPlayerCount);
	viewModel.players(allPlayers);
}

function updateViewModel(countryName,countryValue){
	viewModel.countryName(countryName);
	if(countryValue){
	    viewModel.count(countryValue.count);
	    viewModel.players(countryValue.players);
	}
	else{
		viewModel.count(0);
		viewModel.players({name:"",team:""})
	}
}