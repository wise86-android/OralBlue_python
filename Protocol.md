# OralB Smart Toothbrush protocol

## Advertise
length must be >=16

byte 0 must be 0 and byte 3 must be 0xC (12) or 0xE(14)
byte 3 is the length of the vendor specific part + 1 -> 11 or 13 bytes
byte 5 and 6 must be 0xDC00

byte 7 is the protocol version (1,2,3,4)

byte 8 is device type and can be:

- 0 -> D36 (X Mode)
- 1 -> D36 (6 Mode)
- 2  -> D36 (5 Mode)
- 32  -> D701 (X Mode)
- 33  -> D701 (6 Mode)
- 34  -> D701 (5 Mode)
- 39  -> D700 (5 Mode)
- 40 -> D700 (4 Mode)
- 41  -> D700 (6 Mode)
- 63  -> D36 (Experimental)
- 64  -> D21 (X Mode)
- 65  -> D21 (4 Mode)
- 66  -> D21 (3a Mode)
- 67  -> D21 (2a Mode)
- 68  -> D21 (2b Mode)
- 69  -> D21 (3b Mode)
- 70 -> D21 (1 Mode)
- 80 -> D601 (X Mode)
- 81 -> D601 (5 Mode)
- 82 -> D601 (4 Mode)
- 83 -> D601 (3A Mode)
- 84 -> D601 (2A Mode)
- 85 -> D601 (2B Mode)
- 86 -> D601 (3B Mode)
- 87 -> D601 (1 Mode)

byte 9 is the fwVersion

byte 10 brush state (see #State)

byte 11

- bit 8: high pressure 0 = normal 1 = high
- bit 7: motor speed, 0 = normal 1 = reduced
- bit 3: mode button pressed
- bit 2: power button pressed
- bit 1: timer mode, 0 = profesional (each 30s) 1= only end

byte 12 brushing time min 

byte 13 brushing time sec

byte 14 brush mode (see #Mode)

byte 15:
bit 0,1,2: quadrant
bit 3,4,5: smiley 

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

### ToothbrushID
UUID: a0f0ff01-5047-4d53-8208-4f72616c2d42

data: uint32 little endian
an id different for each toothbrush??

### ModelId
UUID: a0f0ff02-5047-4d53-8208-4f72616c2d42

data: 3 bytes: [modeId, protocolVersion, fwVersion]

Node: protocol version and fwVersion are available only if protocolVersion >=3

### UserId
UUID: a0f0ff03-5047-4d53-8208-4f72616c2d42

data: 1 byte current user id, can be change with a simple write

### Status
UUID: A0F0FF04-5047-4D53-8208-4F72616C2D42

data: 2 bytes [state, unknown] as in the advertise

### Battery level:
UUID: A0F0FF05-5047-4D53-8208-4F72616C2D42

data: 4 bytes [ battery level (%), seconds left (2bytes le), unknown]

Node: seconds left available only with protocol version > 3 

### Button State:
UUID: a0f0ff06-5047-4d53-8208-4f72616c2d42

data: 2 bytes: [powerButtonState, modeButtonState] , 1 = pressed

### Brushing mode
UUID: A0F0FF07-5047-4D53-8208-4F72616C2D42

data: 1 byte -> 0..6 as in the advertise

### Brushing time:
UUID: A0F0FF08-5047-4D53-8208-4F72616C2D42

data: 2 bytes [min, sec]


### Sector
UUID: a0f0ff09-5047-4d53-8208-4f72616c2d42

data 1 byte -> 0..8 as in the advertise


### Control Char
UUID: a0f0ff21-5047-4d53-8208-4f72616c2d42

write here before change some configuration

### Current time
UUID: a0f0ff22-5047-4d53-8208-4f72616c2d42

Access: R/W

data: 4 bytes little endian seconds after 1/1/2000

Note: To change it you have to write [0x37,0x26] into the control characteristics before write the new value

### Signals
UUID: a0f0ff24-5047-4d53-8208-4f72616c2d42

Access: R/W
data: 1 byte: tell the status of the user notification:
- bit 1 = is vibrating (as a sector end)
- bit 2 = is vibrating (as a session end)
- bit 3 = light on (as high pressure)
- bit 4 = light on (as session end)

note: before write it, write [0x37,0x28] in the control characteristics

node: writing is not working :(

### Available modes
UUID: a0f0ff25-5047-4d53-8208-4f72616c2d42
Access: R/W

Data: 8 byte, each byte is a possible motor mode, it can be used to reordered the available modes

Note: To change it you have to write [0x37,0x29] into the control characteristics before write the new value

### Sector timer
UUID: a0f0ff26-5047-4d53-8208-4f72616c2d42
Access: R/W

Data: 8 uint16 le, timeout for each sector, to update it all the 8 value must be present

Node: write [0x37,0x2A] into the control characteristics before change the values  
 

### Session Info
UUID: a0f0ff29-5047-4d53-8208-4f72616c2d42
Access:R

from this value the session data can be read.

To select the session, write [0x02, index] into the control characteristics.

The number of stored session are:
- 20 for protocol version 1
- 30 for protocol version 2,3,4 

#### Session Format
- Start time: 4 bytes le, seconds after 1/1/2000
- duration : 2 bytes le, duration in seconds
- event count: 1 byte ??
- mode: 1 byte, as in the advertise, mode used for the majority of time during the session
- time under pressure: 2 byte le seconds with the hight pressure warning on
- pressure warnings: 1 byte, # pressure warnings
- final battery state: 1 byte % of battery when the session ends

the last 4 byte has a different meaning with different protocol versions:
if protocol version == 1 
- last full charge: 4 bytes seconds after 1/1/2000

if protocol version == 2,3,4
- 2 byte: as uint16 le, 3 bit = # sector, 13 bit total target time
- 2 byte: as uint16 le, 3 bit = # user id, 13 bit session id

if protocol version ==4
time under pressure is in 1/10 seconds 
 