import click

from .loadstar_sensors_interface import LoadstarSensorsInterface, ScaleFactor

@click.command()
@click.option('--port', default=None, help='USB port')
@click.option('--tare/--no-tare', default=False)
@click.option('--scale-factor',
              type=click.Choice(list([sf.name for sf in ScaleFactor]),
                                case_sensitive=False),
              default=ScaleFactor.ONE.name)
def main(port,tare,scale_factor):
    dev = LoadstarSensorsInterface(port=port)
    dev.set_scale_factor(scale_factor)

    dev.print_device_info()

    if tare:
        print('taring...')
        dev.tare()


if __name__ == '__main__':
    main()
