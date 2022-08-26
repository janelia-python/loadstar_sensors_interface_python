import click

from .loadstar_sensors_interface import LoadstarSensorsInterface

@click.command()
@click.option('--port', default=None, help='USB port')
@click.option('--tare/--no-tare', default=False)
def main(port,tare):
    dev = LoadstarSensorsInterface(port=port)
    device_model = dev.get_device_model()
    device_id = dev.get_device_id()
    print('Found device model {0} with ID {0}'.format(device_model,
                                                      device_id))
    if tare:
        print('taring...')
        dev.tare()

if __name__ == '__main__':
    main()
