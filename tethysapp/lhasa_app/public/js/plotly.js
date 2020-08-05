let chartdata = null

function getDrawnChart(drawnItems) {
    // if there's nothing to get charts for then quit
    let geojson = drawnItems.toGeoJSON()["features"]
    if (geojson.length === 0 && chosenRegion === "") {
        return
    }

    $("#chart").html(
        '<div class="load"><img src="https://media.giphy.com/media/jAYUbVXgESSti/giphy.gif"></div>'
    )

    let coords = geojson[0]["geometry"]["coordinates"]
    let loc_type = geojson[0]["geometry"]["type"]
    let variable = $("#variables").val()

    if (loc_type === "Polygon") {
        coords = [coords[0][0][0], coords[0][0][1], coords[0][2][0], coords[0][2][1]]
    }

    console.log("Coordinates", coords)

    // setup a parameters json to generate the right timeserie
    let data = {
        coords: coords,
        variable: variable,
        loc_type: loc_type
    }

    $("#chart_modal").modal("show")
    // decide which ajax url you need based on drawing type
    $.ajax({
        url: URL_requestTimeSeries,
        data: data,
        dataType: "json",
        contentType: "application/json",
        method: "GET",
        success: function(result) {
            // clear the loading gif
            $("#chart").html("")
            // save the data sent back by python to a global variable we can use later
            chartdata = result
            // call the function to create a plotly graph of the data
            plotlyTimeseries(chartdata)
        }
    })
}

function plotlyTimeseries(data) {
    let variable = $("#variables option:selected").text()
    let layout = {
        title: "Timeseries of " + variable,
        xaxis: { title: "Time" },
        yaxis: { title: "Values" }
    }

    let values = {
        x: data.x,
        y: data.y,
        mode: "lines+markers",
        type: "scatter"
    }
    Plotly.newPlot("chart", [values], layout)
    let chart = $("#chart")
    chart.css("height", 500)
    Plotly.Plots.resize(chart[0])
}

function chartToCSV() {
    function zip(arrays) {
        return arrays[0].map(function(_, i) {
            return arrays.map(function(array) {
                return array[i]
            })
        })
    }
    if (chartdata === null) {
        alert("There is no data in the chart. Please plot some data first.")
        return
    }
    let data = zip([chartdata.x, chartdata.y])
    let csv = "data:text/csv;charset=utf-8," + data.map((e) => e.join(",")).join("\n")
    let link = document.createElement("a")
    link.setAttribute("href", encodeURI(csv))
    link.setAttribute("target", "_blank")
    link.setAttribute("download", "extracted_time_series.csv")
    document.body.appendChild(link)
    link.click()
    $("#a").remove()
}

// WHEN YOU CLICK ON THE DOWNLOAD BUTTON- RUN THE DOWNLOAD CSV FUNCTION
$("#chartCSV").click(function() {
    chartToCSV()
})
