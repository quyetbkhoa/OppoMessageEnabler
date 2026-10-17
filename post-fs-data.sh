#!/system/bin/sh
MODDIR="${0%/*}"

umask 077
WORK="$MODDIR/generated"
mkdir -p "$WORK" || exit 1
exec 2>"$WORK/boot.log"

# Derive each overlay from THAT partition's current ROM, including after OTA.
# Never overlay feature_rsa: the SMS role is assigned after boot.
for partition in my_stock my_product my_heytap odm; do
    target="/$partition/etc/config/app_v2.xml"
    [ -f "$target" ] || continue
    output="$WORK/$partition-app_v2.xml"
    if awk -f "$MODDIR/patch-app-config.awk" "$target" > "$output.tmp"; then
        chmod 0644 "$output.tmp" || continue
        context="$(ls -Zd "$target" | awk '{print $1}')"
        [ -n "$context" ] && chcon "$context" "$output.tmp" || {
            echo "Cannot preserve SELinux context: $target" >&2
            continue
        }
        mv -f "$output.tmp" "$output" || continue
        mount --bind "$output" "$target" || echo "Bind failed: $target" >&2
    else
        # Unchanged or unsupported XML must never be mounted.
        rm -f "$output.tmp"
    fi
done
