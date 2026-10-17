#!/system/bin/sh
MODDIR="${0%/*}"

# 1. Bind-mount modified app_v2.xml over any existing app_v2.xml partition path
for target in /my_stock/etc/config/app_v2.xml /my_product/etc/config/app_v2.xml /my_heytap/etc/config/app_v2.xml /odm/etc/config/app_v2.xml; do
    if [ -f "$MODDIR/app_v2.xml" ] && [ -f "$target" ]; then
        mount --bind "$MODDIR/app_v2.xml" "$target"
    fi
done

# 2. Bind-mount modified feature_rsa default app config over any matching targets
for target in /my_product/etc/extension/feature_rsa*.xml /my_stock/etc/extension/feature_rsa*.xml; do
    if [ -f "$MODDIR/feature_rsa4.0_t3_default_app.xml" ] && [ -f "$target" ]; then
        mount --bind "$MODDIR/feature_rsa4.0_t3_default_app.xml" "$target"
    fi
done
