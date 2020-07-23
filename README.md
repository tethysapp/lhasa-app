# Multidimensional Data Series Template

This is a tethys app for demonstrating the steps you need to program in order to:
1. Show animated maps of raster data via open source tools (THREDDS Data Server)
2. Extract time series of values from the multidimensional raster files in a web app environment 

© Riley Hales, 2020. Developed at the BYU Hydroinformatics Lab for a SERVIR Hackathon event August 2020

## Step 0: Prerequisites and Recommendations

1. I would highly recommend you use an IDE (integrated development environment) for this exercise. PyCharm has a free version which is excellent.
2. You need to have installed tethys via and activated the tethys environment in your bash shell (http://docs.tethysplatform.org/en/stable/installation.html)
3. You need access to the Docker CLI (https://docs.docker.com/desktop/). Preferably, you have pulled the image for THREDDS Data server (`docker pull unidata/thredds-docker:latest`)

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
git clone https://github.com/rileyhales/multidimenstional_series_template
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

While several options are available for showing raster data on maps in web pages, the best free option for showing
animations of raster data is the THREDDS Data Server. THREDDS is compatible with netCDF files that conform to the 
Unidata Common Data Model which has been widely adopted (https://www.unidata.ucar.edu/software/netcdf-java/v4.6/CDM/index.html).
Your data MUST be netcdf files conforming to this standard. Raster data of most formats can be quickly converted to netCDF. 
If you want your data to be shown in animated maps, you will need to commit the time to making your data meet these 2 
requirements (if it is not already in that format).

We need to install THREDDS in order to view our raster data. We also need the THREDDS container to have access to the 
`~/spatialdata/thredds` directory so we will mount that directory 

```bash
cd ~/spatialdata/thredds/
docker run --name thredds -v $PWD:/usr/local/tomcat/content/thredds/public/ -d -p 7000:8080 unidata/thredds-docker:latest
```
You can check on the docker container with `docker ps`. When the container is started, open a web page and go to 
127.0.0.1:7000/thredds/catalog.html. The capabilities of the THREDDS server are managed by a few configuration XML 
files which we will now modify.

```bash
docker exec -it thredds bash
cd content/thredds/
vi catalog.xml
```

Uncomment out the lines for the 3 services at the top and modify the wildcard filters to include *

```bash
docker restart thredds
``` 

## Step 5: Configure the tethys app to use THREDDS


