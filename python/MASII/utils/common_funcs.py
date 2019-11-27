import logging
import os, sys
import psutil
import serial

def unimplemented(func):
    '''
    A decorator function for print the current running function's name
    Just for the debug process. 
    '''
    def wrap_func(*args, **kwargs):               
        logging.info('{}({}) is not implemented.'.format(func.__name__, args))
        func(*args, **kwargs)
    return wrap_func


def show_memory_info(hint):
    '''
    Show memory used by current 
    '''
    pid = os.getpid()
    p = psutil.Process(pid)
    
    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    logging.info('{} memory used: {} MB'.format(hint, memory))

def list_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result    


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='/domain-result.log',
                        filemode='w')
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)  
    list_1 = (i for i in range(100000))
    show_memory_info('After generated list_1')
    cwd = os.getcwd()
    print('current dir is ' + cwd)
    new_path = os.path.join(cwd, "nw")
    print('new dir is ' + new_path)
    
    logging.info(list_serial_ports())
    
