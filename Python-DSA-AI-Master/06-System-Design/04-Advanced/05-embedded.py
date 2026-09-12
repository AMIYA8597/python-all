"""
Embedded Systems in Python (MicroPython / CircuitPython Focus)

1. WHAT IS IT?
Embedded systems are specialized computing systems that perform dedicated functions within a larger mechanical or electrical system.
Python, specifically dialects like MicroPython and CircuitPython, is increasingly used in embedded systems (microcontrollers like ESP32, RP2040, STM32) due to its rapid development cycle and rich hardware abstraction layers.

2. INDUSTRY USE CASES
- IoT Devices: Smart home sensors, agricultural monitors, industrial telemetry (ESP32/ESP8266).
- Prototyping: Rapidly testing hardware logic before porting to C/C++.
- Edge AI: Running lightweight machine learning models on microcontrollers (TensorFlow Lite for Microcontrollers).
- Maker/Education: Raspberry Pi Pico, Adafruit boards.

3. BEGINNER EXPLANATION
An embedded system is like the "brain" inside your microwave or washing machine. It doesn't have a screen or a keyboard, and it just does one specific job. 
Because microcontrollers have tiny amounts of memory (RAM) and slow processors compared to your laptop, writing Python for them requires special tricks to avoid running out of memory.

4. TECHNICAL EXPLANATION
Programming embedded systems in Python differs significantly from desktop Python:
- No OS (Bare Metal): MicroPython runs directly on the hardware. There is no standard OS scheduler, filesystem (usually a minimal FAT/LittleFS is provided), or virtual memory.
- Memory Constraints: You might only have 128KB of RAM. Dynamic allocation (creating new objects) fragments memory quickly, leading to `MemoryError`.
- Hardware Interrupts: You must respond to hardware events (like a button press or sensor ready) immediately using Interrupt Service Routines (ISRs).
- Peripheral Buses: Direct interaction with I2C, SPI, UART, ADC, and PWM.

5. ADVANCED CONCEPTS: OPTIMIZATIONS
- Pre-allocation: Allocate buffers and objects at startup. Do NOT allocate inside loops or ISRs.
- ISR Constraints: ISRs must be extremely fast. No floating-point math, no memory allocation, no print statements. Use `micropython.schedule()` to defer processing.
- `const()`: MicroPython provides a `const()` macro to evaluate constants at compile time, saving RAM.
- `memoryview` / `bytearray`: Used for zero-copy buffer manipulation, critical for fast SPI/I2C transfers.

6. INTERVIEW QUESTIONS
- Q: What are the restrictions of an Interrupt Service Routine (ISR) in MicroPython?
  A: Cannot allocate memory (no creating lists/dicts/strings), cannot use floating point, must be as short/fast as possible. Use `micropython.schedule` for heavy lifting.
- Q: How do you prevent memory fragmentation in long-running embedded Python code?
  A: Pre-allocate all necessary buffers globally at startup. Use `gc.collect()` proactively at known safe points in the main loop. Use `memoryview` for slicing buffers without copying.

Below is a mock simulation demonstrating embedded Python design patterns.
"""

import time
import random
# In a real MicroPython environment, you would import machine and micropython
# import machine
# import micropython

# ==========================================
# Mocking MicroPython Hardware APIs
# ==========================================
class MockPin:
    IN = 0
    OUT = 1
    IRQ_FALLING = 2
    
    def __init__(self, id, mode):
        self.id = id
        self.mode = mode
        self.value_state = 0
        
    def value(self, val=None):
        if val is not None:
            self.value_state = val
        return self.value_state

    def irq(self, trigger, handler):
        self.irq_handler = handler
        # We will manually trigger this in the simulation

class MockI2C:
    def __init__(self, scl, sda, freq):
        pass
    def readfrom_mem_into(self, addr, memaddr, buf):
        # Simulate reading 2 bytes of sensor data into a pre-allocated buffer
        buf[0] = random.randint(0, 255)
        buf[1] = random.randint(0, 255)

# MicroPython mock schedule
scheduled_function = None
def mock_schedule(func, arg):
    global scheduled_function
    scheduled_function = (func, arg)

# ==========================================
# Optimized Embedded Code Pattern
# ==========================================

# 1. Use constants to save RAM
SENSOR_ADDR = 0x42
REG_TEMP = 0x01
THRESHOLD = 30000

# 2. Pre-allocate ALL buffers and state variables globally
# This prevents MemoryError and heap fragmentation during the main loop
sensor_buffer = bytearray(2)
i2c_bus = MockI2C(scl=MockPin(22, MockPin.OUT), sda=MockPin(21, MockPin.OUT), freq=400000)
led = MockPin(2, MockPin.OUT)
button = MockPin(0, MockPin.IN)

# Pre-allocated variables for ISR to avoid allocation
interrupt_count = 0
isr_flag = False

# 3. Hardware Interrupt Service Routine (ISR)
# Rule: Keep it short, no allocations, no floats, no prints.
def button_isr(pin):
    global interrupt_count, isr_flag
    # Bare minimum work in the interrupt context
    interrupt_count += 1
    isr_flag = True
    # In real MicroPython: micropython.schedule(handle_button_press, interrupt_count)
    mock_schedule(handle_button_press, interrupt_count)

# Register the ISR
button.irq(trigger=MockPin.IRQ_FALLING, handler=button_isr)


# 4. Deferred Interrupt Handler (Runs in main context)
# Safe to allocate, print, and do heavier processing here.
def handle_button_press(count):
    print(f"[EVENT] Button pressed! Total presses: {count}")
    # Toggle LED
    led.value(not led.value())


def read_sensor_fast(bus, addr, reg, buf):
    """
    Read sensor using pre-allocated buffer (zero allocation).
    """
    bus.readfrom_mem_into(addr, reg, buf)
    # Combine 2 bytes into a 16-bit integer
    return (buf[0] << 8) | buf[1]


def main_loop():
    print("Starting embedded main loop...")
    
    # Optional: trigger garbage collection immediately after initialization
    # import gc; gc.collect()
    
    global scheduled_function, isr_flag
    
    for _ in range(5): # Simulate 5 ticks of the main loop
        start_t = time.time()
        
        # 1. Handle scheduled tasks from ISRs
        if scheduled_function:
            func, arg = scheduled_function
            func(arg)
            scheduled_function = None
            isr_flag = False
            
        # 2. Read Sensors (Zero allocation)
        raw_val = read_sensor_fast(i2c_bus, SENSOR_ADDR, REG_TEMP, sensor_buffer)
        print(f"[TICK] Sensor reading: {raw_val} (LED state: {led.value()})")
        
        # 3. Actuate / Control Logic
        if raw_val > THRESHOLD:
            print("       -> Threshold exceeded! Triggering cooling pump.")
            
        # 4. Simulate a hardware interrupt occurring asynchronously
        if random.random() > 0.6:
            button_isr(button)
            
        # 5. Yield / Sleep (Watchdog feeding in real systems)
        time.sleep(0.5)

if __name__ == "__main__":
    main_loop()

"""
COMMON MISTAKES & SECURITY CONCERNS:
1. Memory Leaks: Creating lists `[]` or strings `""` inside the `while True` loop will eventually exhaust memory. Use `bytearray` and `memoryview`.
2. Blocking: Using `time.sleep()` for long periods prevents checking sensors or feeding the Hardware Watchdog Timer (WDT), causing system resets. Use non-blocking state machines.
3. String Formatting in ISR: `print("Val: {}".format(x))` inside an ISR causes memory allocation and will crash the microcontroller.
4. Security: Embedded devices often store WiFi credentials in plaintext in `boot.py` or `main.py`. Physical access means total compromise. Flash encryption and Secure Boot are required for production.
"""
