use std::sync::Arc;
use std::thread;
use std::time::{Duration, Instant};

use tauri::{AppHandle, Emitter};

use crate::adb::AdbClient;
use crate::collectors;
use crate::collectors::network::NetworkState;
use crate::models::MetricEvent;

pub fn start(app: AppHandle, adb: Arc<AdbClient>) {
    if adb.monitoring() {
        return;
    }

    adb.set_monitoring(true);

    thread::spawn(move || {
        let mut device_collected = false;
        let mut network_state = NetworkState::default();

        let mut last_device: Option<Instant> = None;
        let mut last_battery: Option<Instant> = None;
        let mut last_performance: Option<Instant> = None;
        let mut last_network: Option<Instant> = None;
        let mut last_wifi: Option<Instant> = None;
        let mut last_cellular: Option<Instant> = None;
        let mut last_bluetooth: Option<Instant> = None;

        while adb.monitoring() && adb.serial().is_some() {
            let now = Instant::now();

            if !device_collected && due(last_device, now, Duration::from_secs(0)) {
                if let Ok(info) = collectors::device::collect(&adb) {
                    emit(&app, &collectors::device::events(&info));
                    device_collected = true;
                }
                last_device = Some(now);
            }

            if due(last_performance, now, Duration::from_secs(1)) {
                emit(&app, &collectors::performance::collect(&adb));
                last_performance = Some(now);
            }

            if due(last_network, now, Duration::from_secs(1)) {
                emit(
                    &app,
                    &collectors::network::collect(&adb, &mut network_state),
                );
                last_network = Some(now);
            }

            if due(last_wifi, now, Duration::from_secs(1)) {
                emit(&app, &collectors::wifi::collect(&adb));
                last_wifi = Some(now);
            }

            if due(last_cellular, now, Duration::from_secs(1)) {
                emit(&app, &collectors::cellular::collect(&adb));
                last_cellular = Some(now);
            }

            if due(last_battery, now, Duration::from_secs(5)) {
                emit(&app, &collectors::battery::collect(&adb));
                last_battery = Some(now);
            }

            if due(last_bluetooth, now, Duration::from_secs(5)) {
                emit(&app, &collectors::bluetooth::collect(&adb));
                last_bluetooth = Some(now);
            }

            thread::sleep(Duration::from_millis(200));
        }

        adb.set_monitoring(false);
    });
}

fn due(last: Option<Instant>, now: Instant, interval: Duration) -> bool {
    match last {
        Some(last) => now.duration_since(last) >= interval,
        None => true,
    }
}

fn emit(app: &AppHandle, events: &[MetricEvent]) {
    for event in events {
        let _ = app.emit("metric", event);
    }
}
