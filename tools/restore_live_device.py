"""One-time recovery for the audited CPH2745; run after installing the fixed ZIP.

Removes only the three verified old-module mounts, applies the tested SMS-only
overlay, and clears Google Messages' old disabled-user state. No reboot here.
"""
import shlex
import subprocess

SCRIPT = r'''set -eu
pending=/data/adb/modules_update/oppo_messages_enabler
backup=/data/adb/oppo_messages_enabler-backups/20261018-before-fix
test -f "$backup/module/post-fs-data.sh"
grep -q '^versionCode=201$' "$pending/module.prop"
test "$(readlink /proc/self/ns/mnt)" = "$(readlink /proc/1/ns/mnt)"
for path in /my_stock/etc/config/app_v2.xml /my_product/etc/config/app_v2.xml /my_product/etc/extension/feature_rsa4.0_t3_default_app.xml; do
    root="$(awk -v path="$path" '$5 == path {print $4}' /proc/1/mountinfo)"
    case "$root" in
        /adb/modules/oppo_messages_enabler/app_v2.xml|/adb/modules/oppo_messages_enabler/feature_rsa4.0_t3_default_app.xml) ;;
        *) echo "Refusing unexpected mount: $path ($root)" >&2; exit 1 ;;
    esac
done
for path in /my_product/etc/config/app_v2.xml /my_product/etc/extension/feature_rsa4.0_t3_default_app.xml /my_stock/etc/config/app_v2.xml; do
    umount "$path"
done
sh "$pending/post-fs-data.sh"
test ! -s "$pending/generated/boot.log"
for user in 0 998 999; do
    pm default-state --user "$user" com.google.android.apps.messaging
done
echo 'Recovery applied. Reboot still needed for OEM package scanning.'
'''

result = subprocess.run(["adb", "shell", "su -c " + shlex.quote(SCRIPT)], capture_output=True)
print(result.stdout.decode(), result.stderr.decode())
raise SystemExit(result.returncode)
