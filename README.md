Python dependencies to run this program are:
- openCv
- mediapipe
- numpy
- tensorflow
- keras
- speech_recognition
- matplotlib
- tensorflow_datasets

In order to run the program as is (the main file is called HandGuidance.ipynb), make sure that you have a folder called “donkeyweights” containing the tensor flow model files of the model you want to use (in this case the donkey model) at the same folder level as the “src” folder. Alternatively, you can set the “weights_dir” attribute to the path to that folder.  
You will also need a folder called “tensorflow_datasets” in C:\\Users\\{your session} containing the “donkeyset” folder which can be found at the following link: https://github.com/kevswingler/DonkeyData

If you’re using the glove with this program, make sure to set the COM port properly in the “Glove Control” section of the program, for the method “open_glove()”. If your computer is connected to the glove, you can find which COM port is being used to communicate with the glove (on windows) by going to Bluetooth settings, “More Bluetooth options”, “COM Ports” tab and there will be the name of the board on the glove (“ESP32Buzz ‘ESP32SPP’”). Set whatever is in the “Port” column as the argument of “serial.Serial(‘COMX’)”. 
If you remove the glove from this list and reconnect it, the COM port may change. 
The “gloveControlExample” file also reference the COM port, so if you want to run these programs you will need to change the COM port there as well (they each contain the COM port twice). This file was provided by Dr Kevin Swingler with the glove as an example of how to use it.

Donkey_ObJ_Det_Predict is based on https://keras.io/examples/vision/retinanet/ and was adapted to work with the donkey dataset by Dr Kevin Swingler. It can run detection on donkey images. The path to the image to detect can be set in the last cell.