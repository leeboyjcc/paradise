import getopt
import ipaddress
import socket
import sys

def err():
    print('Parameter Error')
    sys.exit(1)

def paraparse():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ["host=", "port="])
    except getopt.GetoptError:
        err()
    for option, optvalue in opts:
        if option == '--host':
            try:
                ipaddress.ip_address(optvalue)
                addr = optvalue.strip()
            except ValueError:
                err()
        elif option == '--port':
            if '-' not in optvalue:
                try:
                    port = int(optvalue)
                except ValueError:
                    err()
                ports = [port]
            else:
                portlist= [item for item in optvalue.split('-')]
                try:
                    port1 = int(optvalue.split('-')[0])
                    port2 = int(optvalue.split('-')[1])
                except ValueError:
                    err()
                ports = list(range(port1, port2+1))
        else:
            assert False, 'Parameter Error'

    return addr, ports

def main():
    addr, ports = paraparse()
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((addr, port))
        if result == 0:
            print('{} open'.format(port))
        else:
            print('{} closed'.format(port))
        sock.close()
if __name__=='__main__':
    main()
