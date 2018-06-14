function init() {
	Plotly.d3.json('/samples/BB_940', function(error, otu_list){
       if (error) return console.warn(error);

	var  data = [{
		"labels": otu_list[0]['otu_ids'],
		"values": otu_list[0]['sample_values'],
		"type": "pie"}]
       var PIE = document.getElementById('pie');
       Plotly.plot(PIE, data, layout);
   })
}


function updatePlotly(newdata) {
	var PIE = document.getElementById("pie");
	Plotly.restyle(PIE, "labels", [newdata.labels]);
	Plotly.restyle(PIE, "values", [newdata.values]);
	
}


function optionChanged(dataset) {
	console.log(dataset);

	Plotly.d3.json('/samples/' + dataset, function(error, otu_list){
       if (error) return console.warn(error);
	var  data = [{
		"labels": otu_list[0]['otu_ids'],
		"values": otu_list[0]['sample_values'],
		"type": "pie"}]
   })
	updatePlotly(data);
}

init();