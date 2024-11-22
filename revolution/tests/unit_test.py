import unittest
from unittest.mock import MagicMock
from revolution.contexts import Contexts
from revolution.settings import Settings
from revolution.peripheries import Peripheries
from revolution.environment import Environment
from revolution.application import Application
from revolution.miscellaneous import Miscellaneous


class TestMiscellaneousControls(unittest.TestCase):
    def setUp(self):
        self.contexts = Contexts(
            miscellaneous_left_indicator_light_status_input=False,
            miscellaneous_right_indicator_light_status_input=False,
            miscellaneous_hazard_lights_status_input=False,
            miscellaneous_daytime_running_lights_status_input=False,
            miscellaneous_horn_status_input=False,
            miscellaneous_backup_camera_control_status_input=False,
            miscellaneous_display_backlight_status_input=False,
            miscellaneous_brake_status_input=False,
        )

        self.peripheries = Peripheries(
            miscellaneous_indicator_lights_pwm=MagicMock(),
            miscellaneous_left_indicator_light_pwm=MagicMock(),
            miscellaneous_right_indicator_light_pwm=MagicMock(),
            miscellaneous_daytime_running_lights_pwm=MagicMock(),
            miscellaneous_brake_lights_pwm=MagicMock(),
            miscellaneous_horn_switch_gpio=MagicMock(),
            miscellaneous_backup_camera_control_switch_gpio=MagicMock(),
            miscellaneous_display_backlight_switch_gpio=MagicMock(),
        )

        self.settings = Settings(
            miscellaneous_light_timeout=0.1,
        )

        self.environment = Environment(
            contexts=self.contexts,
            peripheries=self.peripheries,
            settings=self.settings,
        )

        self.application = Miscellaneous(self.environment)

    def test_controls_toggle_correctly(self):
        self.contexts.miscellaneous_left_indicator_light_status_input = True
        self.application._light()
        self.peripheries.miscellaneous_left_indicator_light_pwm.enable.assert_called_once()
        
        self.contexts.miscellaneous_left_indicator_light_status_input = False
        self.application._light()
        self.peripheries.miscellaneous_left_indicator_light_pwm.disable.assert_called_once()
        
        self.contexts.miscellaneous_daytime_running_lights_status_input = True
        self.application._light()
        self.peripheries.miscellaneous_daytime_running_lights_pwm.enable.assert_called_once()

        self.contexts.miscellaneous_daytime_running_lights_status_input = False
        self.application._light()
        self.peripheries.miscellaneous_daytime_running_lights_pwm.disable.assert_called_once()

        self.contexts.miscellaneous_horn_status_input = True
        self.application._light()
        self.peripheries.miscellaneous_horn_switch_gpio.write.assert_called_with(True)

        self.contexts.miscellaneous_backup_camera_control_status_input = True
        self.application._light()
        self.peripheries.miscellaneous_backup_camera_control_switch_gpio.write.assert_called_with(True)

        self.contexts.miscellaneous_brake_status_input = True
        self.application._light()
        self.peripheries.miscellaneous_brake_lights_pwm.enable.assert_called_once()

        self.contexts.miscellaneous_brake_status_input = False
        self.application._light()
        self.peripheries.miscellaneous_brake_lights_pwm.disable.assert_called_once()

    def tearDown(self):
        self.application._teardown()


if __name__ == '__main__':
    unittest.main()
