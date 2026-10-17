SKIPUNZIP=0

ui_print "************************************"
ui_print "       Oppo Messages Enabler        "
ui_print "           by quyetbkhoa            "
ui_print "************************************"
ui_print "- Đang cài đặt Oppo Messages Enabler v1.0.3 + Mind Pilot..."
ui_print "- Thiết lập quyền và cấu hình..."

set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755

# No package-cache deletion or system changes during installation.
# Skip SMS setup on upgrades, keeping the user's existing default app choice.
previous_module=/data/adb/modules/oppo_messages_enabler
if [ "$MODPATH" != "$previous_module" ] && [ -f "$previous_module/module.prop" ]; then
  touch "$MODPATH/sms-role-configured" || abort "Cannot preserve SMS setup state"
fi

ui_print "- Cài đặt hoàn tất!"
ui_print "- Vui lòng khởi động lại điện thoại để áp dụng."
