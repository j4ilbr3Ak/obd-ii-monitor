# obd-ii-monitor
A basic concept of vehicle monitoring software to show vehicle data like fuel level, speed, rpm etc..
This entire concept is made using Python, the GUI is made using PySide2 to show the gauges and have some sort of user interface.
to use this software to read data from the vehicle OBD-ii port you must use an ELM327 adapter(Bluetooth, or USB)
you also need to be an admin of some sorts or be able to read and write to the Bluetooth or USB ports 

Note: if you want to add any commands feel free to look at the documents for all the other commands found here https://python-obd.readthedocs.io/en/latest/

commands to get everything installed for you system:        ~$ pip install obd,      ~$ pip install PySide2
This is a very basic version meant just for reading data and outputting it in an easy-to-understand user interface.
With the Python obd library you can also read DTC (also known as diagnostic trouble codes) as well as clear them and much more! which you implement those features into this software for full customizability 
