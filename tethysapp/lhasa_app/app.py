from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class LhasaApp(TethysAppBase):
    """
    Tethys app class for Multidimensional Series Template.
    """

    name = 'LHASA'
    index = 'lhasa_app:home'
    icon = 'lhasa_app/images/icon.gif'
    package = 'lhasa_app'
    root_url = 'lhasa-app'
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
                url='lhasa-app',
                controller='lhasa_app.controllers.home'
            ),
            # UrlMap(
            #     name='request_time_series',
            #     url='multidimensional-series-template/request_time_series',
            #     controller='lhasa_app.controllers.request_time_series'
            # ),
        )
