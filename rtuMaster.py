#!/usr/bin/python

import sys
import serial
import modbus_tk
from modbus_tk import utils
import argparse 
from time import sleep
import struct
PY2 = sys.version_info[0] == 2
def get_log_buffer(prefix, buff):
    """Format binary data into a string for debug purpose"""
    log = prefix
    for i in buff:
        log += str(hex(ord(i)).split('x')[-1] if PY2 else i) + "-"
    return log[:-1]

module = sys.modules['modbus_tk.utils']
module.get_log_buffer = get_log_buffer
sys.modules['modbus_tk.utils'] = module

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from modbus_tk import modbus_tcp



def main():
    
    logger = modbus_tk.utils.create_logger("console")
    #take input of user for  request parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", type=str, required=True,
                   help="serial port, defaults to /dev/ttyUSB0")
    parser.add_argument("-b","--baudrate", type=str, required=True,
                   help="baudrate, defaults to 9600")
    parser.add_argument("-a","--slave",type=int,required=True,
                   help="address of the slave")
    parser.add_argument("-r","--address", type=int,required=True,
                   help="address of first register to access in decimal integer")
    parser.add_argument("-f","--function", type=int, choices=[3,4,6,16],required=True,
                   help="modbus function code")
    parser.add_argument("-c","--length", type=int, default=1, 
                   help="integer count of registers to access, defaults to 1")
    parser.add_argument("-s","--samples", type=int, default=1,
                   help="integer number of samples to poll, defaults to 1")
    parser.add_argument("-i","--interval", type=int, default=1,
                   help="integer seconds for interval between polls, defaults to 1")
    parser.add_argument("-t","--type", type=str, choices=['f','i'],
                        help="type of data for 32bit, f for float, i for integer")
    parser.add_argument("-e","--endian", type=str, default='b',choices=['b', 'l'],
                   help="defaults to big endian, set to 'l' for little endian")
    parser.add_argument("-v","--value", type=str, nargs='+',
                   help="Values to write in decimal")
    
    args = parser.parse_args()
    
    #initialize parameters for request with user input or default values
    PORT = args.port              
    BAUDRATE = args.baudrate              
    SLAVE_ADDRESS = args.slave
    STARTING_ADDRESS = args.address
    LENGTH = args.length
    SAMPLES = args.samples
    INTERVAL = args.interval
    MODBUS_FUNCTION = args.function
    TYPE = args.type
    ENDIANESS = args.endian
    VALUE = args.value

    # pick type of register from library based on input
    if MODBUS_FUNCTION == 3:
        modbus_function = cst.READ_HOLDING_REGISTERS
        modbus_function_info = "Read Holding Registers"
    elif MODBUS_FUNCTION == 4:
        modbus_function = cst.READ_INPUT_REGISTERS
        modbus_function_info = "Read Input Registers"
    elif MODBUS_FUNCTION == 6:
        modbus_function = cst.WRITE_SINGLE_REGISTER
        modbus_function_info = "Write single holding register"
    elif MODBUS_FUNCTION == 16:
        modbus_function = cst.WRITE_MULTIPLE_REGISTERS
        modbus_function_info = "Write multiple holding registers"
    
    
    
    # pick endianess based on input, defaults to big
    if ENDIANESS == 'l':
        endianess_info = "Little"
        endianess_char = '<'
    elif ENDIANESS == 'b':
        endianess_char = '>'
        endianess_info = "Big"
    
    # pick type based on input, defaults to short

        
    if TYPE:
        if TYPE == 'f':
            type_info = "FLOAT32"
        elif TYPE == 'i':
            type_info = "INT32"
        data_format = endianess_char + TYPE
    else:
        type_info = "UINT16"
        data_format = endianess_char + LENGTH*'H'
        
    
    print("Trying for: ")
    print("Port: " + PORT)
    print("Baudrate: " + str(BAUDRATE))
    print("Slave address: " + str(SLAVE_ADDRESS))
    print("Starting address address: " + str(STARTING_ADDRESS))
    print("Registers to request: " + str(LENGTH))
    print("Modbus function: " + modbus_function_info)
    print("Format: " + type_info)
    print("Endianess: " + endianess_info)
    print("*"*50)
    
    
            
    try:   
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(2.0)
        master.set_verbose(True)
    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())
        sys.exit()

    if MODBUS_FUNCTION in [3, 4]:
        try:
            polled = 0
            while polled < SAMPLES: #execute number of requests,calculate roundtrip for each cycle and total time,store things in csv file
                a=master.execute(SLAVE_ADDRESS, modbus_function, STARTING_ADDRESS, LENGTH, data_format=data_format)
                logger.info(a)
                sleep(INTERVAL)
                polled = polled + 1
        except modbus_tk.modbus.ModbusError as exc:
            logger.error("%s- Code=%d", exc, exc.get_exception_code())
        except struct.error:
            logger.error("Data format and endianess can't be applied to the chosen length of registers")
            logger.error("Check usage with -h flag on script call.")
    elif MODBUS_FUNCTION in [6, 16]:
        if not VALUE:
            logger.error("No values to write were found.")
            logger.error("Check usage with -h flag on script call.")
            sys.exit()
        if not TYPE:
            logger.error("No format was selected.")
            logger.error("Check usage with -h flag on script call.")
            sys.exit()


        if TYPE == 'f':
            if MODBUS_FUNCTION == 16:
                values = [float(value) for value in VALUE]
            elif MODBUS_FUNCTION == 6:
                values = float(VALUE[0])
        elif TYPE == 'i':
            if MODBUS_FUNCTION == 16:
                values = [int(value) for value in VALUE]
            elif MODBUS_FUNCTION == 6:
                values = int(VALUE[0])
    
        a=master.execute(SLAVE_ADDRESS, modbus_function, STARTING_ADDRESS, LENGTH, output_value=values)

        
            
        

if __name__ == "__main__":
    main()