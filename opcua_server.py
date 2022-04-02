# https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/server-example.py
import logging
import asyncio
import sys
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod

from serial_manager import SerialManager

serial = SerialManager()

@uamethod
def send_command(parent, command):
    return serial.send_command(command)    


async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/freeopcua/server/')

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