from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider
from tethys_sdk.permissions import login_required

from .app import MultidimensionalSeriesTemplate as App


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

        # metadata
        'thredds_url': App.get_custom_setting('thredds_url'),
    }

    return render(request, 'multidimensional_series_template/home.html', context)
