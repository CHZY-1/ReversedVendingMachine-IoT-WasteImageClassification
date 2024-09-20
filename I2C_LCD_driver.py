# I2C_LCD_driver.py
# A library to control 16x2 LCD displays via I2C using the PCF8574 I2C expander

import smbus
import time

# LCD Address (adjust if needed)
ADDRESS = 0x27

# LCD commands
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # 1st line
LCD_LINE_2 = 0xC0  # 2nd line

LCD_BACKLIGHT = 0x08  # On
LCD_NOBACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

class I2C_LCD_driver:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.lcd_init()

    def lcd_init(self):
        self.lcd_write(0x33, LCD_CMD)  # Initialize
        self.lcd_write(0x32, LCD_CMD)  # Set to 4-bit mode
        self.lcd_write(0x06, LCD_CMD)  # Cursor move direction
        self.lcd_write(0x0C, LCD_CMD)  # Turn cursor off, blinking off
        self.lcd_write(0x28, LCD_CMD)  # 2 line display
        self.lcd_write(0x01, LCD_CMD)  # Clear display
        time.sleep(E_DELAY)

    def lcd_write(self, bits, mode):
        # Send byte to data pins
        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        self.bus.write_byte(ADDRESS, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.bus.write_byte(ADDRESS, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(E_DELAY)
        self.bus.write_byte(ADDRESS, (bits | ENABLE))
        time.sleep(E_PULSE)
        self.bus.write_byte(ADDRESS, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_display_string(self, message, line):
        message = message.ljust(16, " ")
        line_address = LCD_LINE_1 if line == 1 else LCD_LINE_2
        self.lcd_write(line_address, LCD_CMD)
        for i in range(16):
            self.lcd_write(ord(message[i]), LCD_CHR)

    def lcd_clear(self):
        self.lcd_write(0x01, LCD_CMD)
        self.lcd_write(0x02, LCD_CMD)
