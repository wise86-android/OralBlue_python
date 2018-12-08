# OralB Smart Toothbrush protocol

## Advertise
length must be >=16

byte 0 must be 0 and byte 3 must be 0xC (12) or 0xE(14)
byte 3 is the length of the vendor specific part + 1 -> 11 or 13 bytes
byte 5 and 6 must be 0xDC00

byte 7 is the protocol version (1,2,3)

byte 8 is the type( ?) and can be:

- 1 ->  ORAL-B SmartSeries (6 Modes) (1, 5, 2, 4, 3, 6)

- 2 -> ORAL-B SmartSeries (5 Modes) (1, 5, 2, 4, 3)

- 65 (0x41) -> ORAL-B SmartSeries (4 Modes) (1, 2, 4, 3)

- 66 (0x42) -> ORAL-B SmartSeries (3 Modes) (1, 2, 3)

- 67 (0x43) -> ORAL-B SmartSeries (2 Modes) (1, 2)

- 68 (0x44) -> ORAL-B SmartSeries (2 Modes) (1, 3)

- 69 (0x45) -> ORAL-B SmartSeries (3 Modes) (1, 2, 4)

- 70 (0x46) -> ORAL-B SmartSeries (1 Mode) (1)

- 33  -> ??

- 34  -> ??

byte 9 is the fwVersion

byte 10 brush state (see #State)

byte 11 high pressure flag 8bit is high pressure, 7bit unknown

byte 12 brusing time min 

byte 13 brusing time sec

byte 14 brush mode (see #Mode)

byte 15 (first 3 byte: mask 0x07) 

# Mode
|Id |Mode|
|---|---|
| 0x00 | OFF |
| 0x01 | DAILY_CLEAN |
| 0x02 | SENSITIVE |
| 0x03 | MASSAGE |
| 0x04 | WHITENING |
| 0x05 | DEEP_CLEAN |
| 0x06 | TONGUE_CLEANING |
| 0x07 | TURBO |
| 0xFF | UNKNOWN |

# States
|Id |State|
|---|---|
| 0x00 | UNKNOWN |
| 0x01 | INIT |
| 0x02 | IDLE |
| 0x03 | RUN |
| 0x04 | CHARGE |
| 0x05 | SETUP |
| 0x06 | FLIGHT_MENU |
| 0x71 | FINAL_TEST |
| 0x72 | PCB_TEST |
| 0x73 | SLEEP |
| 0x74 | TRANSPORT |
| 0xFF | UNKNOWN |

## Charateristics

### Status
UUID: A0F0FF04-5047-4D53-8208-4F72616C2D42

data: 2 bytes [state, unknown]

### Battery level:
uuid: A0F0FF05-5047-4D53-8208-4F72616C2D42
data: only the first byte it is used -> 0..100 ?

### Brusing mode
UUID: A0F0FF07-5047-4D53-8208-4F72616C2D42

data: 1 byte -> 0..6


### Brusing time:
UUID: A0F0FF08-5047-4D53-8208-4F72616C2D42

data: 2 bytes [min, sec]


###Sector
UUID: a0f0ff09-5047-4d53-8208-4f72616c2d42

data 1 byte -> 0..8

### button state ?
UUID A0F0FF06-5047-4D53-8208-4F72616C2D42

### smily ?
UUID A0F0FF0a-5047-4D53-8208-4F72616C2D42

when 2 minutes ends

data: 1 byte 0/1 



Used Bluetooth LE Scanner app


 A0F0FF04-5047-4D53-8208-4F72616C2D42: Device State
 States over time
 on: 0x200
 starting to brush: 0x800
 brushing: 0x300
 on: 0x200
 
 
 A0F0FF0B-5047-4D53-8208-4F72616C2D42: Pressure Sensor
 0x00 by default
 
 A0F0FF08-5047-4D53-8208-4F72616C2D42: Brushing Time
 Increases by 1 every second
 
 A0F0FF09-5047-4D53-8208-4F72616C2D42: Quadrant
 Increases every second, "jumps when quadrant is jumped"
 
 
 A0F0FF06-5047-4D53-8208-4F72616C2D42: Button State
 0x01000000 when power button pressed, 0x0 otherwise
 
 A0F0FF0a-5047-4D53-8208-4F72616C2D42: Smiley
 0x0 by default, turns to 0x1 when brushing time reached
 0x01000000 when power button pressed, 0x0 otherwise
 
 A0F0FF07-5047-4D53-8208-4F72616C2D42: Brushing mode
 0x1: daily
 0x3: +
 0x4: feather
 0x2: diamond
 0x7 "water"
 
 A0F0FF0d-5047-4D53-8208-4F72616C2D42: sensor data
 lots of hex values updating fast, partially repeated in the hex string
 
 
 gatttool:
 [A8:1B:6A:BD:03:8E][LE]> characteristics
 handle: 0x0002, char properties: 0x02, char value handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
 handle: 0x0004, char properties: 0x02, char value handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
 handle: 0x0006, char properties: 0x0a, char value handle: 0x0007, uuid: 00002a02-0000-1000-8000-00805f9b34fb
 handle: 0x0008, char properties: 0x0a, char value handle: 0x0009, uuid: 00002a03-0000-1000-8000-00805f9b34fb
 handle: 0x000a, char properties: 0x02, char value handle: 0x000b, uuid: 00002a04-0000-1000-8000-00805f9b34fb
 handle: 0x000d, char properties: 0x20, char value handle: 0x000e, uuid: 00002a05-0000-1000-8000-00805f9b34fb
 handle: 0x0011, char properties: 0x1a, char value handle: 0x0012, uuid: a0f0fff1-5047-4d53-8208-4f72616c2d42
 handle: 0x0015, char properties: 0x0a, char value handle: 0x0016, uuid: a0f0fff2-5047-4d53-8208-4f72616c2d42
 handle: 0x0018, char properties: 0x0a, char value handle: 0x0019, uuid: a0f0fff3-5047-4d53-8208-4f72616c2d42
 handle: 0x001b, char properties: 0x0a, char value handle: 0x001c, uuid: a0f0fff4-5047-4d53-8208-4f72616c2d42
 handle: 0x001f, char properties: 0x02, char value handle: 0x0020, uuid: a0f0ff01-5047-4d53-8208-4f72616c2d42
 handle: 0x0022, char properties: 0x02, char value handle: 0x0023, uuid: a0f0ff02-5047-4d53-8208-4f72616c2d42
 handle: 0x0025, char properties: 0x0a, char value handle: 0x0026, uuid: a0f0ff03-5047-4d53-8208-4f72616c2d42
 handle: 0x0028, char properties: 0x12, char value handle: 0x0029, uuid: a0f0ff04-5047-4d53-8208-4f72616c2d42
 handle: 0x002c, char properties: 0x12, char value handle: 0x002d, uuid: a0f0ff05-5047-4d53-8208-4f72616c2d42
 handle: 0x0030, char properties: 0x12, char value handle: 0x0031, uuid: a0f0ff06-5047-4d53-8208-4f72616c2d42
 handle: 0x0034, char properties: 0x12, char value handle: 0x0035, uuid: a0f0ff07-5047-4d53-8208-4f72616c2d42
 handle: 0x0038, char properties: 0x12, char value handle: 0x0039, uuid: a0f0ff08-5047-4d53-8208-4f72616c2d42
 handle: 0x003c, char properties: 0x12, char value handle: 0x003d, uuid: a0f0ff09-5047-4d53-8208-4f72616c2d42
 handle: 0x0040, char properties: 0x12, char value handle: 0x0041, uuid: a0f0ff0a-5047-4d53-8208-4f72616c2d42
 handle: 0x0044, char properties: 0x12, char value handle: 0x0045, uuid: a0f0ff0b-5047-4d53-8208-4f72616c2d42
 handle: 0x0048, char properties: 0x1a, char value handle: 0x0049, uuid: a0f0ff0c-5047-4d53-8208-4f72616c2d42
 handle: 0x004c, char properties: 0x12, char value handle: 0x004d, uuid: a0f0ff0d-5047-4d53-8208-4f72616c2d42
 handle: 0x0051, char properties: 0x1a, char value handle: 0x0052, uuid: a0f0ff21-5047-4d53-8208-4f72616c2d42
 handle: 0x0055, char properties: 0x0a, char value handle: 0x0056, uuid: a0f0ff22-5047-4d53-8208-4f72616c2d42
 handle: 0x0058, char properties: 0x0a, char value handle: 0x0059, uuid: a0f0ff23-5047-4d53-8208-4f72616c2d42
 handle: 0x005b, char properties: 0x0a, char value handle: 0x005c, uuid: a0f0ff24-5047-4d53-8208-4f72616c2d42
 handle: 0x005e, char properties: 0x0a, char value handle: 0x005f, uuid: a0f0ff25-5047-4d53-8208-4f72616c2d42
 handle: 0x0061, char properties: 0x0a, char value handle: 0x0062, uuid: a0f0ff26-5047-4d53-8208-4f72616c2d42
 handle: 0x0064, char properties: 0x0a, char value handle: 0x0065, uuid: a0f0ff27-5047-4d53-8208-4f72616c2d42
 handle: 0x0067, char properties: 0x0a, char value handle: 0x0068, uuid: a0f0ff28-5047-4d53-8208-4f72616c2d42
 handle: 0x006a, char properties: 0x02, char value handle: 0x006b, uuid: a0f0ff29-5047-4d53-8208-4f72616c2d42
 handle: 0x006d, char properties: 0x0a, char value handle: 0x006e, uuid: a0f0ff2a-5047-4d53-8208-4f72616c2d42
 handle: 0x0070, char properties: 0x0a, char value handle: 0x0071, uuid: a0f0ff2b-5047-4d53-8208-4f72616c2d42
 
 gatttool  --device=A8:1B:6A:BD:03:8E --char-write-req --handle=0x003a
 --value=0100 --listen
 Characteristic value was written successfully
 Notification handle = 0x0039 value: 00 02 
 Notification handle = 0x0039 value: 00 03 
 Notification handle = 0x0039 value: 00 04 
 Notification handle = 0x0039 value: 00 05 
 Notification handle = 0x0039 value: 00 06 
 Notification handle = 0x0039 value: 00 07 
 Notification handle = 0x0039 value: 00 00 