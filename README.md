# Karasu: A 3DOF Planar Robotic Arm with Wireless Control Using MQTT

# 3DOF Planar Robotic Arm Controller

This project is comprised of two software components that together control a 3-degree of freedom (3DOF) planar robotic arm. The project allows the user to input a desired (x, y) coordinate and the type of trajectory (angular or linear) that the robotic arm should take to reach this position. The software then calculates the necessary servo motor angles to achieve this movement.

## Software Components

1. `main.py`: This Python program allows the user to input a coordinate and trajectory type for the robotic arm. The software will then calculate the necessary servo motor angles by solving the forward and inverse kinematic equations. The calculated angles are published to an MQTT network for further processing.

2. `karasu_control.ino`: This Arduino program is meant to run on an ESP8266 board and controls the servomotors of the robot. The program subscribes to the MQTT topic containing the servo motor angles. It then processes these values from the published JSON file and sets the corresponding servomotor angles.

## Getting Started

1. Make sure you have Python and Arduino IDE installed on your system.
2. Clone the repository using `git clone`.
3. Open the Python file `main.py` and Arduino file `karasu_control.ino` in their respective IDEs.

## Usage

1. Run `main.py` in a Python environment. Enter the desired (x, y) coordinate and trajectory type when prompted.
2. Make sure your ESP8266 board is connected and run `karasu_control.ino` from the Arduino IDE.
3. The calculated servo angles will be published to the MQTT network, and the ESP8266 board will subscribe to this data, moving the robotic arm as directed.

## Dependencies

- Python 3.7 or later
- Arduino IDE
- paho-mqtt Python package
- ESP8266 board

## Authors

Juan Antono Robledo Lara

## License

This project is licensed under the [insert license here] - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Acknowledgement 1
- Acknowledgement 2

## Contributing

If you want to contribute to this project and make it better, your help is very welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

