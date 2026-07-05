from changeintel.git_diff import parse_diff


def test_parse_modified_added_deleted_and_renamed_files() -> None:
    diff = """diff --git a/src/a.py b/src/a.py
index 111..222 100644
--- a/src/a.py
+++ b/src/a.py
@@ -2,2 +2,3 @@
diff --git a/dev/null b/src/new.py
new file mode 100644
--- /dev/null
+++ b/src/new.py
@@ -0,0 +1,4 @@
diff --git a/src/old.py b/dev/null
deleted file mode 100644
--- a/src/old.py
+++ /dev/null
@@ -1,5 +0,0 @@
diff --git a/src/name.py b/src/renamed.py
similarity index 90%
rename from src/name.py
rename to src/renamed.py
@@ -1 +1 @@
"""
    changes = parse_diff(diff)
    assert [item.change_type for item in changes] == [
        "modified",
        "added",
        "deleted",
        "renamed",
    ]
    assert changes[0].old_ranges[0].start == 2
    assert changes[0].new_ranges[0].end == 4
    assert changes[1].old_path is None
    assert changes[2].new_path is None
    assert changes[3].new_path == "src/renamed.py"
