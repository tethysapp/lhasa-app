from tethys_sdk.base import TethysAppBase, url_map_maker


class MultidimensionalSeriesTemplate(TethysAppBase):
    """
    Tethys app class for Multidimensional Series Template.
    """

    name = 'Multidimensional Series Template'
    index = 'multidimensional_series_template:home'
    icon = 'multidimensional_series_template/images/icon.gif'
    package = 'multidimensional_series_template'
    root_url = 'multidimensional-series-template'
    color = '#27ae60'
    description = 'An app demonstrating the steps to show timeseries raster data and extract timeseries files'
    tags = '"time series", "raster", "GIS"'
    enable_feedback = False
    feedback_emails = []

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
        )
