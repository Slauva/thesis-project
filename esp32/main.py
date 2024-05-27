from machine import ADC

sensor = ADC(36)
while True:
    print(sensor.read_u16())