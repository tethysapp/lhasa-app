let chartdata = null;

function plotlyTimeseries(data) {
    let x = [];
    let y = [];
    let layout = {
        title: data['meta']['name'] + ' v Time ' + '(' + data['meta']['seriesmsg'] + ')',
        xaxis: {title: 'Time'},
        yaxis: {title: 'Units - ' + data['meta']['units']}
    };

    for (let i = 0; i < data['timeseries'].length; i++) {
        x.push(data['timeseries'][i][0]);
        y.push(data['timeseries'][i][1]);
    }

    let values = {
        x: x,
        y: y,
        title: data['meta']['name'],
        mode: 'lines+markers',
        type: 'scatter'
    };
    Plotly.newPlot('chart', [values], layout);
    let chart = $("#chart");
    chart.css('height', 500);
    Plotly.Plots.resize(chart[0]);
}

function getDrawnChart(drawnItems) {
    // if there's nothing to get charts for then quit
    let geojson = drawnItems.toGeoJSON()['features'];
    if (geojson.length === 0 && chosenRegion === '') {
        return
    }

    $("#chart").html('<div class="load"><img src="https://media.giphy.com/media/jAYUbVXgESSti/giphy.gif"></div>');

    let coords = geojson[0]['geometry']['coordinates'];
    let loc_type = geojson[0]['geometry']['type'];
    let variable = $("#variables").val();

    if (loc_type === 'Polygon') {
        coords = [coords[0][0][0], coords[0][0][1], coords[0][2][0], coords[0][2][1]]
    }

    // setup a parameters json to generate the right timeserie
    let data = {
        coords: coords,
        variable: variable,
        loc_type: loc_type,
    };

    $("#chart_modal").modal('show');
    // decide which ajax url you need based on drawing type
    $.ajax({
        url: URL_requestTimeSeries,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        method: 'GET',
        success: function (result) {
            chartdata = result;
            plotlyTimeseries(chartdata);
        }
    })
}

function chartToCSV() {
    if (chartdata === null) {
        alert('There is no data in the chart. Please plot some data first.');
        return
    }
    let data = chartdata['timeseries'];
    let csv = "data:text/csv;charset=utf-8," + data.map(e => e.join(",")).join("\n");
    let link = document.createElement('a');
    link.setAttribute('href', encodeURI(csv));
    link.setAttribute('target', '_blank');
    link.setAttribute('download', app + '_timeseries.csv');
    document.body.appendChild(link);
    link.click();
    $("#a").remove()
}

// WHEN YOU CLICK ON THE DOWNLOAD BUTTON- RUN THE DOWNLOAD CSV FUNCTION
$("#chartCSV").click(function () {chartToCSV()});