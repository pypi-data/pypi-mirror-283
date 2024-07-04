from time import sleep

import click
import serial

from zhixin.device.finder import SerialPortFinder
from zhixin.exception import UserSideException


class SerialTestOutputReader:
    SERIAL_TIMEOUT = 600

    def __init__(self, test_runner):
        self.test_runner = test_runner

    def begin(self):
        click.echo(
            "If you don't see any output for the first 10 secs, "
            "please reset board (press reset button)"
        )
        click.echo()

        try:
            ser = serial.serial_for_url(
                self.resolve_test_port(),
                do_not_open=True,
                baudrate=self.test_runner.get_test_speed(),
                timeout=self.SERIAL_TIMEOUT,
            )
            ser.rts = self.test_runner.options.monitor_rts
            ser.dtr = self.test_runner.options.monitor_dtr
            ser.open()
        except serial.SerialException as exc:
            click.secho(str(exc), fg="red", err=True)
            return

        if not self.test_runner.options.no_reset:
            ser.flushInput()
            ser.setDTR(False)
            ser.setRTS(False)
            sleep(0.1)
            ser.setDTR(True)
            ser.setRTS(True)
            sleep(0.1)

        while not self.test_runner.test_suite.is_finished():
            self.test_runner.on_testing_data_output(ser.read(ser.in_waiting or 1))
        ser.close()

    def resolve_test_port(self):
        project_options = self.test_runner.project_config.items(
            env=self.test_runner.test_suite.env_name, as_dict=True
        )
        port = SerialPortFinder(
            board_config=self.test_runner.platform.board_config(
                project_options["board"]
            ),
            upload_protocol=project_options.get("upload_protocol"),
            ensure_ready=True,
            verbose=self.test_runner.options.verbose,
        ).find(initial_port=self.test_runner.get_test_port())
        if port:
            return port
        raise UserSideException(
            "Please specify `test_port` for environment or use "
            "global `--test-port` option."
        )
