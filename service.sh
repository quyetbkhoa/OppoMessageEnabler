#!/system/bin/sh
MODDIR="${0%/*}"

# Wait until boot completed
until [ "$(getprop sys.boot_completed)" = "1" ]; do
    sleep 1
done

# Wait for package manager to settle
sleep 3

# Make sure com.android.mms is enabled
pm enable com.android.mms 2>/dev/null || true

# Set com.android.mms as default SMS role holder
cmd role add-role-holder --user 0 android.app.role.SMS com.android.mms 2>/dev/null || true

# Disable Google Messages globally and across all user profiles (including App Cloner 998/999)
pm disable com.google.android.apps.messaging 2>/dev/null || true
for u in $(pm list users 2>/dev/null | grep -o 'UserInfo{[0-9]*' | cut -d{ -f2); do
    pm disable-user --user "$u" com.google.android.apps.messaging 2>/dev/null || true
done
