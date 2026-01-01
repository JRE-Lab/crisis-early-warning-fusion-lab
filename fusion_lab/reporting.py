diff --git a/fusion_lab/reporting.py b/fusion_lab/reporting.py
new file mode 100644
index 0000000000000000000000000000000000000000..a16fd815d0d794d868888f9efae29c9232b505f3
--- /dev/null
+++ b/fusion_lab/reporting.py
@@ -0,0 +1,24 @@
+from __future__ import annotations
+
+from datetime import datetime
+from typing import Iterable
+
+from fusion_lab.fusion import summarize_by_location
+from fusion_lab.models import IndicatorScore, SignalRecord
+
+
+def build_brief(records: Iterable[SignalRecord], indicators: Iterable[IndicatorScore]) -> str:
+    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
+    location_summary = summarize_by_location(records)
+    lines = ["BLUF: Early-warning snapshot", f"Generated: {now}", ""]
+    lines.append("Key indicators:")
+    for indicator in indicators:
+        lines.append(f"- {indicator.indicator}: {indicator.score:.1f} ({indicator.rationale})")
+    lines.append("")
+    lines.append("Signals by location:")
+    for location, categories in location_summary.items():
+        category_list = ", ".join(f"{category}={count}" for category, count in categories.items())
+        lines.append(f"- {location}: {category_list}")
+    lines.append("")
+    lines.append("Analytic note: Validate signals with source vetting and triangulate with HUMINT where possible.")
+    return "\n".join(lines)
