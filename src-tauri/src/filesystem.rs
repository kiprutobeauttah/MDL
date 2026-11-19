use base64::Engine as _;

use crate::adb::{shell_quote, AdbClient};
use crate::models::{DirectoryListing, FsEntry, ImagePreview};

const MAX_IMAGE_BYTES: u64 = 20 * 1024 * 1024;

pub fn list(adb: &AdbClient, path: &str) -> Result<DirectoryListing, String> {
    let path = normalize_path(path);
    let result = adb.shell(&format!("LC_ALL=C ls -laL {}", shell_quote(&path)))?;

    if result.exit_code != 0 {
        return Err(error_message(&result.stdout, &result.stderr, &path));
    }

    let mut entries: Vec<FsEntry> = result
        .stdout
        .lines()
        .filter_map(|line| parse_entry(line, &path))
        .collect();

    entries.sort_by(|left, right| {
        right
            .is_dir
            .cmp(&left.is_dir)
            .then_with(|| left.name.to_lowercase().cmp(&right.name.to_lowercase()))
            .then_with(|| left.name.cmp(&right.name))
    });

    Ok(DirectoryListing { path, entries })
}

pub fn image_preview(adb: &AdbClient, path: &str) -> Result<ImagePreview, String> {
    let path = path.trim();
    if !path.starts_with('/') {
        return Err("Invalid image path".to_string());
    }

    let mime = image_mime(path).ok_or_else(|| "Unsupported image type".to_string())?;
    let quoted = shell_quote(path);
    let size = adb.shell(&format!("stat -c %s {quoted}"))?;

    if size.exit_code != 0 {
        return Err(error_message(&size.stdout, &size.stderr, path));
    }

    let bytes = size
        .stdout
        .trim()
        .parse::<u64>()
        .map_err(|_| format!("Unable to read {path}"))?;

    if bytes > MAX_IMAGE_BYTES {
        return Err(format!(
            "Image is too large to preview ({} MB). The limit is {} MB.",
            bytes / (1024 * 1024),
            MAX_IMAGE_BYTES / (1024 * 1024)
        ));
    }

    let data = adb.read_file_bytes(path)?;
    if data.len() as u64 > MAX_IMAGE_BYTES {
        return Err("Image is too large to preview".to_string());
    }

    Ok(ImagePreview {
        mime: mime.to_string(),
        data: base64::engine::general_purpose::STANDARD.encode(data),
    })
}

fn image_mime(path: &str) -> Option<&'static str> {
    let extension = std::path::Path::new(path)
        .extension()?
        .to_str()?
        .to_ascii_lowercase();

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

fn parse_entry(line: &str, directory: &str) -> Option<FsEntry> {
    let line = line.trim_end();
    if line.is_empty() || line.starts_with("total ") {
        return None;
    }

    let parts: Vec<&str> = line.split_whitespace().collect();
    if parts.len() < 8 {
        return None;
    }

    let permissions = parts[0];
    let first = permissions.chars().next()?;
    if !matches!(first, 'd' | '-' | 'l' | 'b' | 'c' | 'p' | 's') {
        return None;
    }

    let is_dir = first == 'd';
    let is_link = first == 'l';
    let size = parts[4].parse::<u64>().unwrap_or(0);
    let modified = format!("{} {}", parts[5], parts[6]);
    let raw_name = parts[7..].join(" ");

    if raw_name.is_empty() {
        return None;
    }

    let (name, link_target) = if is_link {
        match raw_name.split_once(" -> ") {
            Some((name, target)) => (name.to_string(), Some(target.to_string())),
            None => (raw_name, None),
        }
    } else {
        (raw_name, None)
    };

    if name == "." || name == ".." {
        return None;
    }

    Some(FsEntry {
        path: join_path(directory, &name),
        name,
        is_dir,
        is_link,
        size,
        modified,
        permissions: permissions.to_string(),
        link_target,
    })
}

fn normalize_path(path: &str) -> String {
    let path = path.trim();
    let path = if path.is_empty() {
        "/".to_string()
    } else if path.starts_with('/') {
        path.to_string()
    } else {
        format!("/{path}")
    };

    if path.len() > 1 {
        path.trim_end_matches('/').to_string()
    } else {
        path
    }
}

fn join_path(directory: &str, name: &str) -> String {
    if directory == "/" {
        format!("/{name}")
    } else {
        format!("{directory}/{name}")
    }
}

fn error_message(stdout: &str, stderr: &str, path: &str) -> String {
    let message = if stderr.trim().is_empty() {
        stdout.trim()
    } else {
        stderr.trim()
    };

    if message.is_empty() {
        format!("Unable to list {path}")
    } else {
        message.to_string()
    }
}
