use crate::adb::AdbClient;
use crate::models::AppEntry;

pub fn collect(adb: &AdbClient) -> Result<Vec<AppEntry>, String> {
    let output = adb.execute("pm list packages")?;
    let mut apps = Vec::new();

    for line in output.lines() {
        let Some(package) = line.strip_prefix("package:") else {
            continue;
        };
        let package = package.trim();
        if package.is_empty() {
            continue;
        }

        apps.push(AppEntry {
            package: package.to_string(),
            label: label_for(package),
        });
    }

    apps.sort_by(|left, right| left.label.to_lowercase().cmp(&right.label.to_lowercase()));
    Ok(apps)
}

fn label_for(package: &str) -> String {
    let last = package.rsplit('.').next().unwrap_or(package);
    let mut characters = last.chars();

    match characters.next() {
        Some(first) => {
            first.to_uppercase().collect::<String>() + &characters.as_str().to_lowercase()
        }
        None => package.to_string(),
    }
}
