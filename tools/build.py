"""Build a root-manager ZIP with LF scripts and Unix permissions on all hosts."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ["customize.sh", "post-fs-data.sh", "service.sh", "module.prop", "patch-app-config.awk",
         "META-INF/com/google/android/update-binary", "META-INF/com/google/android/updater-script"]
VERSION = next(line.split('=', 1)[1] for line in (ROOT / 'module.prop').read_text().splitlines()
               if line.startswith('version='))
OUTPUT = ROOT / f"Oppo_Messages_Enabler_{VERSION}.zip"
with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for name in FILES:
        info = zipfile.ZipInfo(name)
        info.create_system = 3
        executable = name.endswith(".sh") or name.endswith("update-binary")
        info.external_attr = (0o100755 if executable else 0o100644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, (ROOT / name).read_bytes().replace(b"\r\n", b"\n"))
print(OUTPUT)
checksum = OUTPUT.with_suffix(OUTPUT.suffix + '.sha256')
checksum.write_text(f'{hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}  {OUTPUT.name}\n', encoding='ascii', newline='\n')
print(checksum)
