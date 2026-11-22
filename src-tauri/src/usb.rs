use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use base64::Engine as _;

use crate::models::{DirectoryListing, FsEntry, ImagePreview, UsbDevice, UsbStatus};

const MAX_IMAGE_BYTES: u64 = 20 * 1024 * 1024;

pub fn status() -> Result<UsbStatus, String> {
    let platform = std::env::consts::OS.to_string();
    let mut devices = Vec::new();
    let mut note = String::new();

    #[cfg(target_os = "linux")]
    {
        match Command::new("lsusb").output() {
            Ok(output) if output.status.success() => {
                devices = parse_lsusb(&String::from_utf8_lossy(&output.stdout));
            }
            Ok(_) => note = "lsusb could not list USB devices.".to_string(),
            Err(_) => note = "lsusb is not installed.".to_string(),
        }
    }

    #[cfg(not(target_os = "linux"))]
    {
        note = format!(
            "USB/MTP browsing is available from the file manager on {}. MDL can show guidance but cannot enumerate MTP mounts on this platform.",
            platform
        );
    }

    let mtp_roots = mtp_roots();
    let message = if !mtp_roots.is_empty() {
        format!("MTP storage is mounted at {} location(s).", mtp_roots.len())
    } else if note.is_empty() {
        "No MTP storage mount detected. Unlock the device and choose File Transfer/MTP mode."
            .to_string()
    } else {
        note
    };

    Ok(UsbStatus {
        supported: platform == "linux" && !mtp_roots.is_empty(),
        platform,
        devices,
        mtp_roots,
        message,
    })
}

pub fn list(path: &str) -> Result<DirectoryListing, String> {
    let root = validate_mtp_path(path)?;
    let mut entries = Vec::new();

    for item in fs::read_dir(&root).map_err(|error| format!("Unable to read folder: {error}"))? {
        let item = match item {
            Ok(item) => item,
            Err(_) => continue,
        };
        let path = item.path();
        let metadata = match fs::metadata(&path) {
            Ok(metadata) => metadata,
            Err(_) => continue,
        };
        let name = item.file_name().to_string_lossy().to_string();
        if name.is_empty() {
            continue;
        }
        let is_link = fs::symlink_metadata(&path)
            .map(|metadata| metadata.file_type().is_symlink())
            .unwrap_or(false);
        let modified = metadata
            .modified()
            .ok()
            .map(format_time)
            .unwrap_or_default();

        entries.push(FsEntry {
            path: path.to_string_lossy().to_string(),
            name,
            is_dir: metadata.is_dir(),
            is_link,
            size: if metadata.is_dir() { 0 } else { metadata.len() },
            modified,
            permissions: permissions(&metadata),
            link_target: None,
        });
    }

    entries.sort_by(|left, right| {
        right
            .is_dir
            .cmp(&left.is_dir)
            .then_with(|| left.name.to_lowercase().cmp(&right.name.to_lowercase()))
            .then_with(|| left.name.cmp(&right.name))
    });

    Ok(DirectoryListing {
        path: root.to_string_lossy().to_string(),
        entries,
    })
}

pub fn image_preview(path: &str) -> Result<ImagePreview, String> {
    let path = validate_mtp_path(path)?;
    let mime = image_mime(&path).ok_or_else(|| "Unsupported image type".to_string())?;
    let metadata = fs::metadata(&path).map_err(|error| format!("Unable to read image: {error}"))?;
    if metadata.len() > MAX_IMAGE_BYTES {
        return Err(format!(
            "Image is too large to preview ({} MB). The limit is {} MB.",
            metadata.len() / (1024 * 1024),
            MAX_IMAGE_BYTES / (1024 * 1024)
        ));
    }
    let data = fs::read(&path).map_err(|error| format!("Unable to read image: {error}"))?;
    Ok(ImagePreview {
        mime: mime.to_string(),
        data: base64::engine::general_purpose::STANDARD.encode(data),
    })
}

fn mtp_roots() -> Vec<String> {
    let mut candidates = Vec::new();

    if let Some(uid) = current_uid() {
        candidates.push(format!("/run/user/{uid}/gvfs"));
    }
    if let Ok(home) = std::env::var("HOME") {
        candidates.push(format!("{home}/.gvfs"));
        candidates.push(format!("{home}/gvfs"));
    }
    candidates.push("/media".to_string());
    candidates.push("/run/media".to_string());

    let mut roots = Vec::new();
    for directory in candidates {
        let entries = match fs::read_dir(&directory) {
            Ok(entries) => entries,
            Err(_) => continue,
        };
        for entry in entries.flatten() {
            let name = entry.file_name().to_string_lossy().to_string();
            if !name.to_lowercase().contains("mtp") {
                continue;
            }
            let path = entry.path();
            if !path.is_dir() {
                continue;
            }
            if let Ok(canonical) = path.canonicalize() {
                let value = canonical.to_string_lossy().to_string();
                if !roots.contains(&value) {
                    roots.push(value);
                }
            }
        }
    }

    roots
}

fn current_uid() -> Option<String> {
    if let Ok(uid) = std::env::var("UID") {
        if !uid.trim().is_empty() {
            return Some(uid.trim().to_string());
        }
    }
    let output = Command::new("id").arg("-u").output().ok()?;
    if !output.status.success() {
        return None;
    }
    let value = String::from_utf8_lossy(&output.stdout).trim().to_string();
    if value.is_empty() {
        None
    } else {
        Some(value)
    }
}

fn validate_mtp_path(path: &str) -> Result<PathBuf, String> {
    let requested = path.trim();
    if requested.is_empty() {
        return Err("Choose a folder".to_string());
    }
    let requested = PathBuf::from(requested);
    if !requested.is_absolute() {
        return Err("Invalid MTP path".to_string());
    }

    let canonical = requested
        .canonicalize()
        .map_err(|_| "MTP path is no longer available".to_string())?;
    let roots = mtp_roots();
    if roots.is_empty() {
        return Err(
            "No MTP storage detected. Unlock the device and select File Transfer/MTP mode."
                .to_string(),
        );
    }

    let allowed = roots
        .iter()
        .filter_map(|root| PathBuf::from(root).canonicalize().ok())
        .any(|root| canonical.starts_with(root));

    if !allowed {
        return Err("Path is outside detected MTP storage".to_string());
    }

    Ok(canonical)
}

fn parse_lsusb(output: &str) -> Vec<UsbDevice> {
    output
        .lines()
        .filter_map(|line| {
            let (location, details) = line.split_once(": ID ")?;
            let mut parts = details.split_whitespace();
            let id = parts.next()?;
            let description = details[id.len()..].trim();
            let (vendor, product) = match id.split_once(':') {
                Some((vendor, product)) => (Some(vendor.to_string()), Some(product.to_string())),
                None => (None, None),
            };
            Some(UsbDevice {
                id: id.to_string(),
                location: location.trim().to_string(),
                description: description.to_string(),
                vendor,
                product,
            })
        })
        .collect()
}

fn format_time(time: std::time::SystemTime) -> String {
    let datetime: chrono::DateTime<chrono::Local> = time.into();
    datetime.format("%b %d %H:%M").to_string()
}

#[cfg(unix)]
fn permissions(metadata: &fs::Metadata) -> String {
    use std::os::unix::fs::PermissionsExt;
    format!("{:o}", metadata.permissions().mode() & 0o7777)
}

#[cfg(not(unix))]
fn permissions(metadata: &fs::Metadata) -> String {
    if metadata.is_dir() {
        "dir".to_string()
    } else {
        "file".to_string()
    }
}

fn image_mime(path: &Path) -> Option<&'static str> {
    let extension = path.extension()?.to_str()?.to_ascii_lowercase();
    match extension.as_str() {
        "png" => Some("image/png"),
        "jpg" | "jpeg" | "jfif" => Some("image/jpeg"),
        "gif" => Some("image/gif"),
        "webp" => Some("image/webp"),
        "bmp" => Some("image/bmp"),
        "svg" => Some("image/svg+xml"),
        "avif" => Some("image/avif"),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_lsusb_output() {
        let output = "Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub\nBus 001 Device 004: ID 04e8:6860 Samsung Electronics Co., Ltd Galaxy series, misc. (MTP mode)\n";
        let devices = parse_lsusb(output);
        assert_eq!(devices.len(), 2);
        assert_eq!(devices[0].id, "1d6b:0002");
        assert_eq!(devices[1].location, "Bus 001 Device 004");
        assert_eq!(
            devices[1].description,
            "Samsung Electronics Co., Ltd Galaxy series, misc. (MTP mode)"
        );
        assert_eq!(devices[1].vendor.as_deref(), Some("04e8"));
    }
}
