"""Read original OEM XML in a private mount namespace; never unmount globally."""
import pathlib
import shlex
import subprocess

OUT = pathlib.Path(__file__).resolve().parents[1] / "diagnostics"
OUT.mkdir(exist_ok=True)
TARGETS = [
    "/my_stock/etc/config/app_v2.xml",
    "/my_product/etc/config/app_v2.xml",
    "/my_product/etc/extension/feature_rsa4.0_t3_default_app.xml",
]


def adb(command):
    return subprocess.run(["adb", "shell", command], check=True, capture_output=True).stdout


before = adb("su -c 'cat /proc/1/mountinfo'")
for target in TARGETS:
    name = target.strip("/").replace("/", "_")
    (OUT / (name + ".active")).write_bytes(adb("su -c " + shlex.quote("cat " + target)))
    script = "set -e\numount " + shlex.quote(target) + "\ncat " + shlex.quote(target)
    command = "/data/adb/ksu/bin/busybox unshare -m --propagation private sh -c " + shlex.quote(script)
    original = adb("su -c " + shlex.quote(command))
    (OUT / name).write_bytes(original)
    print(name, len(original), "bytes")
after = adb("su -c 'cat /proc/1/mountinfo'")
assert before == after, "Global mount table changed during audit"
print("Global mount table unchanged")
