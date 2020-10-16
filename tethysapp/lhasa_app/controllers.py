from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider
from tethys_sdk.permissions import login_required


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
        display_text='Select a Dataset',
        name='variables',
        multiple=False,
        original=True,
        options=(('GPM IMERG 30 min Precip. Accumulation', 'Tair_f_inst'),
                 ('GPM IMERG 3 hour Precip. Accumulation', 'CanopInt_inst'),
                 ('GPM IMERG 1 day Precip. Accumulation', 'Qg_tavg'),
                 ('GPM IMERG 3 day Precip. Accumulation', 'ECanop_tavg'),
                 ('GPM IMERG 7 day Precip. Accumulation', 'ESoil_tavg'),
                 ('Global Landslide Nowcast', 'PotEvap_tavg'),
                 ('Global Landslide Nowcast updated every 3 hours', 'Rainf_f_tavg')),
    )
    states = SelectInput(
        display_text='Pick A State (ESRI Living Atlas)',
        name='states',
        multiple=False,
        original=True,
        options=(('Brasil', ''),
                 ('Acre', 'Acre'),
                 ('Alagoas', 'Alagoas'),
                 ('Amapa', 'Amapa'),
                 ('Amazonas', 'Amazonas'),
                 ('Bahia', 'Bahia'),
                 ('Ceara', 'Ceara'),
                 ('Distrito Federal', 'Distrito Federal'),
                 ('Espirito Santo', 'Espirito Santo'),
                 ('Goias', 'Goias'),
                 ('Maranhao', 'Maranhao'),
                 ('Mato Grosso', 'Mato Grosso'),
                 ('Mato Grosso do Sul', 'Mato Grosso do Sul'),
                 ('Minas Gerais', 'Minas Gerais'),
                 ('Para', 'Para'),
                 ('Paraiba', 'Paraiba'),
                 ('Parana', 'Parana'),
                 ('Pernambuco', 'Pernambuco'),
                 ('Piaui', 'Piaui'),
                 ('Rio de Janeiro', 'Rio de Janeiro'),
                 ('Rio Grande do Norte', 'Rio Grande do Norte'),
                 ('Rio Grande do Sul', 'Rio Grande do Sul'),
                 ('Rodonia', 'Rodonia'),
                 ('Roraima', 'Roraima'),
                 ('Santa Catarina', 'Santa Catarina'),
                 ('Sao Paulo', 'Sao Paulo'),
                 ('Sergipe', 'Sergipe'),
                 ('Toncantins', 'Toncantins'),
                 ('None', 'none'),)
    )
    regions = SelectInput(
        display_text='Pick A World Region (ESRI Living Atlas)',
        name='regions',
        multiple=False,
        original=True,
        options=(('Brasil', ''),
                 ('Acre', 'Acre'),
                 ('Alagoas', 'Alagoas'),
                 ('Amapa', 'Australia/New Zealand'),
                 ('Amazonas', 'Amazonas'),
                 ('Bahia', 'Central America'),
                 ('Ceara', 'Central Asia'),
                 ('Distrito Federal', 'Eastern Africa'),
                 ('Espirito Santo', 'Eastern Asia'),
                 ('Goias', 'Eastern Europe'),
                 ('Maranhao', 'European Russia'),
                 ('Mato Grosso', 'Melanesia'),
                 ('Mato Grosso do Sul', 'Micronesia'),
                 ('Minas Gerais', 'Middle Africa'),
                 ('Para', 'Northern Africa'),
                 ('Paraiba', 'Northern America'),
                 ('Parana', 'Northern Europe'),
                 ('Pernambuco', 'Polynesia'),
                 ('Piaui', 'South America'),
                 ('Rio de Janeiro', 'Southeastern Asia'),
                 ('Rio Grande do Norte', 'Southern Africa'),
                 ('Rio Grande do Sul', 'Southern Asia'),
                 ('Rodonia', 'Southern Europe'),
                 ('Roraima', 'Western Africa'),
                 ('Santa Catarina', 'Western Asia'),
                 ('Sao Paulo', 'Western Europe'),
                 ('Sergipe', 'none'),
                 ('Toncantins', 'npne'),
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
        'states': states,
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
