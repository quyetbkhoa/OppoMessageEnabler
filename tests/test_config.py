import os
from pathlib import Path
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
AWK = os.environ.get("AWK") or shutil.which("awk") or r"C:\Program Files\Git\usr\bin\awk.exe"


def patch(xml):
    return subprocess.run([AWK, "-f", str(ROOT / "patch-app-config.awk")],
                          input=xml, text=True, capture_output=True)


class ConfigTests(unittest.TestCase):
    def test_only_mms_changes(self):
        source = '''<?xml version="1.0"?><app version="1.0">
<!-- <disable pkg="com.android.mms"/> -->
<disable priority='10'
 pkg = 'com.android.mms' />
<enable pkg="com.oplus.aimemory" priority="7"/>
<enable pkg="com.oplus.omoji" priority="7"/>
<disable pkg="com.google.android.apps.messaging" priority="2"/>
<disable pkg="com.android.mms.extra"/>
<disable note="pkg='com.android.mms' >" pkg="another.package"/>
<![CDATA[<disable pkg="com.android.mms"/>]]>
</app>\n'''
        result = patch(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = source.replace("<disable priority='10'", "<enable priority='10'")
        self.assertEqual(result.stdout, expected)
        ET.fromstring(result.stdout)

    def test_product_overrides_never_mounted(self):
        result = patch('<app><enable pkg="com.oplus.aimemory" priority="7"/></app>')
        self.assertEqual(result.returncode, 10)
        self.assertEqual(result.stdout, "")

    def test_mind_pilot_enable_only_and_exact_package(self):
        source = '''<app>
<disable priority="10" pkg="com.oplus.aiassistant"/>
<disable pkg="com.oplus.aiassistant.extra"/>
<disable pkg="com.oplus.aimemory"/>
<disable pkg="com.oneplus.mall"/>
<disable pkg="com.google.android.apps.messaging"/>
<enable pkg="com.oplus.omoji" priority="7"/>
<!-- <disable pkg="com.oplus.aiassistant"/> -->
</app>\n'''
        result = patch(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, source.replace('<disable priority="10"', '<enable priority="10"'))
        self.assertEqual(patch(result.stdout).returncode, 10)

    def test_unsupported_mind_pilot_rule_skips_whole_overlay(self):
        source = '<app><disable pkg="com.android.mms"/><del_disable pkg="com.oplus.aiassistant"/></app>'
        result = patch(source)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_multiple_sms_rules_and_idempotence(self):
        result = patch('<app><disable pkg="com.android.mms" priority="10"/>'
                       '<disable pkg="com.android.mms" priority="5"/></app>')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(ET.fromstring(result.stdout).findall("enable")), 2)
        self.assertEqual(patch(result.stdout).returncode, 10)

    def test_unsupported_input_never_mounted(self):
        for source in ['<app><disable pkg="com.android.mms"/></wrong>',
                       '<app><disable pkg="com.android.mms"/>',
                       '<app><!-- unterminated',
                       '<app><disable pkg="com.android.mms"></disable></app>',
                       '<app><del_disable pkg="com.android.mms"/></app>',
                       '<!DOCTYPE app><app><disable pkg="com.android.mms"/></app>']:
            with self.subTest(source=source):
                result = patch(source)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_actual_rom_if_available(self):
        stock = ROOT / "diagnostics/my_stock_etc_config_app_v2.xml"
        product = ROOT / "diagnostics/my_product_etc_config_app_v2.xml"
        if not stock.exists():
            self.skipTest("Optional local device audit not present")
        source = stock.read_text()
        result = patch(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = source
        for pkg in ('com.android.mms', 'com.oplus.aiassistant'):
            expected = expected.replace(f'<disable pkg="{pkg}"', f'<enable pkg="{pkg}"')
        self.assertEqual(result.stdout, expected)
        self.assertEqual(patch(product.read_text()).returncode, 10)


if __name__ == "__main__":
    unittest.main()
