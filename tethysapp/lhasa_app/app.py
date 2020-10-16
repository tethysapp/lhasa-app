from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class LhasaApp(TethysAppBase):
    """
    Lhasa App Class
    """

    name = 'LHASA'
    index = 'lhasa_app:home'
    icon = 'lhasa_app/images/flaglogo.jpg'
    package = 'lhasa_app'
    root_url = 'lhasa-app'
    color = '#27ae60'
    description = 'An app demonstrating the nowcast for landslide susceptibility using precipitation data and terrain susceptibility'
    tags = '"landslide", "nowcast", "NASA"'
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
        )
