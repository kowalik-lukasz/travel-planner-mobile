from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog


class GPSHelper:
    has_centered_map = False

    def run(self):
        # reference to blinker
        gps_blinker = App.get_running_app().root.ids.mapview.ids.blinker
        # start blinking
        gps_blinker.blink()

        # permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                else:
                    print("Did not get all permissions")

                request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])

        # GPS config
        if platform == 'android' or platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position,
                          on_status=self.on_auth_status)
            gps.start(minTime=1000, minDistance=0)

    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        print("GPS POSITION ", my_lat, my_lon)
        gps_blinker = App.get_running_app().root.ids.mapview.ids.blinker
        gps_blinker.lat = my_lat
        gps_blinker.lon = my_lon

        # center on gps
        if not self.has_centered_map:
            map = App.get_running_app().root.ids.mapview
            map.center_on(my_lat, my_lon)
            has_centered_map = True

    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()
