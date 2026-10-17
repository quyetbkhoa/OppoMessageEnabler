#!/system/bin/sh
MODDIR="${0%/*}"

# Wait until boot completed
until [ "$(getprop sys.boot_completed)" = "1" ]; do
    sleep 1
done

# Wait for package manager to settle
sleep 3

exec 2>>"$MODDIR/generated/boot.log"
# Never disable Google Messages or change cloned/work profiles.
# Assign once so later choices in Settings survive a reboot.
[ -f "$MODDIR/sms-role-configured" ] && exit 0
pm path --user 0 com.android.mms | grep -q '^package:' || exit 1
pm enable --user 0 com.android.mms || exit 1
cmd role add-role-holder --user 0 android.app.role.SMS com.android.mms || exit 1
current="$(cmd role get-role-holders --user 0 android.app.role.SMS)"
[ "$current" = com.android.mms ] || exit 1
touch "$MODDIR/sms-role-configured"
