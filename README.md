# MDL v0.1 - Mobile Diagnostic Lab 

**Android Monitoring platform**

*Beauttah K.*

MDL connects to Android devices through USB or Wireless Debugging, continuously collects telemetry, and presents it through a real-time desktop interface.

Built with **Rust**, **Tauri v2**, and a lightweight HTML/CSS/JavaScript frontend.

## Requirements

- Rust 1.77+
- Node.js 18+
- ADB (Android Debug Bridge)
- Android device with USB debugging enabled

On Linux, Tauri also requires the WebKitGTK and GTK development packages (for example `libwebkit2gtk-4.1-dev` and `libgtk-3-dev` on Debian-based distributions).

## Setup

```bash
# Install the Tauri CLI locally
npm install

# Verify ADB is working
adb devices

# Run the desktop app in development mode
npm run tauri dev
```

Build a release bundle:

```bash
npm run tauri build
```

The release binary can also be compiled directly:

```bash
cd src-tauri
cargo build --release
```

## Android setup

1. Connect your Android device via USB
2. Enable USB debugging
3. Click **Refresh** to detect devices
4. Select your device and click **Connect**
5. Dashboard shows live metrics

## Verify ADB

```bash
adb devices
```

A working connection looks like:

```text
List of devices attached
XXXXXXXXXX      device
```

## Interface

> List of devices detected

![List-of-devices](.img/interface1.png)

> Informative UI

![main-ui](.img/interface2.png)

## Architecture

The Tauri backend shells out to the `adb` binary and runs collectors on a background thread. Metrics are emitted to the frontend over Tauri events.

```text
ADB → Collectors → Metric events → Web UI
```

Rust sources live in `src-tauri/src/`, and the frontend lives in `web/`.

Collectors currently cover device information, battery, performance, network diagnostics, Wi-Fi, cellular, Bluetooth, and installed applications. Inspection tools add live logcat, notifications, foreground activity and task stack, power/doze and wake locks, per-app CPU and memory, thermal zones and sensor snapshots, plus recordable sessions that can be exported to CSV or JSON.

Saved sessions can be browsed, replayed, and exported from the connection screen without a device attached. Live device views require an authorized ADB connection.

## Contributing

Contributions are welcome! MDL v0.1 is the foundation with an extensible collector architecture. Feel free to:
- Add new collectors (Wi-Fi signal analysis, cellular metrics, etc.)
- Improve visualizations
- Enhance the UI
- Fix bugs
- Add documentation

Each collector follows the pattern: `Collector → Metric Bus → Analytics → UI`

_More features to be integrated later ..._

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

```text
Based on MDL (Mobile Diagnostic Lab) by Beauttah K.
Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
```
