diff --git a/fusion_lab/models.py b/fusion_lab/models.py
new file mode 100644
index 0000000000000000000000000000000000000000..ebdc7a41d5363853748c9c0c67e4f6f8be19c725
--- /dev/null
+++ b/fusion_lab/models.py
@@ -0,0 +1,34 @@
+from __future__ import annotations
+
+from dataclasses import dataclass, field
+from datetime import datetime
+from typing import Any
+
+
+@dataclass(frozen=True)
+class SignalRecord:
+    source: str
+    category: str
+    location: str
+    date: datetime
+    severity: int
+    summary: str
+    metrics: dict[str, Any] = field(default_factory=dict)
+
+    def to_row(self) -> dict[str, Any]:
+        return {
+            "source": self.source,
+            "category": self.category,
+            "location": self.location,
+            "date": self.date.isoformat(),
+            "severity": self.severity,
+            "summary": self.summary,
+            "metrics": self.metrics,
+        }
+
+
+@dataclass(frozen=True)
+class IndicatorScore:
+    indicator: str
+    score: float
+    rationale: str
