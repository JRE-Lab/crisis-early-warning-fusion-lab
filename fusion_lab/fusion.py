diff --git a/fusion_lab/fusion.py b/fusion_lab/fusion.py
new file mode 100644
index 0000000000000000000000000000000000000000..bc0a4ccb0c61b6b1cfa57e30d06c6c3b1d761cd1
--- /dev/null
+++ b/fusion_lab/fusion.py
@@ -0,0 +1,23 @@
+from __future__ import annotations
+
+from collections import defaultdict
+from datetime import datetime
+from typing import Iterable
+
+from fusion_lab.models import SignalRecord
+
+
+def fuse_signals(records: Iterable[SignalRecord]) -> list[SignalRecord]:
+    return sorted(records, key=lambda record: record.date, reverse=True)
+
+
+def summarize_by_location(records: Iterable[SignalRecord]) -> dict[str, dict[str, int]]:
+    summary: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
+    for record in records:
+        summary[record.location][record.category] += 1
+    return {location: dict(categories) for location, categories in summary.items()}
+
+
+def most_recent(records: Iterable[SignalRecord]) -> datetime | None:
+    dates = [record.date for record in records]
+    return max(dates) if dates else None
