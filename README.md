## Simple Auto Clicker

### Main Features
- Simple and easy to understand console interface
- Lightweight and fast
- Customisable click speed and controls
- Supports multiple click locations

### Installation
1. Download the latest build from the [Releases](https://github.com/Caramajau/simple-auto-clicker/releases) page.
2. Extract the downloaded ZIP file to a folder of your choice.
3. Run the `SimpleAutoClicker.exe` file to start the application. See [Instructions](#instructions) for usage details.

### Instructions
Choose a location with your mouse and press ```g``` (or multiple times for multiple locations), then ```j``` and it will start clicking there. To stop the clicking, press ```k```. If you want new positions clear it with ```c``` and record new ones with ```g``` again. Finally, exit the program using ```ESC```.

For more advanced usages there is the ability to stop recording positions by toggling the recording mode on or off using ```r```. It is also possible to customise the controls and click speed by changing the values in the ```options.json``` file. Lastly, don't worry about breaking the contents in the JSON file, the program will either ignore it or reset the file to default if anything happens.

#### Example Usage
Pressing g g j k ESC would yield:
```
...
Added position: (x, y)
All recorded positions are now: [(x, y)]
Added position: (x2, y2)
All recorded positions are now: [(x, y), (x2, y2)]
Started clicking recorded positions:
(x, y)
(x2, y2)
Stopped clicking recorded positions, press j to start the clicking again.
```
Where:
- ... represents previous outputs. (Assumes recording mode has not been toggled off)
- x, y, x2, y2 represented mouse position coordinates.

### Additional Notes
- The auto clicker is designed for personal use and should not be used for any malicious activities.
- Always ensure that you are in compliance with the terms of service of the applications you are using the auto clicker with.
- If you have any suggestions or feature requests, feel free to open an issue on the [Issues](https://github.com/Caramajau/simple-auto-clicker/issues) page.
