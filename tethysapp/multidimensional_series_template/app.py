from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


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
            UrlMap(
                name='request_time_series',
                url='multidimensional-series-template/request_time_series',
                controller='multidimensional_series_template.controllers.request_time_series'
            ),
        )

    def custom_settings(self):
        return (
            CustomSetting(
                name='thredds_path',
                type=CustomSetting.TYPE_STRING,
                description="Local file path to datasets (same as used by Thredds) "
                            "(e.g.~/spatialdata/thredds/timeseries-workshop)",
                required=True,
                # default='~/spatialdata/thredds/timeseries-workshop'
            ),
            CustomSetting(
                name='thredds_url',
                type=CustomSetting.TYPE_STRING,
                description="URL to the GLDAS folder on the thredds server with trailing / "
                            "(e.g. http://127.0.0.1:7000/thredds/)",
                required=True,
                default='http://127.0.0.1:7000/thredds/wms/thredds-demo/timeseries-workshop/',
            )
        )
