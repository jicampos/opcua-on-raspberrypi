import sys
import argparse
import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.methods import uamethod

from serial_manager import SerialManager

parser = argparse.ArgumentParser(description='Options for initializing server.')
parser.add_argument('-p', '--port', help='Port number', type=str, default='4840')
parser.add_argument('--ip', help='IP address', type=str, default='0.0.0.0')
parser.add_argument('--serial-port', help='Path to serial port from root', type=str, default='/dev/ttyUSB1')
args = parser.parse_args()

serial = SerialManager(port=args.serial_port)


@uamethod
def send_command(parent, command):
    return serial.send_command(command)


async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint(f'opc.tcp://{args.ip}:{args.port}') 

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), send_command, [ua.VariantType.String], [ua.VariantType.String])
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
