import glob
import os

import geomatics
from django.http import JsonResponse
from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider
from tethys_sdk.permissions import login_required

from .app import LhasaApp as App


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    geojson_colors = [('White', '#ffffff'),
                      ('Transparent', 'rgb(0,0,0,0)'),
                      ('Red', '#ff0000'),
                      ('Green', '#00ff00'),
                      ('Blue', '#0000ff'),
                      ('Black', '#000000'),
                      ('Pink', '#ff69b4'),
                      ('Orange', '#ffa500'),
                      ('Teal', '#008080'),
                      ('Purple', '#800080'), ]

    variables = SelectInput(
        display_text='Select GLDAS Variable',
        name='variables',
        multiple=False,
        original=True,
        options=(('Air Temperature', 'Tair_f_inst'),
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
                 ('Wind Speed', 'Wind_f_inst')),
    )

    regions = SelectInput(
        display_text='Pick A World Region (ESRI Living Atlas)',
        name='regions',
        multiple=False,
        original=True,
        options=(('All World Regions', ''),
                 ('Antarctica', 'Antarctica'),
                 ('Asiatic Russia', 'Asiatic Russia'),
                 ('Australia/New Zealand', 'Australia/New Zealand'),
                 ('Caribbean', 'Caribbean'),
                 ('Central America', 'Central America'),
                 ('Central Asia', 'Central Asia'),
                 ('Eastern Africa', 'Eastern Africa'),
                 ('Eastern Asia', 'Eastern Asia'),
                 ('Eastern Europe', 'Eastern Europe'),
                 ('European Russia', 'European Russia'),
                 ('Melanesia', 'Melanesia'),
                 ('Micronesia', 'Micronesia'),
                 ('Middle Africa', 'Middle Africa'),
                 ('Northern Africa', 'Northern Africa'),
                 ('Northern America', 'Northern America'),
                 ('Northern Europe', 'Northern Europe'),
                 ('Polynesia', 'Polynesia'),
                 ('South America', 'South America'),
                 ('Southeastern Asia', 'Southeastern Asia'),
                 ('Southern Africa', 'Southern Africa'),
                 ('Southern Asia', 'Southern Asia'),
                 ('Southern Europe', 'Southern Europe'),
                 ('Western Africa', 'Western Africa'),
                 ('Western Asia', 'Western Asia'),
                 ('Western Europe', 'Western Europe'),
                 ('None', 'none'),)
    )

    colorscheme = SelectInput(
        display_text='GLDAS Raster Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=(('SST-36', 'sst_36'),
                 ('Greyscale', 'greyscale'),
                 ('Rainbow', 'rainbow'),
                 ('OCCAM', 'occam'),
                 ('OCCAM Pastel', 'occam_pastel-30'),
                 ('Red-Blue', 'redblue'),
                 ('NetCDF Viewer', 'ncview'),
                 ('ALG', 'alg'),
                 ('ALG 2', 'alg2'),
                 ('Ferret', 'ferret'),),
        initial='rainbow'
    )

    opacity = RangeSlider(
        display_text='GLDAS Layer Opacity',
        name='opacity',
        min=.5,
        max=1,
        step=.05,
        initial=1,
    )

    gj_color = SelectInput(
        display_text='Boundary Border Colors',
        name='gjClr',
        multiple=False,
        original=True,
        options=geojson_colors,
        initial='#ffffff'
    )

    gj_opacity = RangeSlider(
        display_text='Boundary Border Opacity',
        name='gjOp',
        min=0,
        max=1,
        step=.1,
        initial=1,
    )

    gj_weight = RangeSlider(
        display_text='Boundary Border Thickness',
        name='gjWt',
        min=1,
        max=5,
        step=1,
        initial=2,
    )

    gj_fillcolor = SelectInput(
        display_text='Boundary Fill Color',
        name='gjFlClr',
        multiple=False,
        original=True,
        options=geojson_colors,
        initial='rgb(0,0,0,0)'
    )

    gj_fillopacity = RangeSlider(
        display_text='Boundary Fill Opacity',
        name='gjFlOp',
        min=0,
        max=1,
        step=.1,
        initial=.5,
    )

    context = {
        # data options
        'variables': variables,
        'regions': regions,

        # display options
        'colorscheme': colorscheme,
        'opacity': opacity,
        'gjClr': gj_color,
        'gjOp': gj_opacity,
        'gjWt': gj_weight,
        'gjFlClr': gj_fillcolor,
        'gjFlOp': gj_fillopacity,


    }

    return render(request, 'lhasa_app/home.html', context)


def request_time_series(request):
    # all the parameters sent by the user via javascript are in request.GET (compare with plotly.js)
    # print(request.GET)
    loc_type = request.GET.get('loc_type')
    variable = request.GET.get('variable')
    coords = request.GET.getlist('coords[]')

    # get a list of all the GLDAS files we put in the thredds directory via the custom setting
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
