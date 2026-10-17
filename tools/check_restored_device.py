"""Read-only verification against the saved pre-fix OEM XML after reboot."""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagnostics"
lines = []


def adb(command):
    return subprocess.run(["adb", "shell", command], capture_output=True,
                          text=True, check=True).stdout.strip()


def record(message):
    lines.append(message)
    print(message)


assert adb("getprop sys.boot_completed") == "1", "Boot not completed"
record("PASS: boot completed")
for remote, saved in [
    ("/my_product/etc/config/app_v2.xml", "my_product_etc_config_app_v2.xml"),
    ("/my_product/etc/extension/feature_rsa4.0_t3_default_app.xml",
     "my_product_etc_extension_feature_rsa4.0_t3_default_app.xml"),
    ("/my_stock/etc/config/app_v2.xml", "my_stock_etc_config_app_v2.xml"),
]:
    expected = ET.parse(OUT / saved).getroot()
    if remote.startswith("/my_stock/"):
        for node in expected:
            if node.tag == "disable" and node.get("pkg") in ("com.android.mms", "com.oplus.aiassistant"):
                node.tag = "enable"
    actual = ET.fromstring(adb("su -c 'cat " + remote + "'"))
    def rules(root):
        return (root.tag, root.attrib, [(x.tag, x.attrib) for x in root.iter()])
    assert rules(actual) == rules(expected), remote + " differs from expected OEM rules"
    record("PASS: " + remote + " contains only expected rules")

for package in ["com.oplus.aimemory", "com.oplus.omoji", "com.oplus.nearcomm", "com.android.mms", "com.oplus.aiassistant"]:
    location = adb("pm path " + package)
    assert location.startswith("package:"), package + " missing"
    record("PASS: " + package + " -> " + location)

role = adb("cmd role get-role-holders --user 0 android.app.role.SMS")
assert role == "com.android.mms", "Unexpected SMS role: " + role
record("PASS: Oppo Messages is default SMS app")
for user in [0, 998, 999]:
    disabled = adb(f"pm list packages -d --user {user} com.google.android.apps.messaging")
    state = 'disabled' if 'package:com.google.android.apps.messaging' in disabled else 'enabled/default'
    record(f"Google Messages user {user}: {state} (preserve user preference)")

boot_log = adb("su -c 'cat /data/adb/modules/oppo_messages_enabler/generated/boot.log'")
assert not boot_log, "Module boot log contains errors: " + boot_log
record("PASS: module boot log empty")
for package in ["com.google.android.mosey", "com.qpon.platform", "com.oplus.doublewake.settings"]:
    result = subprocess.run(["adb", "shell", "pm path " + package], capture_output=True, text=True)
    record(package + ": " + (result.stdout.strip() or "not registered; OEM rule restored"))
(OUT / "post-reboot-verification.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
