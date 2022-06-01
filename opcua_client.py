import asyncio
import logging
import asyncua
import argparse

parser = argparse.ArgumentParser(description='Options for initializing client.')
parser.add_argument('-p', '--port', help='Port number', type=str, default='4840')
parser.add_argument('--ip', help='IP address', type=str, default='localhost')
parser.add_argument('-f', '--file', help='File of commands', type=str, default='')
parser.add_argument('-o', '--output', help='Save response to file', type=str, default='')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

def opcua_settings(url, ip, port, uri, idx, var):
    print('-----------------------------------------------------------------------')
    print('Settings:')
    print(f'\turl: {url}')
    print(f'\t\tIP: {ip}')
    print(f'\t\tPort: {port}')
    print(f'\turi: {uri}')
    print(f'\tidx: {idx}')
    print(f'\tvar: {var}')
    print('-----------------------------------------------------------------------')

async def main():
    quit = False
    url = f'opc.tcp://{args.ip}:{args.port}/'

    async with asyncua.Client(url=url) as client:
        _logger.info('Children of root are: %r', await client.nodes.root.get_children())

        uri = 'http://examples.freeopcua.github.io'
        idx = await client.get_namespace_index(uri)
        var = await client.nodes.root.get_child(['0:Objects'])

        # send list of commands from file 
        if args.file:
            result = ''
            try:
                file = open(args.file, 'r')
                if args.output:
                    log_file = open(args.output, 'w')
            except:
                raise Exception('Could not open file!')
            # read each line/command from input file  
            for command in file:
                _logger.info(f'Sending comand: {command}')
                # send command to server 
                try:
                    result = await var.call_method(f'{idx}:ServerMethod', command.strip())
                    _logger.info('Server method returned: %s', result)
                    print(result)
                except Exception as e:
                    _logger.error(e)
                # save command and response to output file 
                if args.output:
                    log_file.write(f'> {command}\n')
                    log_file.write(f'{result}\n')
            if args.file:
                file.close()
                if args.output:
                    log_file.close()
        # run command line interface for user input
        else:
            opcua_settings(url, args.ip, args.port, uri, idx, var)
            print('Type command or \'quit\' to exit.\n')
            # 
            while quit is not True:
                command = input('> ')

                if command.strip() == 'quit':
                    quit = True
                else:
                    try:
                        result = await var.call_method(f'{idx}:ServerMethod', command)
                        _logger.info('Method result is: %s', result)
                        print(result)
                    except Exception as e:
                        _logger.error(e)

if __name__ == '__main__':
    asyncio.run(main())
