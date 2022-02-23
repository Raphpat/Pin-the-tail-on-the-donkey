import serial
import keyboard

ser = serial.Serial("COM5")
print(ser.name)
ser.write(b"0001buzz500.")
ser.close()

def open_glove():
    return serial.Serial('COM5')

def close_glove(ser):
    ser.close()


def buzz(loc, lenms=500):
    '''Buzz given location for given duration in ms
    location codes:
    t, b, l, r, a'''
    loc_ar = {'t':'1000', 'r':'0100', 'b':'0010', 'l':'0001', 'a':'1111'}
    loc_code = loc_ar[loc]
    com = loc_code+'buzz'+str(lenms)+'.'
    ser.write(str.encode(com))

def spin(times):
    for i in range(times):
        buzz('t',50)
        buzz('r',50)
        buzz('b',50)
        buzz('l',50)
        

#ser.close()
ser=open_glove()
print("Go")
while True:
    if keyboard.is_pressed("z"):
        buzz("t")
    if keyboard.is_pressed("s"):
        buzz("b")
    if keyboard.is_pressed("d"):
        buzz("l")
    if keyboard.is_pressed("q"):
        buzz("r")
    if keyboard.is_pressed("space"):
        buzz("a")
    if keyboard.read_key() == 'u':
        break
        
close_glove(ser)