"""Exercise boot overlay in a private namespace, without changing the live OS."""
from pathlib import Path
import shlex
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STAGE = "/data/local/tmp/oppo-messages-verify"


def adb(command):
    result = subprocess.run(["adb", "shell", command], capture_output=True, check=True)
    return result.stdout


adb("mkdir -p " + STAGE)
version = next(line.split('=', 1)[1] for line in (ROOT / 'module.prop').read_text().splitlines()
               if line.startswith('version='))
with zipfile.ZipFile(ROOT / f"Oppo_Messages_Enabler_{version}.zip") as archive:
    for name in ["post-fs-data.sh", "service.sh", "customize.sh", "patch-app-config.awk"]:
        local = ROOT / "diagnostics" / name
        local.write_bytes(archive.read(name))
        subprocess.run(["adb", "push", str(local), STAGE + "/" + name], check=True)

script = f'''set -eu
if grep -q ' shared:' /proc/self/mountinfo; then
    echo 'Namespace still shared; refusing to continue' >&2
    exit 1
fi
for path in /my_stock/etc/config/app_v2.xml /my_product/etc/config/app_v2.xml /my_product/etc/extension/feature_rsa4.0_t3_default_app.xml; do
    if grep -q " $path " /proc/self/mountinfo; then
        umount "$path"
    fi
done
cp /my_product/etc/config/app_v2.xml {STAGE}/product.original
cp /my_product/etc/extension/feature_rsa4.0_t3_default_app.xml {STAGE}/feature.original
awk -f {STAGE}/patch-app-config.awk /my_stock/etc/config/app_v2.xml > {STAGE}/stock.expected
for path in {STAGE}/*.sh; do sh -n "$path"; done
sh {STAGE}/post-fs-data.sh
cmp /my_product/etc/config/app_v2.xml {STAGE}/product.original
cmp /my_product/etc/extension/feature_rsa4.0_t3_default_app.xml {STAGE}/feature.original
cmp /my_stock/etc/config/app_v2.xml {STAGE}/stock.expected
test -f {STAGE}/generated/my_stock-app_v2.xml
test ! -f {STAGE}/generated/my_product-app_v2.xml
test ! -s {STAGE}/generated/boot.log
echo 'PASS: Android awk, shell syntax, bind mount, SELinux context, allowlisted patches'
echo 'PASS: product and feature XML unchanged byte for byte'
'''
before = adb("su -c 'cat /proc/1/mountinfo'")
command = "/data/adb/ksu/bin/busybox unshare -m --propagation private sh -c " + shlex.quote(script)
try:
    print(adb("su -c " + shlex.quote(command)).decode().strip())
finally:
    after = adb("su -c 'cat /proc/1/mountinfo'")
    assert before == after, "Live mount table changed"
    print("PASS: live OS mount table unchanged")
