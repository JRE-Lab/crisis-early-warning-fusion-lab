diff --git a/fusion_lab/collectors.py b/fusion_lab/collectors.py
new file mode 100644
index 0000000000000000000000000000000000000000..1fe6d4d5a2ed29d8f64fba0fec95ae5917ad3e17
--- /dev/null
+++ b/fusion_lab/collectors.py
@@ -0,0 +1,47 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from datetime import datetime
+from pathlib import Path
+from typing import Any, Iterable
+from urllib.request import urlopen
+
+from fusion_lab.models import SignalRecord
+
+
+@dataclass(frozen=True)
+class SourceConfig:
+    name: str
+    path_or_url: str
+    category: str
+
+
+def _read_json(path_or_url: str) -> Any:
+    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
+        with urlopen(path_or_url) as response:
+            return json.loads(response.read().decode("utf-8"))
+    return json.loads(Path(path_or_url).read_text(encoding="utf-8"))
+
+
+def _parse_date(value: str) -> datetime:
+    return datetime.fromisoformat(value.replace("Z", "+00:00"))
+
+
+def collect_sources(sources: Iterable[SourceConfig]) -> list[SignalRecord]:
+    records: list[SignalRecord] = []
+    for source in sources:
+        payload = _read_json(source.path_or_url)
+        for item in payload:
+            records.append(
+                SignalRecord(
+                    source=source.name,
+                    category=source.category,
+                    location=item["location"],
+                    date=_parse_date(item["date"]),
+                    severity=int(item.get("severity", 1)),
+                    summary=item["summary"],
+                    metrics={key: value for key, value in item.items() if key not in {"location", "date", "summary", "severity"}},
+                )
+            )
+    return records
