diff --git a/fusion_lab/__init__.py b/fusion_lab/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..a38d9246954a7de7d1cd80c725c5cf228a97c069
--- /dev/null
+++ b/fusion_lab/__init__.py
@@ -0,0 +1,5 @@
+"""Crisis Early-Warning Fusion Lab package."""
+
+from fusion_lab.cli import main
+
+__all__ = ["main"]
