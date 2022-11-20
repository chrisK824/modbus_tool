### Installation

```
cd modbustool
pip install -r requirements.txt
```

### Usage

Usage can be shown anytime by running `python rtuMaster.py -h`

```
python rtuMaster.py -h
usage: rtuMaster.py [-h] -p PORT -b BAUDRATE -a SLAVE -r ADDRESS -f {3,4,6,16}
                    [-c LENGTH] [-s SAMPLES] [-i INTERVAL] [-t {f,i}]
                    [-e {b,l}] [-v VALUE [VALUE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  serial port, defaults to /dev/ttyUSB0
  -b BAUDRATE, --baudrate BAUDRATE
                        baudrate, defaults to 9600
  -a SLAVE, --slave SLAVE
                        address of the slave
  -r ADDRESS, --address ADDRESS
                        address of first register to access in decimal integer
  -f {3,4,6,16}, --function {3,4,6,16}
                        modbus function code
  -c LENGTH, --length LENGTH
                        integer count of registers to access, defaults to 1
  -s SAMPLES, --samples SAMPLES
                        integer number of samples to poll, defaults to 1
  -i INTERVAL, --interval INTERVAL
                        integer seconds for interval between polls, defaults
                        to 1
  -t {f,i}, --type {f,i}
                        type of data for 32bit, f for float, i for integer
  -e {b,l}, --endian {b,l}
                        defaults to big endian, set to 'l' for little endian
  -v VALUE [VALUE ...], --value VALUE [VALUE ...]
                        Values to write in decimal

```

### Options explanations
| Argument | Input Pool | Description |
| ------ | ------ | ------ |
| -p | ports of device e.g '/dev/ttyUSB0'  | port of the device where the modbus slave is connected |
| -b | integer typical numbers for serial baudrate e.g `9600` | baudrate of the serial communication |
| -a | integer 1-255 | bus address of the slave device |
| -r | integer | starting register address to poll, in decimal |
| -f | integer of  [`3`, `4`, `6`, `16`] | Modbus function:
                                    |||`3`: Read holding register
                                    |||`4`: Read input register
	                                |||`6`: Write single holding register
	                                |||`16`: Write multiple holding registers|
| -c | integer | number of registers to access, read or write, defaults to 1 |
| -s | integer  | number of samples to poll, defaults to 1 |
| -i | integer | interval in seconds between polls if sample more than 1, defaults to 1 |
| -t | string of [`f`, `l`] | type for data of word polls, double registers. `f` for float, `i` for integer.
                                        |||`Note`: If function is write, it is used to define type 	of the number to write |
| -e | string of [`b`, `l`] | endianess, defaults to big, can be set to `l` for little endian |
| -v | integer or float | values in decimal, applies only for write operations and need to come with the `-t` flag for type of the data |

### Examples

##### Example 1

 - slave bus address at `247`
 - serial port `/dev/ttyUSB0`
 - starting register address `1390`
 - holding registers
 - fetch two registers, so `1390` and `1391`
 - each register is UINT16 and big endian so leave the rest flags to default

 ```
 	python rtuMaster.py -p /dev/ttyUSB0 -b 9600 -a 247 -r 1390 -f 3 -c 2
 ```
 
##### Example 2

 - Write single holding register
 - Register address `1391`
 - value to write `250`
 - Register accepts integers
 ```
 python rtuMaster.py -p /dev/ttyUSB0 -b 9600 -a 247 -r 1391 -f 6 -v 250 -t i
 ```
 
##### Example 3

 - Write multiple holding registers
 - Register starting address `1390`
 - Write `2` registers
 - values to write [`1`, `250`]
 - Registers accept floats

 ```
python rtuMaster.py -p /dev/ttyUSB0 -b 9600 -a 247 -r 1391 -f 16 -v 1 250 -t f
 ```
 

