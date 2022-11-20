#!/usr/bin/python

import serial
import modbus_tk
from modbus_tk import utils
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from time import sleep
import argparse 




def main():
    
    logger = modbus_tk.utils.create_logger("console")
    #take input of user for  request parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", type=str, required=True,
                   help="serial port, defaults to /dev/ttyUSB0")
    parser.add_argument("-b","--baudrate", type=str, required=True,
                   help="baudrate, defaults to 9600")
    
    args = parser.parse_args()
    
    #initialize parameters for request with user input or default values
    PORT = args.port              
    BAUDRATE = args.baudrate              

    try:   
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(0.5)
    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())
    except Exception as exc:
        logger.error(exc)


    slaveID = 1
    while slaveID < 255: #execute number of requests,calculate roundtrip for each cycle and total time,store things in csv file
        try:
            master.execute(slaveID, cst.READ_INPUT_REGISTERS, 10, 1)
            logger.info("slave id found to be: %d", slaveID)
            break
        except modbus_tk.modbus.ModbusError as exc:
            logger.info("slave id found to be: %d", slaveID)
            break
        except modbus_tk.modbus.ModbusInvalidResponseError:
            logger.error("No response from bus address: %d", slaveID)

        slaveID = slaveID + 1

        
            
        

if __name__ == "__main__":
    main()