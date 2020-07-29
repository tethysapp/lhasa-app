# Multidimensional Data Series Template

This is a tethys app for demonstrating the steps you need to program in order to:
1. Show animated maps of raster data via open source tools (THREDDS Data Server)
2. Extract time series of values from the multidimensional raster files in a web app environment

© Riley Hales, 2020. Developed at the BYU Hydroinformatics Lab for a SERVIR Hackathon event August 2020

## Step 0: Prerequisites and Recommendations

1. I would highly recommend you use an IDE (integrated development environment) for this exercise. PyCharm has a free version which is excellent but any decent IDE should work fine.
2. You need to have installed tethys via and activated the tethys environment in your bash shell (http://docs.tethysplatform.org/en/stable/installation.html)
3. You need access to the Docker CLI (https://docs.docker.com/desktop/). Preferably, you have pulled the image for THREDDS Data server to save time later (`docker pull unidata/thredds-docker:latest`)
4. Useful but not essential- install Panoply (https://www.giss.nasa.gov/tools/panoply/)

## Step 1: Clone this app and install

I assume you have already created a tethys conda environment and have activated that environment.
```bash
conda activate your_tethys_environment
```

I have done some initial programming work to provide a foundation for the sample data used in this app. This
includes creating the a javascript map with leaflet and adding a few controls. While these steps are not difficult,
the focus of this exercise is intended to focus on the concept of managing raster files rather than leaflet and
javascript skills.

```bash
git clone https://github.com/rileyhales/multidimenstional_series_template -b start
cd multidimensional_series_template
tethys db start
tethys install -d
```

## Step 2: Explore the App

Start the tethys development server
```bash
tethys manage start
```
and navigate to this app which will be found at 127.0.0.1:8000/apps

Some important features to note
1. I have already created the map
2. I have added controls for switching variables and viewing some additional layers from ESRI's Living Atlas.
These are easy to adapt for othe datasets and more complex data through standard html controls and including additional
javascript to read their values.
3. There is no raster data visible on the map yet.

## Step 3: Get some raster data

For the purposes of this demonstration, I have provided you a few sample netCDF files from NASA GESDISC. These are monthly
average GLDAS files from Jan-Dec 2019. We will create a container for thredds and mount a directory on your computer.
You can mount any directory however I suggest you do it as follows:

```bash
cd ~
mkdir spatialdata
cd spatialdata
mkdir thredds
```

You should now have a folder created at `~/spatialdata` which contains a single folder named `thredds`. The path to
this folder is `~/spatialdata/thredds`. Put the sample data in this directory. To be clear, your folder should look like this:

```bash
~/spatialdata/
    thredds/
        multidimensional_data_tutorial.ncml
        GLDAS_NOAH025_M.A201901.021.nc4
        GLDAS_NOAH025_M.A201902.021.nc4
        GLDAS_NOAH025_M.A201903.021.nc4
        GLDAS_NOAH025_M.A201904.021.nc4
        GLDAS_NOAH025_M.A201905.021.nc4
        GLDAS_NOAH025_M.A201906.021.nc4
        GLDAS_NOAH025_M.A201907.021.nc4
        GLDAS_NOAH025_M.A201908.021.nc4
        GLDAS_NOAH025_M.A201909.021.nc4
        GLDAS_NOAH025_M.A201910.021.nc4
        GLDAS_NOAH025_M.A201911.021.nc4
        GLDAS_NOAH025_M.A201912.021.nc4
```

## Step 5: THREDDS Data Server

While several options are available for showing raster data on maps in web pages, i believe the best choice for showing
animations of raster data is the THREDDS Data Server. THREDDS is compatible with any multidimensional file that can be
read by the Java netcdf library (so netcdf, grib, hd5), is open source, is actively developed and maintained by UCAR.
The only qualifier is that thredds will only provide WMS and other services if your netCDF files conform to the UCAR
Unidata Common Data Model (which has been widely adopted https://www.unidata.ucar.edu/software/netcdf-java/v4.6/CDM/index.html).
Your data MUST conform to this standard so you will have to do a little bit of preprocessing work if it does not. If you
need to convert your data, i strongly recommend working with netcdf files as opposed to hd5 or grib.

We need to install THREDDS (as a container via docker) in order to view our raster data. The THREDDS server also needs
to have access to the `~/spatialdata/thredds` directory (so we will mount that directory to the container)

```bash
cd ~/spatialdata/thredds/
docker run --name thredds -v $PWD:/usr/local/tomcat/content/thredds/public/ -d -p 7000:8080 unidata/thredds-docker:latest
```

You can check on the docker container's status with `docker ps`. When the container is started, open a web page and go
to 127.0.0.1:7000/thredds/catalog.html. Browse the contents and the sampel data provided by THREDDS. The capabilities
of the THREDDS server are managed by a few configuration XML files which we will now modify.

```bash
docker exec -it thredds bash
cd content/thredds/
vi catalog.xml
```

1. Uncomment out the lines for the 3 services at the top
2. Modify the wildcard filters to include *
3. Modify the dataset scan root directory to content/

When you are finished modifying the catalog it should look EXACTLY like this one.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog name="THREDDS Server Default Catalog : You must change this to fit your server!"
         xmlns="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
         xmlns:xlink="http://www.w3.org/1999/xlink"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0
           http://www.unidata.ucar.edu/schemas/thredds/InvCatalog.1.0.6.xsd">

  <service name="all" base="" serviceType="compound">
    <service name="odap" serviceType="OpenDAP" base="/thredds/dodsC/" />
    <service name="dap4" serviceType="DAP4" base="/thredds/dap4/" />
    <service name="http" serviceType="HTTPServer" base="/thredds/fileServer/" />
    <service name="wcs" serviceType="WCS" base="/thredds/wcs/" />
    <service name="wms" serviceType="WMS" base="/thredds/wms/" />
    <service name="ncss" serviceType="NetcdfSubset" base="/thredds/ncss/" />
  </service>

  <service name="dap" base="" serviceType="compound">
    <service name="odap" serviceType="OpenDAP" base="/thredds/dodsC/" />
    <service name="dap4" serviceType="DAP4" base="/thredds/dap4/" />
  </service>

  <datasetScan name="Test all files in a directory" ID="testDatasetScan"
               path="thredds-demo" location="content/">
    <metadata inherited="true">
      <serviceName>all</serviceName>
      <dataType>Grid</dataType>
    </metadata>

    <filter>
      <include wildcard="*"/>
    </filter>
  </datasetScan>

  <catalogRef xlink:title="Test Enhanced Catalog" xlink:href="enhancedCatalog.xml" name=""/>
</catalog>
```

If you have successfully modified the catalog.xml, you can exit the container and restart docker.
```bash
docker restart thredds
```

## Step 5: Configure the tethys app to use THREDDS

Add some custom settings to app.py

```python
# add this import statement at the top
from tethys_sdk.app_settings import CustomSetting

# add this code to the app class beneath the UrlMap section
def custom_settings(self):
    return (
        CustomSetting(
            name='thredds_path',
            type=CustomSetting.TYPE_STRING,
            description="Local file path to datasets (same as used by Thredds) (e.g. ~/spatialdata/thredds/)",
            required=True,
        ),
        CustomSetting(
            name='thredds_url',
            type=CustomSetting.TYPE_STRING,
            description="URL to the GLDAS folder served by THREDDS with trailing / (e.g. http://127.0.0.1:7000/thredds/)",
            required=True,
        )
    )
```

restart the tethys server and fill in the custom settings

## Step 6: Configure the list of variables

Open one of the netCDF Files provided in Panoply. Notice how variable names have both a Long Name and a Short Name. The
short name is used by the file to store and name data. The Long Name is the human readable and full name of which we
want to display in the app as an option. I have already made a list of these names for you. We need to make them options
for the user to switch between in the User Interface of the app. In controllers.py, update the code for the `SelectInput`
gizmo called `variables` (tethys 'gizmos' are python shortcuts for creating html controls).

```python
all_gldas_variables = (
    ('Air Temperature', 'Tair_f_inst'),
    ('Canopy Water Amount', 'CanopInt_inst'),
    ('Downward Heat Flux In Soil', 'Qg_tavg'),
    ('Evaporation Flux From Canopy', 'ECanop_tavg'),
    ('Evaporation Flux From Soil', 'ESoil_tavg'),
    ('Potential Evaporation Flux', 'PotEvap_tavg'),
    ('Precipitation Flux', 'Rainf_f_tavg'),
    ('Rainfall Flux', 'Rainf_tavg'),
    ('Root Zone Soil Moisture', 'RootMoist_inst'),
    ('Snowfall Flux', 'Snowf_tavg'),
    ('Soil Temperature', 'SoilTMP0_10cm_inst'),
    ('Specific Humidity', 'Qair_f_inst'),
    ('Subsurface Runoff Amount', 'Qsb_acc'),
    ('Surface Air Pressure', 'Psurf_f_inst'),
    ('Surface Albedo', 'Albedo_inst'),
    ('Surface Downwelling Longwave Flux In Air', 'LWdown_f_tavg'),
    ('Surface Downwelling Shortwave Flux In Air', 'SWdown_f_tavg'),
    ('Surface Net Downward Longwave Flux', 'Lwnet_tavg'),
    ('Surface Net Downward Shortwave Flux', 'Swnet_tavg'),
    ('Surface Runoff Amount', 'Qs_acc'),
    ('Surface Snow Amount', 'SWE_inst'),
    ('Surface Snow Melt Amount', 'Qsm_acc'),
    ('Surface Snow Thickness', 'SnowDepth_inst'),
    ('Surface Temperature', 'AvgSurfT_inst'),
    ('Surface Upward Latent Heat Flux', 'Qle_tavg'),
    ('Surface Upward Sensible Heat Flux', 'Qh_tavg'),
    ('Transpiration Flux From Veg', 'Tveg_tavg'),
    ('Water Evaporation Flux', 'Evap_tavg'),
    ('Wind Speed', 'Wind_f_inst'),
)
```

When the tethys server restarts, open your app. Notice: there now are variables to choose from on the left menu.

## Step 7: Create python functions to extract the time series

There are many ways to extract a timeseries from gridded dataset which vary based on the programming lanuage, files 
format, and the kind of location/geometry for which to extract the series. I have created a python package which can 
handle many of these cases and has been optimized for speed; something particularly important in web apps. This should 
been installed when you installed the app. For the sake of simplicity in this workshop and given the time restraints, 
the app already contains the javascript you need to make the request for a timeseries from the user side. That code 
uses JQuery and is found in the main.js file. I have also included the code to create the plots of these timeseries in 
javascript. We need to provide the python code.

### Modify app.py

We need to create a new url which the user can use to request the time series. In tethys, this is called a 'UrlMap' and 
is done in app.py. Beginning on line 21, modify your url_maps function to match this code. It creates a new url within 
the app called request_time_series.

```python
def url_maps(self):
    """
    Add controllers
    """
    UrlMap = url_map_maker(self.root_url)

    return (
        UrlMap(
            name='home',
            url='multidimensional-series-template',
            controller='multidimensional_series_template.controllers.home'
        ),
        UrlMap(
            name='request_time_series',
            url='multidimensional-series-template/request_time_series',
            controller='multidimensional_series_template.controllers.request_time_series'
        ),
    )
``` 

### Modify home.html
In `home.html` on line about 100, there is a `<script>` tag where you can pass custom javascript to the user. We want 
this url to be accessible as a javascript variable so we need to create a new variable. Make it look like this:

```html
  <script>
    let threddsbase = "{{ thredds_url }}";
    let URL_requestTimeSeries = "{% url 'multidimensional_series_template:request_time_series' %}";
  </script>
``` 

### Create the python controller

in controllers.py, add a new function at the bottom of the file. This function name must be called request_time_series 
because that is the name we specified for this function in UrlMap in app.py.

```python
def request_time_series(request):
    # all the parameters sent by the user via javascript are in request.GET (compare with plotly.js)
    # print(request.GET)
    loc_type = request.GET.get('loc_type')
    variable = request.GET.get('variable')
    coords = request.GET.getlist('coords[]')

    # get a list of all the GLDAS files we put in the thredds directory via the custom setting
    path = App.get_custom_setting('thredds_path')
    list_of_files = sorted(glob.glob(os.path.join(path, '*.nc4')))

    # get the time series for the location the user chose
    # these functions return pandas dataframes with an index, datetime column, and columns of extracted values
    if loc_type == 'Point':
        time_series = geomatics.timeseries.point(
            files=list_of_files,
            var=variable,
            coords=(float(coords[0]), float(coords[1]),),
            dims=('lon', 'lat'),
            t_dim='time',
        )
    else:  # the other option was a bounding box
        time_series = geomatics.timeseries.bounding_box(
            files=list_of_files,
            var=variable,
            min_coords=(float(coords[0]), float(coords[1]),),
            max_coords=(float(coords[2]), float(coords[3]),),
            dims=('lon', 'lat'),
            t_dim='time',
        )

    # we need to build our own list of dates because the GLDAS netcdf files do not store their dates in typical
    # formats which can be automatically parsed by the python packages used to read the files. We can convert the
    # datetime values we got to their proper format using datetime and dateutil. Since there are only 12 dates and to
    # keep things simple for a workshop, I will just manually type the list of dates
    time_series['datetime'] = ['2019-01-01', '2019-02-01', '2019-03-01', '2019-04-01', '2019-05-01', '2019-06-01',
                               '2019-07-01', '2019-08-01', '2019-09-01', '2019-10-01', '2019-11-01', '2019-12-01', ]

    return JsonResponse({
        'x': time_series['datetime'].values.tolist(),
        'y': time_series['values'].values.tolist()
    })
```

## Step 8: Add javascript code to plot the results

Javascript files are stored in the `public/js` directory of the app. There is a file in there named plotly.js which 
contains all the custom functions used by the app to create graphs using plotly. Lets add a function to plot the series 
extracted by the python controller you wrote.
include this function in between the 

```javascript
function plotlyTimeseries(data) {
    let variable = $("#variables option:selected").text();
    let layout = {
        title: 'Timeseries of ' + variable,
        xaxis: {title: 'Time'},
        yaxis: {title: 'Values'}
    };

    let values = {
        x: data.x,
        y: data.y,
        mode: 'lines+markers',
        type: 'scatter'
    };
    Plotly.newPlot('chart', [values], layout);
    let chart = $("#chart");
    chart.css('height', 500);
    Plotly.Plots.resize(chart[0]);
}
```

## Step 9: Add javascript to save the plot as a csv

Add another function to plotly.js to save the chart as a csv and a listener which calls that function when the user 
pressed the button

```javascript
function chartToCSV() {
    function zip(arrays) {
        return arrays[0].map(function (_, i) {
            return arrays.map(function (array) {
                return array[i]
            })
        });
    }
    if (chartdata === null) {
        alert('There is no data in the chart. Please plot some data first.');
        return
    }
    let data = zip([chartdata.x, chartdata.y]);
    let csv = "data:text/csv;charset=utf-8," + data.map(e => e.join(",")).join("\n");
    let link = document.createElement('a');
    link.setAttribute('href', encodeURI(csv));
    link.setAttribute('target', '_blank');
    link.setAttribute('download', 'extracted_time_series.csv');
    document.body.appendChild(link);
    link.click();
    $("#a").remove()
}

// WHEN YOU CLICK ON THE DOWNLOAD BUTTON- RUN THE DOWNLOAD CSV FUNCTION
$("#chartCSV").click(function () {chartToCSV()});
```  




