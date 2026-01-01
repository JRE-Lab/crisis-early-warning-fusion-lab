diff --git a/fusion_lab/indicators.py b/fusion_lab/indicators.py
new file mode 100644
index 0000000000000000000000000000000000000000..ad56ecc1c65a1fb85823b3ff06c0e8691a2ecbd6
--- /dev/null
+++ b/fusion_lab/indicators.py
@@ -0,0 +1,51 @@
+from __future__ import annotations
+
+from dataclasses import dataclass
+from typing import Iterable
+
+from fusion_lab.models import IndicatorScore, SignalRecord
+
+
+@dataclass(frozen=True)
+class Indicator:
+    name: str
+    category_weights: dict[str, float]
+    description: str
+
+    def score(self, records: Iterable[SignalRecord]) -> IndicatorScore:
+        total = 0.0
+        rationale_parts: list[str] = []
+        for record in records:
+            weight = self.category_weights.get(record.category)
+            if weight is None:
+                continue
+            contribution = weight * record.severity
+            total += contribution
+            rationale_parts.append(f"{record.category}:{record.severity}x{weight}")
+        rationale = "; ".join(rationale_parts) if rationale_parts else "no matching signals"
+        return IndicatorScore(indicator=self.name, score=total, rationale=rationale)
+
+
+def default_indicators() -> list[Indicator]:
+    return [
+        Indicator(
+            name="Civil Unrest",
+            category_weights={"protest": 2.0, "violence": 3.0, "governance": 1.5},
+            description="Escalation in demonstrations, clashes, or governance disruptions.",
+        ),
+        Indicator(
+            name="Humanitarian Stress",
+            category_weights={"drought": 2.5, "health": 2.0, "displacement": 2.0},
+            description="Indicators of population vulnerability or crisis drivers.",
+        ),
+        Indicator(
+            name="Economic Shock",
+            category_weights={"inflation": 2.5, "currency": 2.0, "employment": 1.5},
+            description="Macroeconomic pressure that could amplify instability.",
+        ),
+    ]
+
+
+def score_indicators(records: Iterable[SignalRecord]) -> list[IndicatorScore]:
+    indicators = default_indicators()
+    return [indicator.score(records) for indicator in indicators]
