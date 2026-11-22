const ICONS = {
  home: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>`,
  activity: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>`,
  wifi: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"></path><path d="M1.42 9a16 16 0 0 1 21.16 0"></path><path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path><line x1="12" y1="20" x2="12.01" y2="20"></line></svg>`,
  smartphone: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>`,
  bluetooth: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"></polyline></svg>`,
  package: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>`,
  compass: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>`,
  battery: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="6" width="18" height="12" rx="2" ry="2"></rect><line x1="23" y1="13" x2="23" y2="11"></line></svg>`,
  cpu: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>`,
  "hard-drive": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="12" x2="2" y2="12"></line><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path><line x1="6" y1="16" x2="6.01" y2="16"></line><line x1="10" y1="16" x2="10.01" y2="16"></line></svg>`,
  settings: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>`,
  "bar-chart-2": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>`,
  "file-text": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
  "alert-triangle": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
  bell: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>`,
  layers: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>`,
  zap: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`,
  terminal: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>`,
  folder: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>`,
  file: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>`,
  image: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>`,
};

const IMAGE_EXTENSIONS = new Set(["png", "jpg", "jpeg", "jfif", "gif", "webp", "bmp", "svg", "avif"]);
const OFFLINE_VIEWS = new Set(["sessions", "events", "usb-storage", "usb-status"]);

const SHELL_COMMANDS = [
  {
    category: "Device & system",
    command: "getprop ro.product.model",
    description: "Show the device model name.",
  },
  {
    category: "Device & system",
    command: "getprop ro.build.version.release",
    description: "Show the Android OS version.",
  },
  {
    category: "Device & system",
    command: "getprop ro.build.version.sdk",
    description: "Show the Android API level (SDK number).",
  },
  {
    category: "Device & system",
    command: "uname -a",
    description: "Show kernel and system architecture details.",
  },
  {
    category: "Device & system",
    command: "uptime",
    description: "Show how long the device has been running and its load averages.",
  },
  {
    category: "Device & system",
    command: "wm size",
    description: "Show the physical and override display resolution.",
  },
  {
    category: "Battery & power",
    command: "dumpsys battery",
    description: "Show battery level, temperature, voltage, charging status, and health.",
  },
  {
    category: "Battery & power",
    command: "settings get system screen_brightness",
    description: "Read the current screen brightness setting.",
  },
  {
    category: "Performance",
    command: "dumpsys meminfo",
    description: "Show detailed memory usage for the system and running apps.",
  },
  {
    category: "Performance",
    command: "dumpsys cpuinfo",
    description: "Show CPU usage by process.",
  },
  {
    category: "Performance",
    command: "top -n 1 -b | head -n 20",
    description: "Take a single snapshot of the busiest processes.",
  },
  {
    category: "Performance",
    command: "df -h",
    description: "Show storage usage for mounted filesystems in human-readable units.",
  },
  {
    category: "Network",
    command: "ip addr show wlan0",
    description: "Show the Wi-Fi interface IP address and network details.",
  },
  {
    category: "Network",
    command: "dumpsys wifi",
    description: "Show Wi-Fi connection state, signal strength, and link speed.",
  },
  {
    category: "Network",
    command: "dumpsys telephony.registry",
    description: "Show cellular network type, signal strength, and operator details.",
  },
  {
    category: "Network",
    command: "ping -c 4 8.8.8.8",
    description: "Test internet connectivity and measure round-trip latency.",
  },
  {
    category: "Network",
    command: "dumpsys bluetooth_manager",
    description: "Show Bluetooth adapter state and bonded devices.",
  },
  {
    category: "Applications",
    command: "pm list packages",
    description: "List all installed package names.",
  },
  {
    category: "Applications",
    command: "pm list packages -3",
    description: "List only third-party (user-installed) packages.",
  },
  {
    category: "Applications",
    command: "pm path <package>",
    description: "Show the APK path for a package. Replace <package> with a package name.",
  },
  {
    category: "Files",
    command: "ls -la /sdcard",
    description: "List files in the shared internal storage.",
  },
  {
    category: "Files",
    command: "ls -la /data/local/tmp",
    description: "List files in the temporary shell workspace.",
  },
  {
    category: "Files",
    command: "du -sh /sdcard/DCIM",
    description: "Show the total size of the camera folder.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -d -t 200",
    description: "Print the 200 most recent system log lines and exit.",
  },
  {
    category: "Logs & debugging",
    command: "dumpsys activity activities | head -n 40",
    description: "Show the current activity stack summary.",
  },
  {
    category: "Device & system",
    command: "getprop ro.product.manufacturer",
    description: "Show the device manufacturer.",
  },
  {
    category: "Device & system",
    command: "getprop ro.product.brand",
    description: "Show the device brand name.",
  },
  {
    category: "Device & system",
    command: "getprop ro.product.device",
    description: "Show the device codename.",
  },
  {
    category: "Device & system",
    command: "getprop ro.build.version.security_patch",
    description: "Show the Android security patch level.",
  },
  {
    category: "Device & system",
    command: "getprop ro.build.fingerprint",
    description: "Show the full build fingerprint.",
  },
  {
    category: "Device & system",
    command: "getprop ro.boot.hardware",
    description: "Show the hardware platform name.",
  },
  {
    category: "Device & system",
    command: "getprop ro.product.cpu.abi",
    description: "Show the primary CPU ABI.",
  },
  {
    category: "Device & system",
    command: "getprop ro.serialno",
    description: "Show the device serial number.",
  },
  {
    category: "Device & system",
    command: "getprop | grep -i build",
    description: "Show all build-related properties.",
  },
  {
    category: "Device & system",
    command: "getprop | grep -i dalvik",
    description: "Show Dalvik and runtime properties.",
  },
  {
    category: "Device & system",
    command: "getprop | grep -i density",
    description: "Show display density properties.",
  },
  {
    category: "Device & system",
    command: "date",
    description: "Show the device date, time, and timezone.",
  },
  {
    category: "Device & system",
    command: "id",
    description: "Show the current shell user and group IDs.",
  },
  {
    category: "Device & system",
    command: "ps -A",
    description: "List all running processes.",
  },
  {
    category: "Device & system",
    command: "cat /proc/version",
    description: "Show the kernel version and build details.",
  },
  {
    category: "Device & system",
    command: "cat /proc/cpuinfo",
    description: "Show CPU model, cores, and feature flags.",
  },
  {
    category: "Device & system",
    command: "cat /proc/meminfo",
    description: "Show detailed kernel memory statistics.",
  },
  {
    category: "Device & system",
    command: "free -h",
    description: "Show used and available memory in human-readable units.",
  },
  {
    category: "Device & system",
    command: "vmstat 1 3",
    description: "Sample virtual memory and CPU activity three times.",
  },
  {
    category: "Device & system",
    command: "getenforce",
    description: "Show the SELinux enforcement mode.",
  },
  {
    category: "Device & system",
    command: "settings list system",
    description: "List all system settings.",
  },
  {
    category: "Device & system",
    command: "settings list secure",
    description: "List all secure settings.",
  },
  {
    category: "Device & system",
    command: "settings list global",
    description: "List all global settings.",
  },
  {
    category: "Device & system",
    command: "wm density",
    description: "Show the physical and override display density.",
  },
  {
    category: "Device & system",
    command: "dumpsys SurfaceFlinger --list",
    description: "List layers known to SurfaceFlinger.",
  },
  {
    category: "Device & system",
    command: "service list",
    description: "List registered Android system services.",
  },
  {
    category: "Device & system",
    command: "dumpsys usb",
    description: "Show USB device and port state.",
  },
  {
    category: "Device & system",
    command: "dumpsys input",
    description: "Show input devices, keyboards, and touch state.",
  },
  {
    category: "Device & system",
    command: "dumpsys display",
    description: "Show display and brightness state.",
  },
  {
    category: "Device & system",
    command: "dumpsys window displays",
    description: "Show window manager display information.",
  },
  {
    category: "Battery & power",
    command: "dumpsys batterystats --charged",
    description: "Show battery statistics since the last full charge.",
  },
  {
    category: "Battery & power",
    command: "dumpsys batterystats --unplugged",
    description: "Show battery statistics since the device was unplugged.",
  },
  {
    category: "Battery & power",
    command: "dumpsys power",
    description: "Show wakefulness, wake locks, and power state.",
  },
  {
    category: "Battery & power",
    command: "dumpsys deviceidle",
    description: "Show doze and device-idle state.",
  },
  {
    category: "Battery & power",
    command: "dumpsys thermalservice",
    description: "Show thermal status and temperature zones.",
  },
  {
    category: "Battery & power",
    command: "dumpsys alarm",
    description: "Show scheduled alarms and their owners.",
  },
  {
    category: "Battery & power",
    command: "dumpsys jobscheduler",
    description: "Show scheduled jobs and their constraints.",
  },
  {
    category: "Battery & power",
    command: "settings get global low_power",
    description: "Show whether battery saver is enabled.",
  },
  {
    category: "Battery & power",
    command: "settings get global stay_on_while_plugged_in",
    description: "Show the stay-awake charging setting.",
  },
  {
    category: "Performance",
    command: "dumpsys meminfo <package>",
    description: "Show memory usage for a specific package.",
  },
  {
    category: "Performance",
    command: "top -H -n 1 -b",
    description: "Show a one-shot snapshot with per-thread CPU usage.",
  },
  {
    category: "Performance",
    command: "dumpsys gfxinfo <package>",
    description: "Show graphics frame timing for a package.",
  },
  {
    category: "Performance",
    command: "dumpsys gfxinfo <package> framestats",
    description: "Show detailed frame statistics for a package.",
  },
  {
    category: "Performance",
    command: "dumpsys procstats",
    description: "Show process runtime and memory statistics.",
  },
  {
    category: "Performance",
    command: "dumpsys diskstats",
    description: "Show disk I/O and storage statistics.",
  },
  {
    category: "Performance",
    command: "dumpsys SurfaceFlinger",
    description: "Show SurfaceFlinger composition and frame data.",
  },
  {
    category: "Performance",
    command: "dumpsys media.player",
    description: "Show active media players and playback state.",
  },
  {
    category: "Performance",
    command: "dumpsys media.audio_flinger",
    description: "Show audio mixer and track information.",
  },
  {
    category: "Network",
    command: "ip addr",
    description: "Show all network interfaces and addresses.",
  },
  {
    category: "Network",
    command: "ip route",
    description: "Show the device routing table.",
  },
  {
    category: "Network",
    command: "dumpsys connectivity",
    description: "Show connectivity networks and their state.",
  },
  {
    category: "Network",
    command: "cmd wifi status",
    description: "Show current Wi-Fi status using the wifi command.",
  },
  {
    category: "Network",
    command: "cmd wifi list-networks",
    description: "List saved Wi-Fi networks.",
  },
  {
    category: "Network",
    command: "dumpsys netstats",
    description: "Show network traffic statistics.",
  },
  {
    category: "Network",
    command: "dumpsys netpolicy",
    description: "Show network policy and restriction state.",
  },
  {
    category: "Network",
    command: "dumpsys nfc",
    description: "Show NFC adapter and tag state.",
  },
  {
    category: "Network",
    command: "dumpsys location",
    description: "Show location providers and recent fixes.",
  },
  {
    category: "Network",
    command: "settings get global airplane_mode_on",
    description: "Show whether airplane mode is enabled.",
  },
  {
    category: "Network",
    command: "settings get global wifi_on",
    description: "Show whether Wi-Fi is enabled.",
  },
  {
    category: "Network",
    command: "settings get global mobile_data",
    description: "Show whether mobile data is enabled.",
  },
  {
    category: "Network",
    command: "ping -c 4 google.com",
    description: "Test DNS resolution and internet latency.",
  },
  {
    category: "Network",
    command: "getprop | grep -i dns",
    description: "Show configured DNS properties.",
  },
  {
    category: "Applications",
    command: "pm list packages -s",
    description: "List system packages.",
  },
  {
    category: "Applications",
    command: "pm list packages -d",
    description: "List disabled packages.",
  },
  {
    category: "Applications",
    command: "pm list packages -f",
    description: "List packages with their APK paths.",
  },
  {
    category: "Applications",
    command: "dumpsys package <package>",
    description: "Show full package manager details.",
  },
  {
    category: "Applications",
    command: "dumpsys package <package> | grep -A 40 \"runtime permissions\"",
    description: "Show runtime permission grants for a package.",
  },
  {
    category: "Applications",
    command: "dumpsys package <package> | grep -A 20 \"requested permissions\"",
    description: "Show requested permissions for a package.",
  },
  {
    category: "Applications",
    command: "cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package>",
    description: "Resolve the launcher activity for a package.",
  },
  {
    category: "Applications",
    command: "am start -W -n <package>/<activity>",
    description: "Launch a specific activity and wait for the result.",
  },
  {
    category: "Applications",
    command: "am force-stop <package>",
    description: "Force stop a package and all of its processes.",
  },
  {
    category: "Applications",
    command: "dumpsys notification --noredact",
    description: "Show active notifications without redaction.",
  },
  {
    category: "Applications",
    command: "dumpsys activity processes",
    description: "Show process records managed by the activity manager.",
  },
  {
    category: "Applications",
    command: "dumpsys activity services",
    description: "Show running and bound services.",
  },
  {
    category: "Applications",
    command: "dumpsys activity providers",
    description: "Show content providers and their clients.",
  },
  {
    category: "Applications",
    command: "dumpsys activity broadcasts",
    description: "Show registered broadcast receivers.",
  },
  {
    category: "Applications",
    command: "dumpsys activity recents",
    description: "Show recent tasks and activities.",
  },
  {
    category: "Applications",
    command: "dumpsys activity top",
    description: "Show the top activity and its state.",
  },
  {
    category: "Applications",
    command: "dumpsys window",
    description: "Show window manager state and focus.",
  },
  {
    category: "Applications",
    command: "dumpsys window windows",
    description: "Show details for every window.",
  },
  {
    category: "Sensors & thermal",
    command: "dumpsys sensorservice",
    description: "Show the sensor list and recent sensor events.",
  },
  {
    category: "Sensors & thermal",
    command: "dumpsys sensorservice | head -n 80",
    description: "Show the first part of the sensor service dump.",
  },
  {
    category: "Sensors & thermal",
    command: "dumpsys sensorservice | grep -i \"active\"",
    description: "Show active sensor connections.",
  },
  {
    category: "Sensors & thermal",
    command: "dumpsys thermalservice",
    description: "Show thermal status, zones, and cooling devices.",
  },
  {
    category: "Files",
    command: "ls -la /sdcard/Download",
    description: "List files in the shared Downloads folder.",
  },
  {
    category: "Files",
    command: "ls -la /sdcard/DCIM",
    description: "List files in the camera folder.",
  },
  {
    category: "Files",
    command: "du -sh /sdcard/*",
    description: "Show the size of each item in shared storage.",
  },
  {
    category: "Files",
    command: "cat /proc/mounts",
    description: "Show mounted filesystems and mount options.",
  },
  {
    category: "Files",
    command: "find /sdcard -maxdepth 2 -type d | head -n 40",
    description: "List shared-storage directories two levels deep.",
  },
  {
    category: "Files",
    command: "stat /sdcard",
    description: "Show metadata for the shared storage path.",
  },
  {
    category: "Files",
    command: "ls -la /system/app | head -n 40",
    description: "List system applications.",
  },
  {
    category: "Files",
    command: "ls -la /data/app",
    description: "List installed application directories.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -d -b crash",
    description: "Print the crash log buffer and exit.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -d -b system -t 200",
    description: "Print the last 200 system buffer lines.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -d -s AndroidRuntime:E",
    description: "Show Android runtime errors and crashes.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -d -s ActivityManager:I",
    description: "Show activity manager info-level logs.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -d -s PackageManager:I",
    description: "Show package manager info-level logs.",
  },
  {
    category: "Logs & debugging",
    command: "logcat -c",
    description: "Clear all log buffers.",
  },
  {
    category: "Logs & debugging",
    command: "dumpsys dropbox --print",
    description: "Print recent DropBox crash and error entries.",
  },
  {
    category: "Logs & debugging",
    command: "dumpsys dropbox --print system_app_crash",
    description: "Print recent app crash entries from DropBox.",
  },
  {
    category: "Logs & debugging",
    command: "dumpsys dropbox --print system_server_crash",
    description: "Print recent system server crash entries.",
  },
  {
    category: "Logs & debugging",
    command: "dumpsys activity exit-info <package>",
    description: "Show recent exit reasons for a package.",
  },
  {
    category: "Logs & debugging",
    command: "dumpsys activity lastanr",
    description: "Show the last application-not-responding record.",
  },
  {
    category: "Media & display",
    command: "settings get system screen_off_timeout",
    description: "Show the screen timeout in milliseconds.",
  },
  {
    category: "Media & display",
    command: "settings get system accelerometer_rotation",
    description: "Show whether auto-rotate is enabled.",
  },
  {
    category: "Media & display",
    command: "settings get system user_rotation",
    description: "Show the current user rotation setting.",
  },
  {
    category: "Media & display",
    command: "dumpsys media.camera",
    description: "Show camera service and device state.",
  },
  {
    category: "Media & display",
    command: "dumpsys media.codec",
    description: "Show media codec and codec-list state.",
  },
  {
    category: "Media & display",
    command: "dumpsys audio",
    description: "Show audio focus, streams, and volume state.",
  },
  {
    category: "Security & permissions",
    command: "dumpsys device_policy",
    description: "Show device administrator policies.",
  },
  {
    category: "Security & permissions",
    command: "dumpsys trust",
    description: "Show trust agents and trust state.",
  },
  {
    category: "Security & permissions",
    command: "settings get global adb_enabled",
    description: "Show whether ADB is enabled.",
  },
  {
    category: "Security & permissions",
    command: "settings get secure install_non_market_apps",
    description: "Show the unknown-sources install setting.",
  },
  {
    category: "Security & permissions",
    command: "dumpsys lock_settings",
    description: "Show lock screen and credential settings.",
  },
  {
    category: "Storage",
    command: "dumpsys storaged",
    description: "Show storage I/O and usage statistics.",
  },
  {
    category: "Storage",
    command: "sm list-volumes",
    description: "List mounted storage volumes.",
  },
  {
    category: "Storage",
    command: "ls -la /storage/emulated/0",
    description: "List the primary emulated storage root.",
  },
];

const CHARTS = [];

const state = {
  devices: [],
  selectedSerial: null,
  device: {},
  apps: [],
  appsLoaded: false,
  appsLoading: false,
  events: [],
  maxEvents: 100,
  ramUsed: 0,
  ramTotal: 0,
  storageUsed: 0,
  storageTotal: 0,
  batteryLevel: null,
  shellHistory: [],
  shellHistoryIndex: 0,
  shellBusy: false,
  shellMode: "terminal",
  fsPath: "/",
  fsEntries: [],
  fsLoaded: false,
  fsBusy: false,
  charts: {},
  appDetail: {
    package: null,
    label: null,
    details: null,
    loading: false,
    loadToken: 0,
    logSession: null,
    logActive: false,
  },
  notifications: [],
  notificationsLoading: false,
  activity: null,
  activityLoading: false,
  usage: [],
  usageLoading: false,
  power: null,
  powerLoading: false,
  sensorSnapshot: null,
  sensorsLoading: false,
  deviceLogs: {
    session: null,
    active: false,
  },
  sessions: [],
  sessionsLoading: false,
  sessionStatus: null,
  offline: false,
  usbStatus: null,
  usbLoading: false,
  usbStoragePath: null,
  usbStorageBusy: false,
  viewTimers: {},
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function invoke(command, args) {
  if (window.__TAURI__ && window.__TAURI__.core) {
    return window.__TAURI__.core.invoke(command, args);
  }
  return Promise.reject(new Error("Tauri backend is not available"));
}

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entities[character];
  });
}

function formatValue(value) {
  if (value === null || value === undefined) {
    return "--";
  }
  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

function formatNumber(value, digits = 1) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return "--";
  }
  return value.toFixed(digits);
}

function setStatus(kind, text) {
  const dot = $("#status-dot");
  dot.className = `status-dot ${kind || ""}`.trim();
  dot.textContent = "●";
  $("#status-text").textContent = text;
}

function setConnectionMessage(text) {
  $("#connection-message").textContent = text || "";
}

function setDetail(root, key, value) {
  const element = $(`[data-detail="${key}"]`, root);
  if (element) {
    element.textContent = value === undefined || value === null || value === "" ? "--" : String(value);
  }
}

class Chart {
  constructor(canvas, series, options = {}) {
    this.canvas = canvas;
    this.series = series.map((item) => ({ ...item, data: [] }));
    this.maxPoints = options.maxPoints || 60;
    this.renderQueued = false;
    CHARTS.push(this);
  }

  push(name, value) {
    const series = this.series.find((item) => item.name === name);
    if (!series) {
      return;
    }
    const number = Number(value);
    series.data.push(Number.isFinite(number) ? number : 0);
    if (series.data.length > this.maxPoints) {
      series.data.shift();
    }
    this.render();
  }

  render() {
    const canvas = this.canvas;
    if (!canvas) {
      return;
    }

    const rect = canvas.getBoundingClientRect();
    if (rect.width < 4 || rect.height < 4) {
      return;
    }

    const dpr = window.devicePixelRatio || 1;
    const width = Math.floor(rect.width);
    const height = Math.floor(rect.height);

    if (canvas.width !== Math.floor(width * dpr) || canvas.height !== Math.floor(height * dpr)) {
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
    }

    const context = canvas.getContext("2d");
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    context.clearRect(0, 0, width, height);

    const padding = { left: 42, right: 10, top: 10, bottom: 18 };
    const plotWidth = width - padding.left - padding.right;
    const plotHeight = height - padding.top - padding.bottom;

    context.font = '10px "Segoe UI", system-ui, sans-serif';
    context.fillStyle = cssVar("--text-secondary");
    context.strokeStyle = cssVar("--border");
    context.lineWidth = 1;

    const values = this.series.flatMap((item) => item.data);
    const hasData = values.length > 0;

    let min = hasData ? Math.min(...values) : 0;
    let max = hasData ? Math.max(...values) : 1;

    if (min === max) {
      min -= 1;
      max += 1;
    }

    const spread = max - min;
    min -= spread * 0.1;
    max += spread * 0.1;

    const rows = 4;
    for (let row = 0; row <= rows; row += 1) {
      const y = padding.top + (plotHeight / rows) * row;
      context.beginPath();
      context.moveTo(padding.left, y);
      context.lineTo(padding.left + plotWidth, y);
      context.stroke();

      const value = max - ((max - min) / rows) * row;
      context.textAlign = "right";
      context.textBaseline = "middle";
      context.fillText(value.toFixed(Math.abs(value) >= 10 ? 0 : 1), padding.left - 6, y);
    }

    if (!hasData) {
      context.textAlign = "center";
      context.textBaseline = "middle";
      context.fillStyle = cssVar("--text-secondary");
      context.fillText("Waiting for data", padding.left + plotWidth / 2, padding.top + plotHeight / 2);
      return;
    }

    const toPoint = (value, index, length) => {
      const x = padding.left + (plotWidth * index) / Math.max(1, length - 1);
      const y = padding.top + plotHeight - ((value - min) / (max - min)) * plotHeight;
      return [x, y];
    };

    for (const series of this.series) {
      if (series.data.length === 0) {
        continue;
      }

      if (this.series.length === 1 && series.data.length > 1) {
        const gradient = context.createLinearGradient(0, padding.top, 0, padding.top + plotHeight);
        gradient.addColorStop(0, series.color);
        gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
        context.save();
        context.globalAlpha = 0.12;
        context.beginPath();
        series.data.forEach((value, index) => {
          const [x, y] = toPoint(value, index, series.data.length);
          if (index === 0) {
            context.moveTo(x, y);
          } else {
            context.lineTo(x, y);
          }
        });
        context.lineTo(padding.left + plotWidth, padding.top + plotHeight);
        context.lineTo(padding.left, padding.top + plotHeight);
        context.closePath();
        context.fillStyle = gradient;
        context.fill();
        context.restore();
      }

      context.beginPath();
      context.lineWidth = 2;
      context.strokeStyle = series.color;
      context.lineJoin = "round";
      context.lineCap = "round";

      series.data.forEach((value, index) => {
        const [x, y] = toPoint(value, index, series.data.length);
        if (index === 0) {
          context.moveTo(x, y);
        } else {
          context.lineTo(x, y);
        }
      });
      context.stroke();

      if (series.data.length === 1) {
        const [x, y] = toPoint(series.data[0], 0, 1);
        context.beginPath();
        context.arc(x, y, 3, 0, Math.PI * 2);
        context.fillStyle = series.color;
        context.fill();
      }
    }
  }
}

function setupCharts() {
  const accent = cssVar("--accent");
  const green = cssVar("--green");

  state.charts.cpu = new Chart($("#chart-cpu"), [{ name: "cpu", color: accent }]);
  state.charts.ram = new Chart($("#chart-ram"), [{ name: "ram", color: green }]);
  state.charts.latency = new Chart($("#chart-latency"), [{ name: "latency", color: accent }]);
  state.charts.throughput = new Chart($("#chart-throughput"), [
    { name: "rx", color: green },
    { name: "tx", color: accent },
  ]);
  state.charts.wifiSignal = new Chart($("#chart-wifi-signal"), [{ name: "rssi", color: green }]);
  state.charts.wifiSpeed = new Chart($("#chart-wifi-speed"), [{ name: "speed", color: accent }]);
  state.charts.cellular = new Chart($("#chart-cellular"), [
    { name: "rsrp", color: green },
    { name: "rsrq", color: accent },
  ]);
}

function renderAllCharts() {
  CHARTS.forEach((chart) => chart.render());
}

function injectIcons() {
  $$("[data-icon]").forEach((element) => {
    const text = element.textContent.trim();
    element.innerHTML = `<span class="icon">${ICONS[element.dataset.icon] || ""}</span><span>${escapeHtml(text)}</span>`;
  });
}

function setupNavigation() {
  $("#nav").addEventListener("click", (event) => {
    const button = event.target.closest(".nav-btn");
    if (!button) {
      return;
    }
    setView(button.dataset.view);
  });
}

function clearViewTimers() {
  Object.values(state.viewTimers).forEach((timer) => clearInterval(timer));
  state.viewTimers = {};
}

function setView(view) {
  if (state.offline && !OFFLINE_VIEWS.has(view)) {
    view = "sessions";
  }
  $$(".nav-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  $$(".view").forEach((section) => {
    section.classList.toggle("active", section.id === `view-${view}`);
  });
  $("#content").scrollTop = 0;
  clearViewTimers();

  if (view === "apps") {
    loadApps();
  } else if (view === "notifications") {
    loadNotifications();
    state.viewTimers.notifications = setInterval(loadNotifications, 5000);
  } else if (view === "activity") {
    loadActivity();
    state.viewTimers.activity = setInterval(loadActivity, 3000);
  } else if (view === "usage") {
    loadUsage();
    state.viewTimers.usage = setInterval(loadUsage, 3000);
  } else if (view === "power") {
    loadPower();
    state.viewTimers.power = setInterval(loadPower, 5000);
  } else if (view === "sensors") {
    loadSensors();
    state.viewTimers.sensors = setInterval(loadSensors, 3000);
  } else if (view === "sessions") {
    refreshSessionStatus();
    loadSessions();
  } else if (view === "usb-status") {
    loadUsbStatus();
  } else if (view === "usb-storage") {
    loadUsbStorage();
  } else if (view === "shell") {
    focusShellInput();
  } else if (view === "filesystem" && !state.fsLoaded) {
    loadDirectory(state.fsPath);
  }
  requestAnimationFrame(renderAllCharts);
}

function setupConnection() {
  $("#refresh-btn").addEventListener("click", refreshDevices);
  $("#connect-btn").addEventListener("click", connectDevice);
  $("#offline-sessions-btn").addEventListener("click", () => enterOfflineMode());
  $("#offline-usb-storage-btn").addEventListener("click", () => enterOfflineMode("usb-storage"));
  $("#offline-usb-status-btn").addEventListener("click", () => enterOfflineMode("usb-status"));
  $("#offline-connect-btn").addEventListener("click", exitOfflineMode);
}

async function refreshOfflineUsbStatus() {
  const label = $("#offline-usb-count");
  if (!label) {
    return;
  }
  try {
    const status = await invoke("get_usb_status");
    label.textContent = status.mtp_roots.length
      ? `${status.mtp_roots.length} MTP storage location${status.mtp_roots.length === 1 ? "" : "s"} detected`
      : "No MTP storage detected";
  } catch (error) {
    label.textContent = "USB status unavailable";
  }
}

async function refreshOfflineSessions() {
  const label = $("#offline-session-count");
  if (!label) {
    return;
  }
  try {
    const sessions = await invoke("list_sessions");
    label.textContent = sessions.length
      ? `${sessions.length} saved session${sessions.length === 1 ? "" : "s"} available`
      : "No saved sessions yet";
  } catch (error) {
    label.textContent = "Saved sessions unavailable";
  }
}

function setOfflineMode(offline) {
  state.offline = offline;
  $$(".nav-btn").forEach((button) => {
    const blocked = offline && !OFFLINE_VIEWS.has(button.dataset.view);
    button.disabled = blocked;
    if (blocked) {
      button.title = "Connect a device to use this view";
    } else {
      button.removeAttribute("title");
    }
  });

  $("#offline-connect-btn").classList.toggle("hidden", !offline);

  const nameInput = $("#session-name");
  const toggle = $("#session-toggle");
  if (nameInput && toggle) {
    nameInput.disabled = offline;
    toggle.disabled = offline;
    if (offline) {
      nameInput.title = "Connect a device to record a session";
      toggle.title = "Connect a device to record a session";
    } else {
      nameInput.removeAttribute("title");
      toggle.removeAttribute("title");
    }
  }
}

function enterOfflineMode(view = "sessions") {
  setOfflineMode(true);
  $("#connection-screen").classList.add("hidden");
  $("#app-screen").classList.remove("hidden");
  setStatus("offline", "Offline - no device");
  setView(view);
}

function exitOfflineMode() {
  setOfflineMode(false);
  $("#app-screen").classList.add("hidden");
  $("#connection-screen").classList.remove("hidden");
  setStatus("", "No device");
  refreshOfflineSessions();
  refreshOfflineUsbStatus();
  refreshDevices();
}

async function refreshDevices() {
  setConnectionMessage("Scanning for devices...");
  try {
    state.devices = await invoke("list_devices");
    if (state.selectedSerial && !state.devices.some((device) => device.serial === state.selectedSerial)) {
      state.selectedSerial = null;
    }
    renderDevices();
    setConnectionMessage(state.devices.length === 0 ? "No devices found" : "");
  } catch (error) {
    state.devices = [];
    renderDevices();
    setConnectionMessage(String(error));
  }
}

function renderDevices() {
  const list = $("#device-list");
  const empty = $("#device-empty");
  list.innerHTML = "";

  if (state.devices.length === 0) {
    list.classList.add("hidden");
    empty.classList.remove("hidden");
    $("#connect-btn").disabled = true;
    return;
  }

  list.classList.remove("hidden");
  empty.classList.add("hidden");

  for (const device of state.devices) {
    const online = device.state === "device";
    const row = document.createElement("div");
    row.className = "device-row";
    row.dataset.serial = device.serial;
    row.innerHTML = `
      <span class="dot ${online ? "online" : ""}">${online ? "●" : "○"}</span>
      <div>
        <div class="device-serial">${escapeHtml(device.serial)}</div>
        <div class="device-meta">${escapeHtml(device.connection_type)} • ${escapeHtml(device.state)}</div>
      </div>
    `;
    row.addEventListener("click", () => selectDevice(device.serial));
    list.append(row);
  }

  applySelection();
}

function selectDevice(serial) {
  state.selectedSerial = serial;
  applySelection();
}

function applySelection() {
  $$(".device-row", $("#device-list")).forEach((row) => {
    row.classList.toggle("selected", row.dataset.serial === state.selectedSerial);
  });
  $("#connect-btn").disabled = !state.selectedSerial;
}

async function connectDevice() {
  if (!state.selectedSerial) {
    return;
  }

  const serial = state.selectedSerial;
  $("#connect-btn").disabled = true;
  setConnectionMessage(`Connecting to ${serial}...`);
  setStatus("connecting", "Connecting...");

  try {
    const info = await invoke("connect_device", { serial });
    state.device = { ...info };
    renderDeviceInfo();
    await invoke("start_monitoring");
    setOfflineMode(false);
    refreshSessionStatus();
    refreshOfflineSessions();
    refreshOfflineUsbStatus();
    $("#connection-screen").classList.add("hidden");
    $("#app-screen").classList.remove("hidden");
    setView("overview");
    setStatus("connected", `${deviceName()} - Connected`);
    setConnectionMessage("");
  } catch (error) {
    $("#connect-btn").disabled = false;
    setConnectionMessage(String(error));
    setStatus("error", "Connection error");
  }
}

function deviceName() {
  const parts = [state.device.manufacturer, state.device.model].filter(
    (value) => value && value !== "Unknown"
  );
  return parts.length > 0 ? parts.join(" ") : "Unknown device";
}

function renderDeviceInfo() {
  $("#ov-device-name").textContent = deviceName();

  const android = state.device.android_version;
  const sdk = state.device.sdk_level;
  if (android || sdk) {
    $("#ov-android").textContent = `Android ${android || "--"} (SDK ${sdk || "--"})`;
  } else {
    $("#ov-android").textContent = "";
  }

  const details = {
    serial: state.device.serial,
    build: state.device.build_number,
    security_patch: state.device.security_patch,
    cpu_arch: state.device.cpu_arch,
    uptime: state.device.uptime,
  };

  for (const [key, value] of Object.entries(details)) {
    setDetail($("#ov-details"), key, value);
  }
}

function setupSearch() {
  $("#apps-search").addEventListener("input", renderApps);
  $("#apps-refresh").addEventListener("click", () => loadApps(true));
  $("#events-search").addEventListener("input", scheduleEventsRender);
  $("#events-category").addEventListener("change", scheduleEventsRender);
}

function setupShell() {
  $("#shell-form").addEventListener("submit", (event) => {
    event.preventDefault();
    runShellCommand("terminal");
  });

  $("#shell-gui-form").addEventListener("submit", (event) => {
    event.preventDefault();
    runShellCommand("gui");
  });

  $("#shell-clear").addEventListener("click", clearShellTerminal);
  $("#shell-gui-clear").addEventListener("click", clearShellGui);

  $("#shell-input").addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp") {
      if (state.shellHistory.length === 0) {
        return;
      }
      event.preventDefault();
      state.shellHistoryIndex = Math.max(0, state.shellHistoryIndex - 1);
      $("#shell-input").value = state.shellHistory[state.shellHistoryIndex] || "";
    } else if (event.key === "ArrowDown") {
      if (state.shellHistory.length === 0) {
        return;
      }
      event.preventDefault();
      state.shellHistoryIndex = Math.min(
        state.shellHistory.length,
        state.shellHistoryIndex + 1
      );
      $("#shell-input").value = state.shellHistory[state.shellHistoryIndex] || "";
    }
  });

  $$(".segment[data-shell-mode]").forEach((button) => {
    button.addEventListener("click", () => setShellMode(button.dataset.shellMode));
  });

  $("#shell-help-btn").addEventListener("click", openShellHelp);
  $("#shell-help-close").addEventListener("click", closeShellHelp);
  $("#shell-help").addEventListener("click", (event) => {
    if (event.target === $("#shell-help")) {
      closeShellHelp();
    }
  });
  $("#shell-help-search").addEventListener("input", renderShellHelp);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeShellHelp();
      hideContextMenu();
    }
  });

  renderShellHistory();
}

function setShellMode(mode) {
  state.shellMode = mode === "gui" ? "gui" : "terminal";
  $$(".segment[data-shell-mode]").forEach((button) => {
    button.classList.toggle("active", button.dataset.shellMode === state.shellMode);
  });
  $("#shell-terminal-panel").classList.toggle("hidden", state.shellMode !== "terminal");
  $("#shell-gui-panel").classList.toggle("hidden", state.shellMode !== "gui");
  if (state.shellMode === "gui") {
    renderShellHistory();
  }
  focusShellInput();
}

function focusShellInput() {
  const input = state.shellMode === "gui" ? $("#shell-gui-input") : $("#shell-input");
  input.focus();
}

function setShellStatus(text, kind) {
  const status = $("#shell-status");
  status.textContent = text;
  status.className = `status-text ${kind || ""}`.trim();
}

function appendShellLine(text, className = "") {
  const output = $("#shell-output");
  const line = document.createElement("div");
  line.className = `terminal-line ${className}`.trim();
  line.textContent = text;
  output.append(line);
  output.scrollTop = output.scrollHeight;
}

function appendShellOutput(text, className) {
  const limit = 50000;
  if (text.length <= limit) {
    appendShellLine(text, className);
    return;
  }
  appendShellLine(text.slice(0, limit), className);
  appendShellLine(`... output truncated (${text.length} characters)`, "terminal-muted");
}

function clearShellTerminal() {
  const output = $("#shell-output");
  output.innerHTML = "";
  appendShellLine("Type a command and press Enter.", "terminal-muted");
  setShellStatus("● Ready", "success");
  $("#shell-input").focus();
}

function clearShellGui() {
  $("#shell-gui-command").textContent = "";
  $("#shell-gui-state").textContent = "No command run yet";
  $("#shell-gui-stdout").textContent = "";
  $("#shell-gui-stderr").textContent = "";
  $("#shell-gui-stderr").classList.add("hidden");
  $("#shell-gui-exit").classList.add("hidden");
  $("#shell-gui-input").focus();
}

function pushShellHistory(command) {
  if (state.shellHistory[state.shellHistory.length - 1] !== command) {
    state.shellHistory.push(command);
    if (state.shellHistory.length > 50) {
      state.shellHistory.shift();
    }
  }
  state.shellHistoryIndex = state.shellHistory.length;
  renderShellHistory();
}

function renderShellHistory() {
  const container = $("#shell-history");
  const count = state.shellHistory.length;
  $("#shell-history-count").textContent = `${count} command${count === 1 ? "" : "s"}`;
  container.innerHTML = "";

  if (count === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-list";
    empty.textContent = "Commands you run will appear here.";
    container.append(empty);
    return;
  }

  for (const command of state.shellHistory.slice().reverse()) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "shell-history-item";
    item.textContent = command;
    item.title = "Insert this command";
    item.addEventListener("click", () => insertShellCommand(command));
    container.append(item);
  }
}

function insertShellCommand(command) {
  const input = state.shellMode === "gui" ? $("#shell-gui-input") : $("#shell-input");
  input.value = command;
  closeShellHelp();
  input.focus();
}

async function runShellCommand(source) {
  const mode = source === "gui" ? "gui" : "terminal";
  if (state.shellBusy || state.shellMode !== mode) {
    return;
  }

  const input = mode === "gui" ? $("#shell-gui-input") : $("#shell-input");
  const command = input.value.trim();
  if (!command) {
    return;
  }

  pushShellHistory(command);
  input.value = "";
  state.shellBusy = true;
  $("#shell-run").disabled = true;
  $("#shell-gui-run").disabled = true;
  $("#shell-clear").disabled = true;
  $("#shell-gui-clear").disabled = true;
  setShellStatus("● Running...", "");

  if (mode === "terminal") {
    appendShellLine(`$ ${command}`, "terminal-command");
  } else {
    $("#shell-gui-command").textContent = `$ ${command}`;
    $("#shell-gui-state").textContent = "Running...";
    $("#shell-gui-stdout").textContent = "";
    $("#shell-gui-stdout").classList.remove("hidden");
    $("#shell-gui-stderr").textContent = "";
    $("#shell-gui-stderr").classList.add("hidden");
    $("#shell-gui-exit").classList.add("hidden");
  }

  try {
    const result = await invoke("run_shell_command", { command });
    if (mode === "terminal") {
      const stdout = String(result.stdout || "").replace(/\n$/, "");
      const stderr = String(result.stderr || "").replace(/\n$/, "");
      if (stdout) {
        appendShellOutput(stdout, "terminal-stdout");
      }
      if (stderr) {
        appendShellOutput(stderr, "terminal-stderr");
      }
      if (!stdout && !stderr) {
        appendShellLine("(no output)", "terminal-muted");
      }
      if (result.exit_code !== 0) {
        appendShellLine(`Exit code: ${result.exit_code}`, "terminal-exit");
      }
    } else {
      renderGuiShellResult(result);
    }
    setShellStatus("● Ready", "success");
  } catch (error) {
    if (mode === "terminal") {
      appendShellLine(String(error), "terminal-stderr");
    } else {
      renderGuiShellError(String(error));
    }
    setShellStatus("● Error", "error");
  } finally {
    state.shellBusy = false;
    $("#shell-run").disabled = false;
    $("#shell-gui-run").disabled = false;
    $("#shell-clear").disabled = false;
    $("#shell-gui-clear").disabled = false;
    focusShellInput();
  }
}

function renderGuiShellResult(result) {
  const stdout = String(result.stdout || "").replace(/\n$/, "");
  const stderr = String(result.stderr || "").replace(/\n$/, "");
  const stdoutElement = $("#shell-gui-stdout");
  const stderrElement = $("#shell-gui-stderr");
  const exitElement = $("#shell-gui-exit");

  stdoutElement.textContent = stdout || "(no output)";
  stdoutElement.classList.remove("hidden");
  stderrElement.textContent = stderr;
  stderrElement.classList.toggle("hidden", !stderr);
  exitElement.textContent = `Exit code: ${result.exit_code}`;
  exitElement.classList.toggle("hidden", result.exit_code === 0);
  $("#shell-gui-state").textContent =
    result.exit_code === 0 ? "Completed" : `Completed with exit code ${result.exit_code}`;
}

function renderGuiShellError(message) {
  $("#shell-gui-stdout").textContent = "";
  $("#shell-gui-stdout").classList.add("hidden");
  $("#shell-gui-stderr").textContent = message;
  $("#shell-gui-stderr").classList.remove("hidden");
  $("#shell-gui-exit").classList.add("hidden");
  $("#shell-gui-state").textContent = "Failed";
}

function openShellHelp() {
  $("#shell-help").classList.remove("hidden");
  $("#shell-help").setAttribute("aria-hidden", "false");
  $("#shell-help-search").value = "";
  renderShellHelp();
  $("#shell-help-search").focus();
}

function closeShellHelp() {
  const help = $("#shell-help");
  if (!help) {
    return;
  }
  help.classList.add("hidden");
  help.setAttribute("aria-hidden", "true");
}

function renderShellHelp() {
  const list = $("#shell-help-list");
  const query = $("#shell-help-search").value.trim().toLowerCase();
  list.innerHTML = "";

  const filtered = SHELL_COMMANDS.filter((item) => {
    const haystack = `${item.category} ${item.command} ${item.description}`.toLowerCase();
    return haystack.includes(query);
  });

  if (filtered.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-list";
    empty.textContent = "No matching commands";
    list.append(empty);
    return;
  }

  const groups = new Map();
  for (const item of filtered) {
    if (!groups.has(item.category)) {
      groups.set(item.category, []);
    }
    groups.get(item.category).push(item);
  }

  for (const [category, items] of groups) {
    const heading = document.createElement("div");
    heading.className = "help-category";
    heading.textContent = category;
    list.append(heading);

    for (const item of items) {
      const row = document.createElement("div");
      row.className = "help-item";

      const info = document.createElement("div");
      info.className = "help-info";
      const command = document.createElement("code");
      command.className = "help-command";
      command.textContent = item.command;
      const description = document.createElement("p");
      description.className = "help-description";
      description.textContent = item.description;
      info.append(command, description);

      const insert = document.createElement("button");
      insert.type = "button";
      insert.className = "btn secondary help-insert";
      insert.textContent = "Insert";
      insert.addEventListener("click", () => insertShellCommand(item.command));

      row.append(info, insert);
      list.append(row);
    }
  }
}

function setupFilesystem() {
  $("#fs-refresh").addEventListener("click", () => loadDirectory(state.fsPath));
  $("#fs-up").addEventListener("click", () => {
    if (state.fsPath !== "/") {
      loadDirectory(parentPath(state.fsPath));
    }
  });
  $("#fs-go").addEventListener("click", () => loadDirectory($("#fs-path").value));
  $("#fs-path").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      loadDirectory(event.currentTarget.value);
    }
  });
  $$(".chip[data-fs-path]").forEach((button) => {
    button.addEventListener("click", () => loadDirectory(button.dataset.fsPath));
  });

  $("#fs-list").addEventListener("contextmenu", (event) => {
    const row = event.target.closest(".fs-row");
    event.preventDefault();

    if (!row) {
      showFilesystemContextMenu(event.clientX, event.clientY, null);
      return;
    }

    const entry = state.fsEntries.find((item) => item.path === row.dataset.path);
    if (!entry) {
      return;
    }

    $$(".fs-row", $("#fs-list")).forEach((item) => item.classList.remove("selected"));
    row.classList.add("selected");
    showFilesystemContextMenu(event.clientX, event.clientY, entry);
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest("#context-menu")) {
      hideContextMenu();
    }
  });
  window.addEventListener("blur", hideContextMenu);
  window.addEventListener("resize", hideContextMenu);
}

async function loadDirectory(path) {
  if (state.fsBusy) {
    return;
  }

  const target = String(path || "").trim() || "/";
  state.fsBusy = true;
  $("#fs-status").textContent = "Loading...";
  $("#fs-error").textContent = "";
  $("#fs-refresh").disabled = true;
  $("#fs-go").disabled = true;

  try {
    const listing = await invoke("list_directory", { path: target });
    state.fsPath = listing.path;
    state.fsEntries = Array.isArray(listing.entries) ? listing.entries : [];
    state.fsLoaded = true;
    $("#fs-path").value = listing.path;
    $("#fs-list").innerHTML = "";
    renderBreadcrumb(listing.path);
    renderFilesystem();
    const count = state.fsEntries.length;
    $("#fs-status").textContent = `${count} item${count === 1 ? "" : "s"}`;
    $("#fs-count").textContent = `${count} item${count === 1 ? "" : "s"}`;
    $("#fs-error").textContent = "";
  } catch (error) {
    state.fsEntries = [];
    state.fsPath = target;
    $("#fs-path").value = target;
    renderBreadcrumb(target);
    $("#fs-list").innerHTML = "";
    $("#fs-count").textContent = "0 items";
    $("#fs-status").textContent = "Error";
    $("#fs-error").textContent = String(error);
  } finally {
    state.fsBusy = false;
    $("#fs-refresh").disabled = false;
    $("#fs-go").disabled = false;
    $("#fs-up").disabled = state.fsPath === "/";
  }
}

function renderBreadcrumb(path) {
  const container = $("#fs-breadcrumb");
  container.innerHTML = "";

  const root = document.createElement("button");
  root.type = "button";
  root.className = `fs-crumb${path === "/" ? " active" : ""}`;
  root.textContent = "Root";
  root.addEventListener("click", () => {
    if (path !== "/") {
      loadDirectory("/");
    }
  });
  container.append(root);

  let current = "";
  for (const segment of path.split("/").filter(Boolean)) {
    current += `/${segment}`;
    const separator = document.createElement("span");
    separator.className = "fs-sep";
    separator.textContent = "/";
    container.append(separator);

    const button = document.createElement("button");
    button.type = "button";
    button.className = `fs-crumb${current === path ? " active" : ""}`;
    button.textContent = segment;
    button.addEventListener("click", () => {
      if (current !== path) {
        loadDirectory(current);
      }
    });
    container.append(button);
  }
}

function renderFilesystem() {
  const list = $("#fs-list");
  list.innerHTML = "";

  if (state.fsEntries.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-list";
    empty.textContent = "This folder is empty";
    list.append(empty);
    return;
  }

  for (const entry of state.fsEntries) {
    const row = document.createElement("button");
    row.type = "button";
    row.className = `fs-row${entry.is_dir ? " is-dir" : ""}`;
    row.title = entry.path;
    row.dataset.path = entry.path;

    const isImage = isImageEntry(entry);
    const nameCell = document.createElement("span");
    nameCell.className = "fs-name";
    const icon = document.createElement("span");
    icon.className = "fs-icon";
    icon.innerHTML = entry.is_dir ? ICONS.folder : isImage ? ICONS.image : ICONS.file;
    const name = document.createElement("span");
    name.className = "fs-name-text";
    name.textContent = entry.name;
    nameCell.append(icon, name);

    if (entry.is_link && entry.link_target) {
      const target = document.createElement("span");
      target.className = "fs-link-target";
      target.textContent = `→ ${entry.link_target}`;
      nameCell.append(target);
    }

    const size = document.createElement("span");
    size.className = "fs-size";
    size.textContent = entry.is_dir ? "—" : formatFileSize(entry.size);

    const modified = document.createElement("span");
    modified.className = "fs-modified";
    modified.textContent = entry.modified || "--";

    const permissions = document.createElement("span");
    permissions.className = "fs-perms";
    permissions.textContent = entry.permissions || "--";

    row.append(nameCell, size, modified, permissions);
    row.addEventListener("click", () => {
      $$(".fs-row", list).forEach((item) => item.classList.remove("selected"));
      row.classList.add("selected");
      if (entry.is_dir) {
        loadDirectory(entry.path);
      }
    });
    if (isImage) {
      row.title = `${entry.path} — double-click to preview`;
      row.addEventListener("dblclick", (event) => {
        event.preventDefault();
        openImagePreview(entry);
      });
    }
    list.append(row);
  }
}

function parentPath(path) {
  const trimmed = String(path || "").replace(/\/+$/, "");
  if (!trimmed || trimmed === "/") {
    return "/";
  }
  const index = trimmed.lastIndexOf("/");
  return index <= 0 ? "/" : trimmed.slice(0, index);
}

function formatFileSize(bytes) {
  if (typeof bytes !== "number" || !Number.isFinite(bytes) || bytes < 0) {
    return "--";
  }
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  const units = ["KB", "MB", "GB", "TB"];
  let value = bytes / 1024;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(value >= 10 ? 1 : 2)} ${units[unit]}`;
}

function isImageEntry(entry) {
  if (!entry || entry.is_dir) {
    return false;
  }
  const match = /\.([^./]+)$/.exec(entry.name);
  return Boolean(match && IMAGE_EXTENSIONS.has(match[1].toLowerCase()));
}

let imagePreviewToken = 0;

function setupImagePreview() {
  $("#image-preview-close").addEventListener("click", closeImagePreview);
  $("#image-preview").addEventListener("click", (event) => {
    if (event.target === $("#image-preview")) {
      closeImagePreview();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !$("#image-preview").classList.contains("hidden")) {
      closeImagePreview();
    }
  });
}

function openImagePreview(entry) {
  if (!isImageEntry(entry)) {
    return;
  }

  const token = ++imagePreviewToken;
  const image = $("#image-preview-image");
  const loading = $("#image-preview-loading");
  const error = $("#image-preview-error");

  hideContextMenu();
  $("#image-preview-title").textContent = entry.name;
  $("#image-preview-path").textContent = entry.path;
  image.classList.add("hidden");
  image.removeAttribute("src");
  image.alt = entry.name;
  error.textContent = "";
  error.classList.add("hidden");
  loading.textContent = "Loading image...";
  loading.classList.remove("hidden");
  $("#image-preview").classList.remove("hidden");
  $("#image-preview").setAttribute("aria-hidden", "false");
  $("#image-preview-close").focus();

  invoke("read_image_preview", { path: entry.path })
    .then((preview) => {
      if (token !== imagePreviewToken) {
        return;
      }
      image.onload = () => {
        if (token !== imagePreviewToken) {
          return;
        }
        loading.classList.add("hidden");
        image.classList.remove("hidden");
      };
      image.onerror = () => {
        if (token !== imagePreviewToken) {
          return;
        }
        image.classList.add("hidden");
        loading.classList.add("hidden");
        error.textContent = "Unable to decode this image.";
        error.classList.remove("hidden");
      };
      image.src = `data:${preview.mime};base64,${preview.data}`;
    })
    .catch((previewError) => {
      if (token !== imagePreviewToken) {
        return;
      }
      loading.classList.add("hidden");
      error.textContent = String(previewError);
      error.classList.remove("hidden");
    });
}

function closeImagePreview() {
  imagePreviewToken += 1;
  const overlay = $("#image-preview");
  if (!overlay || overlay.classList.contains("hidden")) {
    return;
  }

  overlay.classList.add("hidden");
  overlay.setAttribute("aria-hidden", "true");
  const image = $("#image-preview-image");
  image.onload = null;
  image.onerror = null;
  image.removeAttribute("src");
  image.classList.add("hidden");
  $("#image-preview-loading").classList.add("hidden");
  $("#image-preview-error").classList.add("hidden");
}

let fsMessageTimer = null;

function showFilesystemContextMenu(x, y, entry) {
  const menu = $("#context-menu");
  menu.innerHTML = "";

  const header = document.createElement("div");
  header.className = "context-header";
  const title = document.createElement("div");
  title.className = "context-title";
  title.textContent = entry ? entry.name : state.fsPath;
  const meta = document.createElement("div");
  meta.className = "context-meta";
  if (entry) {
    const type = entry.is_dir ? "Folder" : entry.is_link ? "Link" : "File";
    const size = entry.is_dir ? "" : ` · ${formatFileSize(entry.size)}`;
    meta.textContent = `${type}${size} · ${entry.modified || "Unknown modified time"}`;
  } else {
    const count = state.fsEntries.length;
    meta.textContent = `${count} item${count === 1 ? "" : "s"}`;
  }
  header.append(title, meta);
  menu.append(header);

  if (entry && entry.is_dir) {
    addContextMenuItem(menu, "Open folder", () => loadDirectory(entry.path));
  }
  addContextMenuItem(menu, entry ? "Copy path" : "Copy current path", () =>
    copyToClipboard(entry ? entry.path : state.fsPath)
  );
  addContextMenuItem(menu, "Refresh", () => loadDirectory(state.fsPath));
  if (state.fsPath !== "/") {
    addContextMenuItem(menu, "Go to parent", () => loadDirectory(parentPath(state.fsPath)));
  }

  menu.classList.remove("hidden");
  menu.setAttribute("aria-hidden", "false");
  menu.style.left = "0px";
  menu.style.top = "0px";

  const rect = menu.getBoundingClientRect();
  let left = x;
  let top = y;
  if (left + rect.width > window.innerWidth - 8) {
    left = window.innerWidth - rect.width - 8;
  }
  if (top + rect.height > window.innerHeight - 8) {
    top = window.innerHeight - rect.height - 8;
  }
  menu.style.left = `${Math.max(8, left)}px`;
  menu.style.top = `${Math.max(8, top)}px`;
}

function addContextMenuItem(menu, label, action) {
  const item = document.createElement("button");
  item.type = "button";
  item.className = "context-item";
  item.setAttribute("role", "menuitem");
  item.textContent = label;
  item.addEventListener("click", () => {
    hideContextMenu();
    action();
  });
  menu.append(item);
}

function hideContextMenu() {
  const menu = $("#context-menu");
  if (!menu || menu.classList.contains("hidden")) {
    return;
  }
  menu.classList.add("hidden");
  menu.setAttribute("aria-hidden", "true");
  menu.innerHTML = "";
}

async function copyToClipboard(text) {
  let copied = false;

  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
      copied = true;
    }
  } catch (error) {
    copied = false;
  }

  if (!copied) {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.append(area);
    area.select();
    try {
      copied = document.execCommand("copy");
    } catch (error) {
      copied = false;
    }
    area.remove();
  }

  if (copied) {
    $("#fs-error").textContent = "";
    showFilesystemMessage("Path copied to clipboard");
  } else {
    showFilesystemMessage("Unable to copy path", true);
  }
}

function showFilesystemMessage(message, isError = false) {
  if (isError) {
    $("#fs-error").textContent = message;
    return;
  }

  const count = state.fsEntries.length;
  $("#fs-status").textContent = message;
  clearTimeout(fsMessageTimer);
  fsMessageTimer = setTimeout(() => {
    if (!state.fsBusy) {
      $("#fs-status").textContent = `${count} item${count === 1 ? "" : "s"}`;
    }
  }, 1800);
}

async function loadApps(force = false) {
  if (state.appsLoading || (!force && state.appsLoaded)) {
    if (state.appsLoaded) {
      renderApps();
    }
    return;
  }

  state.appsLoading = true;
  $("#apps-count").textContent = "Loading...";

  try {
    state.apps = await invoke("get_apps");
    state.appsLoaded = true;
    $("#apps-count").textContent = `${state.apps.length} apps`;
    renderApps();
  } catch (error) {
    state.apps = [];
    state.appsLoaded = false;
    $("#apps-count").textContent = "Failed to load apps";
    $("#apps-list").innerHTML = `<div class="empty-list">${escapeHtml(String(error))}</div>`;
  } finally {
    state.appsLoading = false;
  }
}

function renderApps() {
  const list = $("#apps-list");
  const query = $("#apps-search").value.trim().toLowerCase();
  const filtered = query
    ? state.apps.filter(
        (app) =>
          app.package.toLowerCase().includes(query) || app.label.toLowerCase().includes(query)
      )
    : state.apps;

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-list">No applications found</div>`;
    return;
  }

  list.innerHTML = filtered
    .map(
      (app) => `
        <div class="list-item app-item">
          <div>
            <div class="title">${escapeHtml(app.label)}</div>
            <div class="sub">${escapeHtml(app.package)}</div>
          </div>
          <button class="btn secondary app-inspect" type="button" data-package="${escapeHtml(
            app.package
          )}" data-label="${escapeHtml(app.label)}">Inspect</button>
        </div>
      `
    )
    .join("");
}

function setupUsb() {
  $("#usb-status-refresh").addEventListener("click", loadUsbStatus);
  $("#usb-storage-refresh").addEventListener("click", () => loadUsbStorage());
  $("#usb-storage-go").addEventListener("click", () => loadUsbStorage($("#usb-storage-path").value.trim()));
  $("#usb-storage-up").addEventListener("click", () => {
    const current = state.usbStoragePath;
    if (!current) {
      return;
    }
    const root = currentUsbRoot();
    if (root && (current === root || current === `${root}/`)) {
      return;
    }
    loadUsbStorage(parentPath(current));
  });

  $$("[data-usb-folder]").forEach((button) => {
    button.addEventListener("click", () => {
      const root = currentUsbRoot();
      if (!root) {
        loadUsbStatus();
        return;
      }
      const folder = button.dataset.usbFolder;
      loadUsbStorage(folder ? `${root}/${folder}` : root);
    });
  });

  $("#usb-mtp-roots").addEventListener("click", (event) => {
    const button = event.target.closest("[data-usb-root]");
    if (button) {
      loadUsbStorage(button.dataset.usbRoot);
    }
  });

  $("#usb-storage-breadcrumb").addEventListener("click", (event) => {
    const button = event.target.closest("[data-usb-crumb]");
    if (button) {
      loadUsbStorage(button.dataset.usbCrumb);
    }
  });
}

async function loadUsbStatus() {
  if (state.usbLoading) {
    return;
  }
  state.usbLoading = true;
  setViewStatus("#usb-status-status", "Scanning...");
  try {
    state.usbStatus = await invoke("get_usb_status");
    renderUsbStatus();
  } catch (error) {
    setViewStatus("#usb-status-status", String(error), true);
  } finally {
    state.usbLoading = false;
  }
}

function renderUsbStatus() {
  const status = state.usbStatus;
  if (!status) {
    return;
  }

  $("#usb-status-platform").textContent = status.platform || "--";
  $("#usb-status-mount-count").textContent = String(status.mtp_roots.length);
  $("#usb-status-message").textContent = status.message || "--";
  $("#usb-device-count").textContent = `${status.devices.length} devices`;
  setViewStatus("#usb-status-status", status.mtp_roots.length ? "MTP storage ready" : "No MTP mount");

  const roots = $("#usb-mtp-roots");
  roots.innerHTML = status.mtp_roots.length
    ? status.mtp_roots
        .map(
          (root) => `
            <div class="list-item">
              <div>
                <div class="title mono">${escapeHtml(root)}</div>
                <div class="sub">MTP storage mount</div>
              </div>
              <button class="btn secondary" type="button" data-usb-root="${escapeHtml(root)}">Browse</button>
            </div>
          `
        )
        .join("")
    : `<div class="empty-state">No MTP storage detected. Unlock the device and select File Transfer/MTP mode.</div>`;

  const devices = $("#usb-devices");
  devices.innerHTML = status.devices.length
    ? status.devices
        .map(
          (device) => `
            <div class="list-item">
              <div>
                <div class="title mono">${escapeHtml(device.id)}</div>
                <div class="sub">${escapeHtml(device.location)}</div>
              </div>
              <div class="notification-meta">
                <div class="sub">${escapeHtml(device.description)}</div>
              </div>
            </div>
          `
        )
        .join("")
    : `<div class="empty-state">No USB devices reported by this computer.</div>`;
}

async function loadUsbStorage(path) {
  if (state.usbStorageBusy) {
    return;
  }

  let target = path || state.usbStoragePath;
  if (!target) {
    if (!state.usbStatus) {
      await loadUsbStatus();
    }
    target = state.usbStatus && state.usbStatus.mtp_roots.length ? state.usbStatus.mtp_roots[0] : null;
  }
  if (!target) {
    setViewStatus("#usb-storage-status", "No MTP storage", true);
    $("#usb-storage-error").textContent =
      (state.usbStatus && state.usbStatus.message) || "Connect the device in File Transfer/MTP mode.";
    return;
  }

  state.usbStorageBusy = true;
  $("#usb-storage-error").textContent = "";
  setViewStatus("#usb-storage-status", "Loading...");
  try {
    const listing = await invoke("list_mtp_directory", { path: target });
    state.usbStoragePath = listing.path;
    renderUsbStorage(listing);
    setViewStatus("#usb-storage-status", `${listing.entries.length} items`);
  } catch (error) {
    $("#usb-storage-error").textContent = String(error);
    setViewStatus("#usb-storage-status", "Error", true);
  } finally {
    state.usbStorageBusy = false;
  }
}

function currentUsbRoot() {
  const roots = (state.usbStatus && state.usbStatus.mtp_roots) || [];
  const current = state.usbStoragePath || "";
  return roots.find((root) => current === root || current.startsWith(`${root}/`)) || roots[0] || "";
}

function renderUsbBreadcrumb(path) {
  const root = currentUsbRoot();
  const relative = root && (path === root || path.startsWith(`${root}/`)) ? path.slice(root.length) : path;
  const parts = relative.split("/").filter(Boolean);
  let current = root || "";
  const crumbs = [
    `<button class="chip" type="button" data-usb-crumb="${escapeHtml(root || path)}">${escapeHtml(root ? "MTP device" : "/")}</button>`,
  ];

  for (const part of parts) {
    current = current ? `${current}/${part}` : `/${part}`;
    crumbs.push(`<button class="chip" type="button" data-usb-crumb="${escapeHtml(current)}">${escapeHtml(part)}</button>`);
  }

  $("#usb-storage-breadcrumb").innerHTML = crumbs.join("");
}

function renderUsbStorage(listing) {
  $("#usb-storage-path").value = listing.path;
  $("#usb-storage-count").textContent = `${listing.entries.length} items`;
  renderUsbBreadcrumb(listing.path);

  const list = $("#usb-storage-list");
  list.innerHTML = "";

  for (const entry of listing.entries) {
    const row = document.createElement("div");
    row.className = "fs-row";
    row.setAttribute("role", "listitem");

    const name = document.createElement("span");
    name.className = "fs-name";
    name.textContent = entry.name;
    if (entry.is_link && entry.link_target) {
      name.title = `→ ${entry.link_target}`;
    }

    const size = document.createElement("span");
    size.className = "fs-size";
    size.textContent = entry.is_dir ? "—" : formatFileSize(entry.size);

    const modified = document.createElement("span");
    modified.className = "fs-modified";
    modified.textContent = entry.modified || "--";

    const permissions = document.createElement("span");
    permissions.className = "fs-perms";
    permissions.textContent = entry.permissions || "--";

    row.append(name, size, modified, permissions);
    if (entry.is_dir) {
      row.addEventListener("click", () => loadUsbStorage(entry.path));
    } else if (isImageEntry(entry)) {
      row.title = `${entry.name} — double-click to preview`;
      row.addEventListener("dblclick", (event) => {
        event.preventDefault();
        openLocalImagePreview(entry.path, entry.name);
      });
    }
    list.append(row);
  }
}

async function openLocalImagePreview(path, name) {
  const token = ++imagePreviewToken;
  hideContextMenu();
  $("#image-preview-title").textContent = name;
  $("#image-preview-path").textContent = path;
  const image = $("#image-preview-image");
  const loading = $("#image-preview-loading");
  const error = $("#image-preview-error");
  image.classList.add("hidden");
  image.removeAttribute("src");
  image.alt = name;
  error.textContent = "";
  error.classList.add("hidden");
  loading.textContent = "Loading image...";
  loading.classList.remove("hidden");
  $("#image-preview").classList.remove("hidden");
  $("#image-preview").setAttribute("aria-hidden", "false");
  $("#image-preview-close").focus();

  try {
    const preview = await invoke("read_local_image_preview", { path });
    if (token !== imagePreviewToken) {
      return;
    }
    image.onload = () => {
      if (token !== imagePreviewToken) {
        return;
      }
      loading.classList.add("hidden");
      image.classList.remove("hidden");
    };
    image.onerror = () => {
      if (token !== imagePreviewToken) {
        return;
      }
      image.classList.add("hidden");
      loading.classList.add("hidden");
      error.textContent = "Unable to decode this image.";
      error.classList.remove("hidden");
    };
    image.src = `data:${preview.mime};base64,${preview.data}`;
  } catch (previewError) {
    if (token !== imagePreviewToken) {
      return;
    }
    image.classList.add("hidden");
    loading.classList.add("hidden");
    error.textContent = String(previewError);
    error.classList.remove("hidden");
  }
}

function setupApps() {
  $("#apps-list").addEventListener("click", (event) => {
    const button = event.target.closest(".app-inspect");
    if (!button) {
      return;
    }
    openAppDetail(button.dataset.package, button.dataset.label);
  });

  $("#app-detail-close").addEventListener("click", closeAppDetail);
  $("#app-detail").addEventListener("click", (event) => {
    if (event.target === $("#app-detail")) {
      closeAppDetail();
    }
  });
  $("#app-launch").addEventListener("click", launchSelectedApp);
  $("#app-stop").addEventListener("click", stopSelectedApp);
  $("#app-logs-toggle").addEventListener("click", toggleAppLogs);
  $("#app-refresh").addEventListener("click", loadAppDetails);

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || $("#app-detail").classList.contains("hidden")) {
      return;
    }
    if (!$("#confirm-dialog").classList.contains("hidden")) {
      return;
    }
    closeAppDetail();
  });
}

let confirmResolve = null;

function setupConfirmDialog() {
  $("#confirm-cancel").addEventListener("click", () => closeConfirmDialog(false));
  $("#confirm-ok").addEventListener("click", () => closeConfirmDialog(true));
  $("#confirm-dialog").addEventListener("click", (event) => {
    if (event.target === $("#confirm-dialog")) {
      closeConfirmDialog(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !$("#confirm-dialog").classList.contains("hidden")) {
      closeConfirmDialog(false);
    }
  });
}

function confirmAction(title, message, confirmLabel) {
  return new Promise((resolve) => {
    if (confirmResolve) {
      confirmResolve(false);
    }

    confirmResolve = resolve;
    $("#confirm-title").textContent = title;
    $("#confirm-message").textContent = message;
    $("#confirm-ok").textContent = confirmLabel || "Confirm";
    $("#confirm-dialog").classList.remove("hidden");
    $("#confirm-dialog").setAttribute("aria-hidden", "false");
    $("#confirm-ok").focus();
  });
}

function closeConfirmDialog(result) {
  const overlay = $("#confirm-dialog");
  if (overlay.classList.contains("hidden")) {
    return;
  }

  overlay.classList.add("hidden");
  overlay.setAttribute("aria-hidden", "true");
  const resolve = confirmResolve;
  confirmResolve = null;
  if (resolve) {
    resolve(result);
  }
}

function openAppDetail(packageName, label) {
  const detail = state.appDetail;
  if (detail.logActive) {
    stopAppLogs();
  }

  detail.package = packageName;
  detail.label = label || packageName;
  detail.details = null;
  detail.logSession = null;
  detail.logActive = false;

  $("#app-detail-title").textContent = detail.label;
  $("#app-detail-package").textContent = packageName;
  $("#app-log-output").textContent = "";
  $("#app-log-status").textContent = "Not streaming";
  $("#app-log-status").className = "muted small";
  $("#app-logs-toggle").textContent = "Start logs";
  $("#app-running").textContent = "--";
  $("#app-pids").textContent = "--";
  $("#app-apk-size").textContent = "--";
  $("#app-data-size").textContent = "--";
  $("#app-cache-size").textContent = "--";
  $("#app-services").textContent = "--";
  $("#app-jobs").textContent = "--";
  $("#app-alarms").textContent = "--";
  $("#app-permissions").innerHTML = "";
  $("#app-permissions-count").textContent = "";
  setAppActionStatus("Loading...", "");

  $("#app-detail").classList.remove("hidden");
  $("#app-detail").setAttribute("aria-hidden", "false");
  loadAppDetails();
}

function closeAppDetail() {
  if (state.appDetail.logActive) {
    stopAppLogs();
  }

  state.appDetail.package = null;
  state.appDetail.details = null;
  const overlay = $("#app-detail");
  overlay.classList.add("hidden");
  overlay.setAttribute("aria-hidden", "true");
}

function setAppActionStatus(text, kind) {
  const status = $("#app-action-status");
  status.textContent = text;
  status.className = `status-text ${kind || ""}`.trim();
}

async function loadAppDetails() {
  const detail = state.appDetail;
  if (!detail.package) {
    return;
  }

  const token = ++detail.loadToken;
  detail.loading = true;
  setAppActionStatus("Refreshing...", "");

  try {
    const data = await invoke("get_app_details", { package: detail.package });
    if (token !== detail.loadToken || detail.package !== data.package) {
      return;
    }
    detail.details = data;
    renderAppDetails(data);
    setAppActionStatus(data.running ? "● Running" : "● Stopped", data.running ? "success" : "");
  } catch (error) {
    if (token === detail.loadToken) {
      setAppActionStatus(String(error), "error");
    }
  } finally {
    if (token === detail.loadToken) {
      detail.loading = false;
    }
  }
}

function renderAppDetails(details) {
  $("#app-running").textContent = details.running ? "Yes" : "No";
  $("#app-pids").textContent =
    details.pids && details.pids.length > 0 ? details.pids.join(", ") : "--";
  $("#app-apk-size").textContent = formatFileSize(details.apk_size);
  $("#app-data-size").textContent = formatFileSize(details.data_size);
  $("#app-cache-size").textContent = formatFileSize(details.cache_size);
  $("#app-services").textContent = formatAppList(details.services, "No active services");
  $("#app-jobs").textContent = formatAppList(details.jobs, "No scheduled jobs");
  $("#app-alarms").textContent = formatAppList(details.alarms, "No pending alarms");
  renderAppPermissions(details.permissions || []);
}

function formatAppList(items, emptyText) {
  if (!Array.isArray(items) || items.length === 0) {
    return emptyText;
  }
  return items.join("\n");
}

function renderAppPermissions(permissions) {
  const list = $("#app-permissions");
  const count = permissions.length;
  $("#app-permissions-count").textContent = `${count} permission${count === 1 ? "" : "s"}`;

  if (count === 0) {
    list.innerHTML = `<div class="empty-list">No permissions reported</div>`;
    return;
  }

  list.innerHTML = permissions
    .map((permission) => {
      const granted = permission.granted;
      const badge = granted === true ? "Granted" : granted === false ? "Denied" : "Declared";
      const kind = granted === true ? "success" : granted === false ? "error" : "";
      const suffix = permission.runtime ? " · runtime" : "";
      return `
        <div class="permission-row">
          <code class="permission-name">${escapeHtml(permission.name)}</code>
          <span class="permission-badge ${kind}">${badge}${suffix}</span>
        </div>
      `;
    })
    .join("");
}

async function launchSelectedApp() {
  const detail = state.appDetail;
  if (!detail.package) {
    return;
  }

  setAppActionStatus("Launching...", "");
  try {
    const message = await invoke("launch_app", { package: detail.package });
    setAppActionStatus(message, "success");
    await loadAppDetails();
  } catch (error) {
    setAppActionStatus(String(error), "error");
  }
}

async function stopSelectedApp() {
  const detail = state.appDetail;
  if (!detail.package) {
    return;
  }

  const confirmed = await confirmAction(
    "Force stop application",
    `Force stop ${detail.label}? Any unsaved state in the app will be lost.`,
    "Force stop"
  );
  if (!confirmed || !detail.package) {
    return;
  }

  setAppActionStatus("Stopping...", "");
  try {
    const message = await invoke("stop_app", { package: detail.package });
    setAppActionStatus(message, "success");
    await loadAppDetails();
  } catch (error) {
    setAppActionStatus(String(error), "error");
  }
}

async function toggleAppLogs() {
  if (state.appDetail.logActive) {
    await stopAppLogs();
  } else {
    await startAppLogs();
  }
}

async function startAppLogs() {
  const detail = state.appDetail;
  if (!detail.package) {
    return;
  }

  const session = Date.now();
  detail.logSession = session;
  detail.logActive = true;
  $("#app-log-output").textContent = "";
  $("#app-logs-toggle").textContent = "Stop logs";
  $("#app-log-status").textContent = "● Streaming";
  $("#app-log-status").className = "status-text success";

  try {
    await invoke("start_app_logs", { package: detail.package, session });
  } catch (error) {
    detail.logActive = false;
    detail.logSession = null;
    $("#app-logs-toggle").textContent = "Start logs";
    $("#app-log-status").textContent = String(error);
    $("#app-log-status").className = "status-text error";
  }
}

async function stopAppLogs() {
  const detail = state.appDetail;
  const wasActive = detail.logActive;
  detail.logActive = false;
  detail.logSession = null;
  $("#app-logs-toggle").textContent = "Start logs";
  $("#app-log-status").textContent = "Not streaming";
  $("#app-log-status").className = "muted small";

  if (wasActive) {
    try {
      await invoke("stop_app_logs");
    } catch (error) {
      console.error(error);
    }
  }
}

function appendAppLog(line) {
  const output = $("#app-log-output");
  output.append(document.createTextNode(`${line}\n`));
  while (output.childNodes.length > 3000) {
    output.removeChild(output.firstChild);
  }
  output.scrollTop = output.scrollHeight;
}

async function listenAppLogs() {
  if (!window.__TAURI__ || !window.__TAURI__.event) {
    return;
  }

  await window.__TAURI__.event.listen("app-log", (event) => {
    const payload = event.payload;
    const detail = state.appDetail;
    if (!payload || !detail.logActive || payload.session !== detail.logSession) {
      return;
    }
    appendAppLog(payload.line);
  });

  await window.__TAURI__.event.listen("app-log-end", (event) => {
    const payload = event.payload;
    const detail = state.appDetail;
    if (!payload || payload.session !== detail.logSession) {
      return;
    }
    detail.logActive = false;
    $("#app-logs-toggle").textContent = "Start logs";
    $("#app-log-status").textContent = "Stream ended";
    $("#app-log-status").className = "muted small";
  });
}

function setViewStatus(selector, text, isError = false) {
  const element = $(selector);
  if (!element) {
    return;
  }
  element.textContent = text;
  element.className = `status-text${isError ? " error" : ""}`;
}

async function loadNotifications() {
  if (state.notificationsLoading) {
    return;
  }
  state.notificationsLoading = true;
  setViewStatus("#notifications-status", "Loading...");
  try {
    state.notifications = await invoke("get_notifications");
    renderNotifications();
  } catch (error) {
    setViewStatus("#notifications-status", String(error), true);
  } finally {
    state.notificationsLoading = false;
  }
}

function renderNotifications() {
  const list = $("#notifications-list");
  const entries = state.notifications;
  setViewStatus("#notifications-status", `${entries.length} active`);

  if (!entries.length) {
    list.innerHTML = `<div class="empty-state">No active notifications</div>`;
    return;
  }

  list.innerHTML = entries
    .map((entry) => {
      const meta = [
        entry.channel,
        entry.importance !== null && entry.importance !== undefined ? `importance ${entry.importance}` : "",
        entry.tag,
      ]
        .filter(Boolean)
        .join(" · ");
      const created = entry.created_at_ms ? new Date(entry.created_at_ms).toLocaleString() : "";
      return `
        <div class="list-item notification-item">
          <div class="notification-main">
            <div class="title">${escapeHtml(entry.title || "(untitled)")}</div>
            <div class="sub">${escapeHtml(entry.text || "No text")}</div>
            <div class="sub mono">${escapeHtml(entry.package)}${entry.id ? ` #${escapeHtml(entry.id)}` : ""}</div>
          </div>
          <div class="notification-meta">
            <div class="sub">${escapeHtml(meta)}</div>
            <div class="sub">${escapeHtml(created)}</div>
          </div>
        </div>
      `;
    })
    .join("");
}

async function loadActivity() {
  if (state.activityLoading) {
    return;
  }
  state.activityLoading = true;
  setViewStatus("#activity-status", "Loading...");
  try {
    state.activity = await invoke("get_activity_state");
    renderActivity();
  } catch (error) {
    setViewStatus("#activity-status", String(error), true);
  } finally {
    state.activityLoading = false;
  }
}

function renderActivity() {
  const activity = state.activity;
  if (!activity) {
    return;
  }

  $("#activity-foreground").textContent = activity.foreground_package || "--";
  $("#activity-component").textContent = activity.foreground_component || "--";
  $("#activity-task-count").textContent = `${activity.tasks.length} tasks`;
  setViewStatus("#activity-status", activity.foreground_package ? "Foreground detected" : "No foreground activity");

  const list = $("#activity-tasks");
  if (!activity.tasks.length) {
    list.innerHTML = `<div class="empty-state">No recent tasks reported</div>`;
    return;
  }

  list.innerHTML = activity.tasks
    .map(
      (task) => `
        <div class="list-item task-item">
          <div>
            <div class="title">Task #${escapeHtml(task.id)} · ${escapeHtml(task.package)}</div>
            <div class="sub mono">${escapeHtml(task.activity || "No top activity")}</div>
          </div>
          <span class="badge ${task.visible ? "badge-success" : ""}">${task.visible ? "visible" : "hidden"}</span>
        </div>
      `
    )
    .join("");
}

async function loadUsage() {
  if (state.usageLoading) {
    return;
  }
  state.usageLoading = true;
  setViewStatus("#usage-status", "Loading...");
  try {
    state.usage = await invoke("get_app_usage");
    renderUsage();
  } catch (error) {
    setViewStatus("#usage-status", String(error), true);
  } finally {
    state.usageLoading = false;
  }
}

function renderUsage() {
  const entries = state.usage;
  setViewStatus("#usage-status", `${entries.length} processes`);

  if (!entries.length) {
    $("#usage-list").innerHTML = `<div class="empty-state">No process usage reported</div>`;
    return;
  }

  $("#usage-list").innerHTML = entries
    .map(
      (entry) => `
        <div class="fs-row usage-row" role="listitem">
          <span class="usage-name mono">${escapeHtml(entry.package)}</span>
          <span>${formatNumber(entry.cpu_percent, 1)}%</span>
          <span>${formatFileSize(entry.pss_kb * 1024)}</span>
        </div>
      `
    )
    .join("");
}

async function loadPower() {
  if (state.powerLoading) {
    return;
  }
  state.powerLoading = true;
  setViewStatus("#power-status", "Loading...");
  try {
    state.power = await invoke("get_power_report");
    renderPower();
  } catch (error) {
    setViewStatus("#power-status", String(error), true);
  } finally {
    state.powerLoading = false;
  }
}

function renderPower() {
  const report = state.power;
  if (!report) {
    return;
  }

  $("#power-wakefulness").textContent = report.wakefulness;
  $("#power-doze").textContent = `${report.doze_state} / ${report.light_doze_state}`;
  $("#power-saver").textContent = report.battery_saver ? "On" : "Off";
  $("#power-charging").textContent = report.powered ? "Yes" : "No";
  $("#power-wakelock-count").textContent = `${report.wakelocks.length} locks`;
  setViewStatus("#power-status", report.battery_saver ? "Battery saver active" : "Normal power mode");

  const list = $("#power-wakelocks");
  if (!report.wakelocks.length) {
    list.innerHTML = `<div class="empty-state">No wake locks held</div>`;
    return;
  }

  list.innerHTML = report.wakelocks
    .map(
      (lock) => `
        <div class="list-item">
          <div>
            <div class="title mono">${escapeHtml(lock.kind)}</div>
            <div class="sub">${escapeHtml(lock.tag || "unknown tag")}</div>
          </div>
          <div class="notification-meta">
            <div class="sub">${escapeHtml(lock.held || "--")}</div>
            <div class="sub">${lock.uid ? `uid ${escapeHtml(lock.uid)}` : ""}${lock.pid ? ` · pid ${escapeHtml(lock.pid)}` : ""}</div>
          </div>
        </div>
      `
    )
    .join("");
}

async function loadSensors() {
  if (state.sensorsLoading) {
    return;
  }
  state.sensorsLoading = true;
  setViewStatus("#sensors-status", "Loading...");
  try {
    state.sensorSnapshot = await invoke("get_sensor_snapshot");
    renderSensors();
  } catch (error) {
    setViewStatus("#sensors-status", String(error), true);
  } finally {
    state.sensorsLoading = false;
  }
}

function renderSensors() {
  const snapshot = state.sensorSnapshot;
  const zones = snapshot ? snapshot.thermal_zones : [];
  const sensors = snapshot ? snapshot.sensors : [];

  $("#thermal-status").textContent =
    snapshot && snapshot.thermal_status !== null && snapshot.thermal_status !== undefined
      ? `Thermal status ${snapshot.thermal_status}`
      : "No thermal data";
  setViewStatus("#sensors-status", snapshot ? "Live snapshot" : "--");
  $("#sensors-count").textContent = `${sensors.length} sensors`;

  $("#thermal-grid").innerHTML = zones.length
    ? zones
        .map(
          (zone) => `
            <div class="sensor-card">
              <div class="sensor-name">${escapeHtml(zone.name)}</div>
              <div class="sensor-type">${zone.status !== null && zone.status !== undefined ? `status ${zone.status}` : "thermal zone"}</div>
              <div class="sensor-values">${formatNumber(zone.temperature_c, 1)} °C</div>
            </div>
          `
        )
        .join("")
    : `<div class="sensor-card"><div class="sensor-name">No thermal zones reported</div><div class="sensor-type">The thermal HAL may be unavailable on this device</div></div>`;

  $("#sensors-grid").innerHTML = sensors.length
    ? sensors
        .map(
          (sensor) => `
            <div class="sensor-card">
              <div class="sensor-name">${escapeHtml(sensor.name)}</div>
              <div class="sensor-type">${escapeHtml(sensor.type_name)}${sensor.wake_up ? " · wake-up" : ""}</div>
              <div class="sensor-values">${sensor.values.length ? sensor.values.map((value) => formatNumber(value, 3)).join(", ") : "No recent events"}</div>
              <div class="sensor-vendor">${escapeHtml(sensor.vendor)}</div>
            </div>
          `
        )
        .join("")
    : `<div class="sensor-card"><div class="sensor-name">No sensors reported</div><div class="sensor-type">The sensor service did not return a sensor list</div></div>`;
}

function formatDuration(milliseconds) {
  if (!Number.isFinite(milliseconds) || milliseconds < 0) {
    return "--";
  }
  const total = Math.round(milliseconds / 1000);
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = total % 60;
  if (hours) {
    return `${hours}h ${minutes}m`;
  }
  if (minutes) {
    return `${minutes}m ${seconds}s`;
  }
  return `${seconds}s`;
}

function setupSessions() {
  $("#session-toggle").addEventListener("click", toggleSession);
  $("#sessions-refresh").addEventListener("click", () => {
    refreshSessionStatus();
    loadSessions();
  });
  $("#sessions-list").addEventListener("click", (event) => {
    const viewButton = event.target.closest("[data-session-view]");
    if (viewButton) {
      openSession(viewButton.dataset.sessionView);
      return;
    }
    const exportButton = event.target.closest("[data-session-export]");
    if (exportButton) {
      exportSession(exportButton.dataset.sessionExport, exportButton.dataset.format);
    }
  });
}

async function refreshSessionStatus() {
  try {
    state.sessionStatus = await invoke("get_session_status");
    renderSessionStatus();
  } catch (error) {
    console.error(error);
  }
}

function renderSessionStatus() {
  const status = state.sessionStatus;
  const toggle = $("#session-toggle");
  const label = $("#session-status");
  if (!toggle || !label) {
    return;
  }

  if (state.offline) {
    toggle.textContent = "Start recording";
    label.textContent = "Offline mode · recording requires a device";
    label.className = "session-status muted small";
    return;
  }

  if (status) {
    toggle.textContent = "Stop recording";
    label.textContent = `Recording "${status.name}" · ${status.event_count} events`;
    label.className = "session-status small recording";
  } else {
    toggle.textContent = "Start recording";
    label.textContent = "Not recording";
    label.className = "session-status muted small";
  }
}

function setSessionMessage(text, isError = false) {
  const label = $("#session-status");
  if (!label) {
    return;
  }
  label.textContent = text;
  label.className = `session-status small${isError ? " error" : ""}`;
}

async function toggleSession() {
  const toggle = $("#session-toggle");
  toggle.disabled = true;
  try {
    if (state.sessionStatus) {
      const summary = await invoke("stop_session");
      state.sessionStatus = null;
      renderSessionStatus();
      setSessionMessage(`Saved "${summary.name}" with ${summary.event_count} events`);
      await loadSessions();
    } else {
      const name = $("#session-name").value.trim();
      const summary = await invoke("start_session", { name: name || null });
      state.sessionStatus = summary;
      $("#session-name").value = "";
      renderSessionStatus();
    }
  } catch (error) {
    setSessionMessage(String(error), true);
  } finally {
    toggle.disabled = false;
  }
}

async function loadSessions() {
  if (state.sessionsLoading) {
    return;
  }
  state.sessionsLoading = true;
  try {
    state.sessions = await invoke("list_sessions");
    renderSessions();
  } catch (error) {
    $("#sessions-list").innerHTML = `<div class="empty-state">${escapeHtml(String(error))}</div>`;
  } finally {
    state.sessionsLoading = false;
  }
}

function renderSessions() {
  const sessions = state.sessions;
  $("#sessions-count").textContent = `${sessions.length} sessions`;

  if (!sessions.length) {
    $("#sessions-list").innerHTML = `<div class="empty-state">No recorded sessions yet. Start recording to capture device telemetry.</div>`;
    return;
  }

  $("#sessions-list").innerHTML = sessions
    .map((session) => {
      const start = new Date(session.started_at);
      const end = session.ended_at ? new Date(session.ended_at) : null;
      const duration = end ? formatDuration(end.getTime() - start.getTime()) : "recording";
      return `
        <div class="list-item session-item">
          <div>
            <div class="title">${escapeHtml(session.name)}</div>
            <div class="sub">${escapeHtml(start.toLocaleString())} · ${escapeHtml(duration)} · ${session.event_count} events</div>
          </div>
          <div class="row-actions session-actions">
            <button class="btn secondary" type="button" data-session-view="${escapeHtml(session.id)}">View events</button>
            <button class="btn secondary" type="button" data-session-export="${escapeHtml(session.id)}" data-format="csv">CSV</button>
            <button class="btn secondary" type="button" data-session-export="${escapeHtml(session.id)}" data-format="json">JSON</button>
          </div>
        </div>
      `;
    })
    .join("");
}

async function openSession(id) {
  try {
    const session = await invoke("get_session", { id });
    state.events = session.events.slice().reverse();
    $("#events-search").value = "";
    $("#events-category").value = "all categories";
    renderEvents();
    setView("events");
  } catch (error) {
    setSessionMessage(String(error), true);
  }
}

async function exportSession(id, format) {
  try {
    const result = await invoke("export_session", { id, format });
    setSessionMessage(`Exported ${result.events} events to ${result.path}`);
  } catch (error) {
    setSessionMessage(String(error), true);
  }
}

function setupLogs() {
  $("#logs-toggle").addEventListener("click", toggleDeviceLogs);
  $("#logs-clear").addEventListener("click", () => {
    $("#logs-output").textContent = "";
  });
}

async function toggleDeviceLogs() {
  if (state.deviceLogs.active) {
    await stopDeviceLogs();
  } else {
    await startDeviceLogs();
  }
}

async function startDeviceLogs() {
  const session = Date.now();
  state.deviceLogs = { session, active: true };
  $("#logs-output").textContent = "";
  $("#logs-toggle").textContent = "Stop";
  setViewStatus("#logs-status", "● Streaming");

  try {
    await invoke("start_device_logs", {
      session,
      buffer: $("#logs-buffer").value,
      level: $("#logs-level").value,
      tag: $("#logs-tag").value,
    });
  } catch (error) {
    state.deviceLogs.active = false;
    $("#logs-toggle").textContent = "Start";
    setViewStatus("#logs-status", String(error), true);
  }
}

async function stopDeviceLogs() {
  state.deviceLogs.active = false;
  $("#logs-toggle").textContent = "Start";
  setViewStatus("#logs-status", "● Stopped");
  try {
    await invoke("stop_device_logs");
  } catch (error) {
    console.error(error);
  }
}

function appendDeviceLog(line) {
  const output = $("#logs-output");
  output.append(document.createTextNode(`${line}\n`));
  while (output.childNodes.length > 4000) {
    output.removeChild(output.firstChild);
  }
  output.scrollTop = output.scrollHeight;
}

async function listenDeviceLogs() {
  if (!window.__TAURI__ || !window.__TAURI__.event) {
    return;
  }

  await window.__TAURI__.event.listen("device-log", (event) => {
    const payload = event.payload;
    if (!payload || !state.deviceLogs.active || payload.session !== state.deviceLogs.session) {
      return;
    }
    appendDeviceLog(payload.line);
  });

  await window.__TAURI__.event.listen("device-log-end", (event) => {
    const payload = event.payload;
    if (!payload || payload.session !== state.deviceLogs.session) {
      return;
    }
    state.deviceLogs.active = false;
    $("#logs-toggle").textContent = "Start";
    setViewStatus("#logs-status", "● Stream ended");
  });
}

let eventsFrame = null;

function scheduleEventsRender() {
  if (eventsFrame) {
    return;
  }
  eventsFrame = requestAnimationFrame(() => {
    eventsFrame = null;
    renderEvents();
  });
}

function renderEvents() {
  const list = $("#events-list");
  const query = $("#events-search").value.trim().toLowerCase();
  const category = $("#events-category").value.toLowerCase();

  $("#events-count").textContent = `${state.events.length} events`;

  const filtered = state.events.filter((event) => {
    if (category !== "all categories" && event.category !== category) {
      return false;
    }
    if (!query) {
      return true;
    }
    return (
      event.source.toLowerCase().includes(query) ||
      event.metric.toLowerCase().includes(query) ||
      formatValue(event.value).toLowerCase().includes(query)
    );
  });

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-list">No events yet</div>`;
    return;
  }

  list.innerHTML = filtered
    .map((event) => {
      const severityClass = ["info", "warning", "critical"].includes(event.severity)
        ? event.severity
        : "";
      return `
        <div class="event-item">
          <span class="event-dot ${severityClass}">●</span>
          <div>
            <div class="event-time">${escapeHtml(event.timestamp || "--")}</div>
            <div class="event-message">${escapeHtml(
              `${event.source}.${event.metric} = ${formatValue(event.value)}`
            )}</div>
            <div class="event-category">${escapeHtml(event.category.toUpperCase())}</div>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderBluetoothDevices(devices) {
  const list = $("#bt-list");
  const count = Array.isArray(devices) ? devices.length : 0;
  $("#bt-count").textContent = `${count} devices`;

  if (count === 0) {
    list.innerHTML = `<div class="empty-list">No paired devices</div>`;
    return;
  }

  list.innerHTML = devices
    .map((device) => {
      const connected = Boolean(device.connected);
      const paired = Boolean(device.paired);
      const status = connected ? "Connected" : paired ? "Paired" : "Available";
      return `
        <div class="list-item">
          <span class="dot ${connected ? "online" : ""}">${connected ? "●" : "○"}</span>
          <div>
            <div class="title">${escapeHtml(device.name || "Unknown Device")}</div>
            <div class="sub">${escapeHtml(device.address || "")}</div>
            <div class="sub">${status}</div>
          </div>
        </div>
      `;
    })
    .join("");
}

function updateHealth(score) {
  const element = $("#net-health-score");
  element.textContent = String(score);
  element.classList.remove("good", "fair", "bad");

  let status = "Critical";
  if (score >= 90) {
    status = "Excellent";
  } else if (score >= 75) {
    status = "Good";
  } else if (score >= 50) {
    status = "Fair";
  } else if (score >= 25) {
    status = "Poor";
  }

  if (score >= 75) {
    element.classList.add("good");
  } else if (score >= 25) {
    element.classList.add("fair");
  } else {
    element.classList.add("bad");
  }

  $("#net-health-status").textContent = status;
}

function updateBatteryMetric(metric, value) {
  if (metric === "level") {
    state.batteryLevel = value;
    $("#bat-level").textContent = `${value}%`;
    $("#ov-battery").textContent = `${value}%`;

    const progress = $("#battery-progress");
    const color = value < 20 ? "red" : value < 50 ? "yellow" : "green";
    progress.className = `progress-fill ${color}`;
    progress.style.width = `${Math.max(0, Math.min(100, value))}%`;
    $("#battery-progress-label").textContent = `${value}%`;
  } else if (metric === "temperature") {
    $("#bat-temp").textContent = `${formatNumber(value)}°C`;
  } else if (metric === "voltage") {
    $("#bat-voltage").textContent = `${formatNumber(value)} V`;
  } else if (metric === "status") {
    $("#bat-status").textContent = value;
  } else if (["health", "technology", "plugged"].includes(metric)) {
    setDetail($("#battery-details"), metric, value);
  }
}

function updatePerformance(metric, value) {
  const ramBar = $("#perf-ram-bar");
  const storageBar = $("#perf-storage-bar");

  if (metric === "ram_used") {
    state.ramUsed = value;
    $("#perf-ram").textContent = `${value} MB`;
    if (state.ramTotal > 0) {
      const percent = Math.round((state.ramUsed / state.ramTotal) * 100);
      ramBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
      $("#ov-ram").textContent = `${percent}%`;
    }
    state.charts.ram.push("ram", value);
  } else if (metric === "ram_total") {
    state.ramTotal = value;
    if (state.ramTotal > 0) {
      const percent = Math.round((state.ramUsed / state.ramTotal) * 100);
      ramBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
      $("#ov-ram").textContent = `${percent}%`;
    }
  } else if (metric === "storage_used") {
    state.storageUsed = value;
    $("#perf-storage").textContent = `${formatNumber(value / 1024)} GB`;
    const total = state.storageTotal > 0 ? state.storageTotal : 256 * 1024;
    const percent = Math.round((state.storageUsed / total) * 100);
    storageBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
    $("#ov-storage").textContent = `${percent}%`;
    updateStorageView();
  } else if (metric === "storage_total") {
    state.storageTotal = value;
    if (state.storageUsed > 0) {
      const percent = Math.round((state.storageUsed / state.storageTotal) * 100);
      storageBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
      $("#ov-storage").textContent = `${percent}%`;
    }
    updateStorageView();
  } else if (metric === "cpu_usage") {
    $("#perf-cpu").textContent = `${formatNumber(value)}%`;
    $("#ov-cpu").textContent = `${formatNumber(value)}%`;
    $("#perf-cpu-bar").style.width = `${Math.max(0, Math.min(100, value))}%`;
    state.charts.cpu.push("cpu", value);
  }
}

function updateStorageView() {
  if (state.storageUsed > 0) {
    $("#storage-used").textContent = `${formatNumber(state.storageUsed / 1024)} GB`;
  }
  if (state.storageTotal > 0) {
    $("#storage-total").textContent = `${formatNumber(state.storageTotal / 1024)} GB`;
  }
  if (state.storageTotal > 0) {
    const percent = Math.round((state.storageUsed / state.storageTotal) * 100);
    $("#storage-progress").style.width = `${Math.max(0, Math.min(100, percent))}%`;
    $("#storage-progress-label").textContent = `${percent}%`;
  }
}

function updateNetworkMetric(metric, value) {
  if (metric === "health") {
    updateHealth(value);
  } else if (metric === "latency") {
    $("#net-latency").textContent = `${formatNumber(value)} ms`;
    state.charts.latency.push("latency", value);
  } else if (metric === "packet_loss") {
    $("#net-loss").textContent = `${formatNumber(value)}%`;
  } else if (metric === "rx_rate") {
    $("#net-rx").textContent = `${formatNumber(value)} KB/s`;
    state.charts.throughput.push("rx", value);
  } else if (metric === "tx_rate") {
    $("#net-tx").textContent = `${formatNumber(value)} KB/s`;
    state.charts.throughput.push("tx", value);
  }
}

function updateWifiMetric(metric, value) {
  if (metric === "connected") {
    const status = $("#wifi-status");
    status.textContent = value ? "● Connected" : "● Disconnected";
    status.classList.toggle("success", Boolean(value));
  } else if (metric === "ssid") {
    $("#wifi-ssid").textContent = value;
  } else if (metric === "rssi") {
    $("#wifi-rssi").textContent = `${value} dBm`;
    state.charts.wifiSignal.push("rssi", value);
  } else if (metric === "link_speed") {
    $("#wifi-speed").textContent = `${value} Mbps`;
    state.charts.wifiSpeed.push("speed", value);
  } else if (["bssid", "frequency", "channel", "ip_address"].includes(metric)) {
    setDetail($("#wifi-details"), metric, value);
  }
}

function updateCellularMetric(metric, value) {
  if (metric === "network_type") {
    $("#cell-network-type").textContent = value;
  } else if (metric === "operator") {
    $("#cell-operator").textContent = value;
  } else if (metric === "rsrp") {
    $("#cell-rsrp").textContent = `${value} dBm`;
    state.charts.cellular.push("rsrp", value);
  } else if (metric === "rsrq") {
    $("#cell-rsrq").textContent = `${value} dB`;
    state.charts.cellular.push("rsrq", value);
  } else if (metric === "rssi") {
    $("#cell-rssi").textContent = `${value} dBm`;
  } else if (metric === "sinr") {
    $("#cell-sinr").textContent = `${value} dB`;
  } else if (["mcc_mnc", "state", "data_state", "roaming"].includes(metric)) {
    setDetail($("#cell-details"), metric, value);
  } else if (["cell_id", "tac", "pci", "band"].includes(metric)) {
    setDetail($("#cell-serving"), metric, value);
  }
}

function updateBluetoothMetric(metric, value) {
  if (metric === "enabled") {
    const status = $("#bt-status");
    status.textContent = value ? "● Enabled" : "● Disabled";
    status.classList.toggle("success", Boolean(value));
  } else if (metric === "devices") {
    renderBluetoothDevices(value);
  } else if (["adapter_address", "adapter_name", "adapter_state"].includes(metric)) {
    setDetail($("#bt-details"), metric, value);
  }
}

function handleMetric(event) {
  state.events.unshift(event);
  if (state.events.length > state.maxEvents) {
    state.events.pop();
  }
  scheduleEventsRender();

  if (state.sessionStatus && $("#view-sessions").classList.contains("active")) {
    state.sessionStatus.event_count += 1;
    renderSessionStatus();
  }

  const { category, source, metric, value } = event;

  if (category === "device") {
    if (metric === "build") {
      state.device.build_number = value;
    } else {
      state.device[metric] = value;
    }
    renderDeviceInfo();
    return;
  }

  if (category === "battery") {
    updateBatteryMetric(metric, value);
    return;
  }

  if (category === "performance") {
    updatePerformance(metric, value);
    return;
  }

  if (category === "network") {
    if (source === "network") {
      updateNetworkMetric(metric, value);
    } else if (source === "wifi") {
      updateWifiMetric(metric, value);
    } else if (source === "cellular") {
      updateCellularMetric(metric, value);
    } else if (source === "bluetooth") {
      updateBluetoothMetric(metric, value);
    }
  }
}

async function listenMetrics() {
  if (!window.__TAURI__ || !window.__TAURI__.event) {
    return;
  }
  await window.__TAURI__.event.listen("metric", (event) => {
    if (event.payload) {
      handleMetric(event.payload);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  injectIcons();
  setupNavigation();
  setupConnection();
  setupSearch();
  setupShell();
  setupFilesystem();
  setupApps();
  setupSessions();
  setupLogs();
  setupConfirmDialog();
  setupCharts();
  renderSessions();
  renderSessionStatus();
  renderEvents();
  listenMetrics().catch((error) => console.error(error));
  listenAppLogs().catch((error) => console.error(error));
  listenDeviceLogs().catch((error) => console.error(error));
  setupUsb();
  refreshDevices();
  refreshOfflineSessions();
  refreshOfflineUsbStatus();
});

window.addEventListener("resize", () => {
  renderAllCharts();
});
