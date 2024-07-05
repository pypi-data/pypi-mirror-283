# Pythonion

## Description

`Pythonion` is a Python library used to interface to `TernionEAI` firmware running on `Ternion` microcontroller board.
It provides a high level interface to interact with the board and its peripherals.

*Note:* The project is still in development and tested on `Windows OS` only.


## Installation


### Step 1

Create a new environment with the required dependencies.

```
python -m venv .venv.ternion
```

### Step 2

Activate the environment.

```
.venv.ternion/Scripts/activate
```

### Step 3

Install the `pythonion` package.

```
python -m pip install pythonion
```

## Usage

Create a new script, import the `pythonion` package and use it as shown in the following examples.

### Example 1

```py
""" Get Firmware Info and Serial Number """

from pythonion import Ternion

ptn = Ternion()
print(f"Firmware Info: {ptn.get_firmware_info()}")
print(f"Serial Number: {ptn.get_serial_number()}")
ptn.start()

```

### Example 2
```python
"""
Testing:
    - Make an analog input change to see the event data
    - Press a switch to see the event data
"""

from pythonion import Ternion, TernionSwitchEventData, TernionAnalogEventData


def psw_event_callback(event: TernionSwitchEventData) -> None:
    print(f"{event.get_producer()} {event.get_state_name()} {event.get_press_count()}")


def adc_event_callback(event: TernionAnalogEventData) -> None:
    print(f"{event.get_producer()} {event.get_voltage():.3f}")


pyt = Ternion()
pyt.on_switch_event(psw_event_callback)
pyt.on_analog_event(adc_event_callback)
pyt.start()

```
