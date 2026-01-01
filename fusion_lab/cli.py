diff --git a/fusion_lab/cli.py b/fusion_lab/cli.py
new file mode 100644
index 0000000000000000000000000000000000000000..4aa888712d9ef385e89aa282f0f949543882ce76
--- /dev/null
+++ b/fusion_lab/cli.py
@@ -0,0 +1,77 @@
+from __future__ import annotations
+
+import argparse
+import csv
+from pathlib import Path
+
+from fusion_lab.collectors import SourceConfig, collect_sources
+from fusion_lab.fusion import fuse_signals
+from fusion_lab.indicators import score_indicators
+from fusion_lab.reporting import build_brief
+
+
+DEFAULT_SOURCES = [
+    SourceConfig(name="News", path_or_url="data/sample_news.json", category="protest"),
+    SourceConfig(name="Events", path_or_url="data/sample_events.json", category="violence"),
+    SourceConfig(name="Weather", path_or_url="data/sample_weather.json", category="drought"),
+    SourceConfig(name="Economy", path_or_url="data/sample_econ.json", category="inflation"),
+]
+
+
+def _write_csv(path: Path, records: list[dict[str, object]]) -> None:
+    if not records:
+        return
+    path.parent.mkdir(parents=True, exist_ok=True)
+    with path.open("w", newline="", encoding="utf-8") as handle:
+        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
+        writer.writeheader()
+        writer.writerows(records)
+
+
+def run_pipeline(output_dir: Path, sources: list[SourceConfig]) -> None:
+    records = collect_sources(sources)
+    fused = fuse_signals(records)
+    indicators = score_indicators(fused)
+
+    output_dir.mkdir(parents=True, exist_ok=True)
+    _write_csv(output_dir / "signals.csv", [record.to_row() for record in fused])
+    (output_dir / "brief.txt").write_text(build_brief(fused, indicators), encoding="utf-8")
+
+
+def build_parser() -> argparse.ArgumentParser:
+    parser = argparse.ArgumentParser(description="Run the crisis early-warning fusion lab pipeline.")
+    parser.add_argument(
+        "--output-dir",
+        default="outputs",
+        help="Directory to write fused outputs.",
+    )
+    parser.add_argument(
+        "--sources",
+        nargs="*",
+        help="Optional list of source specifiers name=path_or_url=category.",
+    )
+    return parser
+
+
+def parse_sources(source_args: list[str] | None) -> list[SourceConfig]:
+    if not source_args:
+        return DEFAULT_SOURCES
+    parsed: list[SourceConfig] = []
+    for raw in source_args:
+        try:
+            name, path_or_url, category = raw.split("=", 2)
+        except ValueError as exc:
+            raise ValueError("Source specifier must be name=path_or_url=category") from exc
+        parsed.append(SourceConfig(name=name, path_or_url=path_or_url, category=category))
+    return parsed
+
+
+def main() -> None:
+    parser = build_parser()
+    args = parser.parse_args()
+    sources = parse_sources(args.sources)
+    run_pipeline(Path(args.output_dir), sources)
+
+
+if __name__ == "__main__":
+    main()
