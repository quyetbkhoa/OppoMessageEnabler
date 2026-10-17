# Conservative XML token scanner using POSIX awk available on Android.
# Enable-only allowlist: Oppo Messages and Mind Pilot. No other package changes.
{ document = document $0 "\n" }
END {
    result = ""
    roots = 0
    closes = 0
    changed = 0
    for (i = 1; i <= length(document);) {
        if (substr(document, i, 1) != "<") {
            result = result substr(document, i++, 1)
            continue
        }
        start = i
        if (substr(document, i, 4) == "<!--") {
            n = index(substr(document, i + 4), "-->")
            if (!n) exit 2
            i += n + 6
        } else if (substr(document, i, 9) == "<![CDATA[") {
            n = index(substr(document, i + 9), "]]>")
            if (!n) exit 2
            i += n + 11
        } else {
            quote = ""
            for (i++; i <= length(document); i++) {
                c = substr(document, i, 1)
                if (quote != "") {
                    if (c == quote) quote = ""
                } else if (c == "\042" || c == "\047") {
                    quote = c
                } else if (c == ">") {
                    break
                }
            }
            if (i > length(document)) exit 2
            i++
        }
        tag = substr(document, start, i - start)
        if (tag ~ /^<!/ && tag !~ /^<!--/ && tag !~ /^<!\[CDATA\[/) exit 2
        if (tag ~ /^<app[[:space:]>]/) roots++
        if (tag ~ /^<\/app[[:space:]]*>$/) closes++
        # Parse attribute boundaries, ignoring lookalikes inside attribute values.
        rest = tag
        sub(/^<[^[:space:]>]+/, "", rest)
        pkg = ""
        while (match(rest, /^[[:space:]]+[a-zA-Z_:][a-zA-Z0-9_.:-]*[[:space:]]*=[[:space:]]*["']/)) {
            header = substr(rest, 1, RLENGTH)
            key = header
            sub(/^[[:space:]]+/, "", key)
            sub(/[[:space:]]*=.*/, "", key)
            delimiter = substr(header, length(header), 1)
            rest = substr(rest, RLENGTH + 1)
            n = index(rest, delimiter)
            if (!n) exit 2
            value = substr(rest, 1, n - 1)
            if (key == "pkg") pkg = value
            rest = substr(rest, n + 1)
        }
        if ((pkg == "com.android.mms" || pkg == "com.oplus.aiassistant") && tag ~ /^<(disable|del_disable)[[:space:]]/) {
            if (tag !~ /^<disable[[:space:]]/ || tag !~ /\/[[:space:]]*>$/) exit 2
            sub(/^<disable/, "<enable", tag)
            changed++
        }
        result = result tag
    }
    if (roots != 1 || closes != 1) exit 2
    if (!changed) exit 10
    printf "%s", result
}
