# https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/client-example.py
import asyncio
import sys
# sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua

# logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    quit = False
    url = 'opc.tcp://localhost:4840/freeopcua/server/'
    async with Client(url=url) as client:
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        # Node objects have methods to read and write node attributes as well as browse or populate address space
        _logger.info('Children of root are: %r', await client.nodes.root.get_children())

        uri = 'http://examples.freeopcua.github.io'
        idx = await client.get_namespace_index(uri)
        
        var = await client.nodes.root.get_child(["0:Objects"])

        print('-----------------------------------------------------------------------')
        print('Settings:')
        print(f'\turl: {url}')
        print(f'\turi: {uri}')
        print(f'\tidx: {idx}')
        print(f'\tvar: {var}')
        print('-----------------------------------------------------------------------')
        print('Type command or \'quit\' to exit.\n')

        while quit is not True:
            command = input('> ')
            
            if command == '':
                command = 'RD AFE 0 REG 1'
            if command.strip() == 'quit':
                quit = True
            else:
                try:
                    result = await var.call_method(f"{idx}:ServerMethod", command)
                    _logger.info('Method result is: %s', result)
                    print(result)
                except Exception as e:
                    _logger.error(e)


if __name__ == '__main__':
    asyncio.run(main())
