SKIPUNZIP=0

ui_print "************************************"
ui_print "       Oppo Messages Enabler        "
ui_print "           by quyetbkhoa            "
ui_print "************************************"
ui_print "- Đang cài đặt Oppo Messages Enabler v1.0.1..."
ui_print "- Thiết lập quyền và cấu hình..."

set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755

# Clear package cache so system cleanly reloads Oppo Messages
rm -rf /data/system/package_cache/*

ui_print "- Cài đặt hoàn tất!"
ui_print "- Vui lòng khởi động lại điện thoại để áp dụng."
