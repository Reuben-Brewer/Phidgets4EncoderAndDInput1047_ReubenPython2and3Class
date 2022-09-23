########################

Phidgets4EncoderAndDInput1047_ReubenPython2and3Class

Wrapper (including ability to hook to Tkinter GUI) to control Phidget Encoder HighSpeed 4-Input (4 quadrature encoders and 4 digital inputs) 1047_2B (non VINT).

From Phidgets' website:
"The PhidgetEncoder Highspeed 4-Input interfaces with any 5V quadrature encoder.
A quadrature encoder is the most commonly used feedback device for a DC or stepper motor.
With an encoder, you can keep track of how far your motor has turned, which then allows you to control the
position and velocity in your code. This Phidget connects to your computer via USB.
Features:
Four digital inputs for reading limit switches or buttons
Works with all 0-5V quadrature encoders - simultaneously read four incremental encoders with
line driver, open collector, or push-pull output circuits
Read at speeds of up to 250,000 quadrature cycles per second
Power Saving Options - You can turn it off via software when it's not turning.
While disabled, this board draws 30mA of current.
Reports a timestamp in milliseconds for each position change event, for easy velocity calculation."

Phidget Encoder HighSpeed 4-Input
ID: 1047_2B
https://phidgets.com/?tier=3&catid=4&pcid=2&prodid=1199

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision H, 09/21/2022

Verified working on: 
Python 2.7, 3.8.
Windows 8.1, 10 64-bit
Raspberry Pi Buster 
(no Mac testing yet)

*NOTE THAT YOU MUST INSTALL BOTH THE Phidget22 LIBRARY AS WELL AS THE PYTHON MODULE.*

########################  

########################### Python module installation instructions, all OS's

Phidgets4EncoderAndDInput1047_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'Phidget22']
Phidgets4EncoderAndDInput1047_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class']
Phidgets4EncoderAndDInput1047_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins', 'numpy']
Phidgets4EncoderAndDInput1047_ReubenPython2and3Class, ListOfModuleDependencies_All: ['future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'Phidget22']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:
pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -
sudo apt-get install -y libphidget22
 
###########################