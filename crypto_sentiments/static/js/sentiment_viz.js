var margin = {top: 30, right: 50, bottom: 30, left: 100};
var svgWidth = 1200;
var svgHeight = 270;
var graphWidth = svgWidth - margin.left - margin.right;
var graphHeight = svgHeight - margin.top - margin.bottom;

var x = d3.time.scale().range([0, graphWidth]);
var y = d3.scale.linear().range([graphHeight, 0]);

var parseDate = d3.time.format("%Y-%m-%d").parse;
var parseYear = d3.time.format("%Y").parse;

var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);
var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

var priceLine = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.price); });

var sentimentLine = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.sentiment); });


var svg2 = d3.select("#sentiment-chart")
    .append("svg2")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


function drawGraph() {
  // For each row in the data, parse the date
  // and use + to make sure data is numerical

    url = "/viz/data"

    d3.json(url, function(error, data) {
        console.log("data is loaded")
        var data = data['pts']

        data.forEach(function(d) {
            d.date = parseDate(d.date);
            console.log(d.date)
            d.price = +d.price;
            d.sentiment = +d.sentiment;
        });

        console.log(data)

        var svg = d3.select("#price-chart")
            .append("svg")
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        
        y.domain([d3.min(data, function(d) {
            return Math.min(d.price) }),
                d3.max(data, function(d) {
            return Math.max(d.price) })]);  

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + graphHeight + ")")
              .call(xAxis);

        svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("dy", "-5em")
            .attr("transform", "rotate(-90)")
            .text("Price of Bitcoin (USD)");


        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

        // Add the highLine as a green line
        svg.append("path")
            .style("stroke", "green")
            .style("fill", "none")
            .attr("class", "line")
            .attr("d", priceLine(data));


        var svg2 = d3.select("#price-chart")
            .append("svg")
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        
        y.domain([d3.min(data, function(d) {
            return Math.min(-1) }),
                d3.max(data, function(d) {
            return Math.max(d.sentiment) })]);  

        // Add the X Axis
        svg2.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + graphHeight + ")")
              .call(xAxis);

        // Add the Y Axis
        svg2.append("g")
            .attr("class", "y axis")
            .call(yAxis);

        svg2.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("dy", "-5em")
            .attr("transform", "rotate(-90)")
            .text("Sentiment Score");

        // Add the highLine as a green line
        svg2.append("path")
            .style("stroke", "blue")
            .style("fill", "none")
            .attr("class", "line")
            .attr("d", sentimentLine(data));


        // Add the closeLine as a blue dashed line
        // svg.append("path")
        //     .style("stroke", "blue")
        //     .style("fill", "none")
        //     .style("stroke-dasharray", ("3, 3"))
        //     .attr("d", closeLine(data));

        // // Add the lowLine as a red dashed line
        // svg.append("path")
        //     .style("stroke", "red")
        //     .attr("d", lowLine(data));

        

        



    // // Add the text for the "Low" line
    // svg.append("text")
    //     .attr("transform", "translate("+(graphWidth+3)+","+y(graphData[0].Low)+")")
    //     .attr("dy", ".35em")
    //     .attr("text-anchor", "start")
    //     .style("fill", "red")
    //     .text("Low");

    // // Add the text for the "Close" line
    // svg.append("text")
    //     .attr("transform", "translate("+(graphWidth+3)+","+y(graphData[0].Close)+")")
    //     .attr("dy", ".35em")
    //     .attr("text-anchor", "start")
    //     .style("fill", "blue")
    //     .text("Close");
    });
}

$(document).ready(function() {
    drawGraph();
})
