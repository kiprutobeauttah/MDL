# MDL v0.1 - Mobile Diagnostic Lab 

**Android Monitoring platform**

*Beauttah K.*

MDL connects to Android devices through USB or Wireless Debugging, continuously collects telemetry, and presents it through a  real-time desktop interface.




## Installation Guide

### Requirements

- Python 3.12+
- ADB (Android Debug Bridge)
- Android device with USB debugging enabled
### clone Repository
```bash

git clone https://github.com/kiprutobeauttah/MDL.git

```
### Setup 

```bash
# Install dependencies
pip install -r requirements.txt

# Or use pip with pyproject.toml
pip install -e .
```

### Verify ADB

```bash
# Check ADB is working
adb devices

# Should show your connected device
# --------------------------
# List of devices attached
# XXXXXXXXXX      device
# --------------------------

```

## Launch

```bash
# Launch MDL
python app.py
```
## Android setup
1. Connect your Android device via USB
2. Enable USB debugging
3. Click **Refresh** to detect devices
4. Select your device and click **Connect**
5. Dashboard shows live metrics

## Interface

> > List of devices detected

![List-of-devices](.img/interface1.png)


>> Informative ui

![main-ui](.img/interface2.png)

---




MDL - Mobile Diagnostic Lab -**Beauttah K.**

## License

This project is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit to Beauttah K., provide a link to the license, and indicate if changes were made.

See the [LICENSE](LICENSE) file for full details or visit [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)

### Attribution Example

When using or building upon MDL, please provide attribution:

```
Based on MDL (Mobile Diagnostic Lab) by Beauttah K.
Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
```

## Contributing

Contributions are welcome! MDL v0.1 is the foundation with an extensible collector architecture. Feel free to:
- Add new collectors (Wi-Fi signal analysis, cellular metrics, sensors, etc.)
- Improve visualizations
- Enhance the UI
- Fix bugs
- Add documentation

Each collector follows the pattern: `Collector → Metric Bus → Analytics → UI`


_More features to be intergrated later ..._