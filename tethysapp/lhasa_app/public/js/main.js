// base.html scripts has additional vars from render context
let csrftoken = Cookies.get("csrftoken")
var prevLayer = null

const layerMapping = {
    1: "",
    //2: "https://maps.disasters.nasa.gov/ags03/rest/services/NRT_Latest/GPM_NRT_7day_Latest/ImageServer",
    //2: "https://maps.disasters.nasa.gov/ags03/rest/services/NRT_Latest/GPM_NRT_30min_Latest/ImageServer",
    //3: "https://maps.disasters.nasa.gov/ags03/rest/services/GPM_NRT/GPM_NRT_3hr/ImageServer", //this no longer exists
    //3: "https://maps.disasters.nasa.gov/ags03/rest/services/NRT_Latest/GPM_NRT_1day_Latest/ImageServer",
    //2: "https://maps.nccs.nasa.gov/server/rest/services/global_landslide_catalog/landslide_susceptibility/MapServer"
    3: "https://maps.disasters.nasa.gov/ags03/rest/services/GPM_NRT/GPM_NRT_7day/ImageServer",
    4: "https://maps.disasters.nasa.gov/ags03/rest/services/NRT/landslide_nowcast/ImageServer",
   // 5: "",
}

function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

for (const [key, value] of Object.entries(layerMapping)) {
    var newLayer = L.esri.imageMapLayer({
        url: value,
        opacity: 0.5,
        // only necessary for old versions of ArcGIS Server
        useCors: false
    })
    layerMapping[key] = newLayer
}

var statesFeatureGroup = statesESRI() //adds the state boundaries of Brazil from esri living atlas
let controlsObj = makeControls() // the layer toggle controls top-right corner
//legend.addTo(mapObj) // add the legend graphic to the map
latlon.addTo(mapObj) // add the box showing lat and lon to the map

////////////////////////////////////////////////////////////////////////  EVENT LISTENERS
function update() {
    // layerWMS = newWMS()
    stateLayer = statesESRI()
    controlsObj = makeControls()
    legend.addTo(mapObj)
}
function changestates(firedfrom) {
    let countryJQ = $("#countries")
    let stateJQ = $("#states")
    if (firedfrom === "country") {
        let country = countryJQ.val()
        regionJQ.val("none")
    } else {
        countryJQ.val("")
    }
    // change to none/empty input
    mapObj.removeLayer(stateLayer)
    controlsObj.removeLayer(stateLayer)
    if (firedfrom === "state") {
        stateLayer = statesESRI()
        controlsObj.addOverlay(stateLayer, "State Boundaries")
    } /*else {
        layerRegion = countriesESRI()
        controlsObj.addOverlay(layerRegion, "Country Boundaries")
    }*/
}
function changeregions(firedfrom) {
    let countryJQ = $("#countries")
    let regionJQ = $("#regions")
    if (firedfrom === "country") {
        let country = countryJQ.val()
        if (!countrieslist.includes(country)) {
            alert(
                'The country "' +
                    country +
                    '" was not found in the list of countries available. Please check spelling and capitalization, and use the input suggestions.'
            )
            return
        }
        regionJQ.val("none")
    } else {
        countryJQ.val("")
    }
    // change to none/empty input
    mapObj.removeLayer(layerRegion)
    controlsObj.removeLayer(layerRegion)
    if (firedfrom === "region") {
        layerRegion = regionsESRI()
        controlsObj.addOverlay(layerRegion, "Region Boundaries")
    } else {
        layerRegion = countriesESRI()
        controlsObj.addOverlay(layerRegion, "Country Boundaries")
    }
}

// input validation
$(".customs").keyup(function() {
    this.value = this.value.replace(/i[a-z]/, "")
})

// data controls
$("#variables").change(function() {

    //value of current data set
    curvariable = $("#variables").val()

    let layerToSelect = curvariable

    if (prevLayer != null) {
        layerMapping[prevLayer].remove(mapObj)
        // Do something here to hide/remove the previous layer
        // Remove that specific layer from the map
    }

    prevLayer = layerToSelect

    layerMapping[layerToSelect].addTo(mapObj)
})
$("#dates").change(function() {
    clearMap()
    update()
    getDrawnChart(drawnItems)
})
$("#charttype").change(function() {
    makechart()
})
$("#regions").change(function() {
    changeregions("region")
})
$("#states").change(function() {

    //value of current selected state
    curstate = $("#states").val()

    // jquery val
    let id = curstate

    var matched_layer = null

    statesFeatureGroup.eachLayer(function(layer) {
        if (layer.feature.properties.id == id) {
            matched_layer = layer
        }
    })

    mapObj.fitBounds(matched_layer.getBounds())
})

$("#countriesGO").click(function() {
    changeregions("country")
})

// display controls
$("#display").click(function() {
    $("#displayopts").toggle()
})
$("#cs_min").change(function() {
    if ($("#use_csrange").is(":checked")) {
        clearMap()
        update()
    }
})
$("#cs_max").change(function() {
    if ($("#use_csrange").is(":checked")) {
        clearMap()
        update()
    }
})
$("#use_csrange").change(function() {
    clearMap()
    update()
})
$("#colorscheme").change(function() {
    clearMap()
    update()
})
$("#opacity").change(function() {
    layerWMS.setOpacity($(this).val())
})
$("#gjClr").change(function() {
    styleGeoJSON()
})
$("#gjOp").change(function() {
    styleGeoJSON()
})
$("#gjWt").change(function() {
    styleGeoJSON()
})
$("#gjFlClr").change(function() {
    styleGeoJSON()
})
$("#gjFlOp").change(function() {
    styleGeoJSON()
})