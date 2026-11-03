#!/usr/bin/env python3
"""Tests for .github/scripts/release_skills.sh and scripts/versions.py.

Each test builds a throw-away git repository with skills and tags and runs the release script
with DRY_RUN=1. Run: python3 -m unittest discover -s tests
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = "# {name}\n\nAbout.\n\n## Version notes\n\n{entries}\n"
ZH = "# {name}\n\n说明。\n\n## 版本说明\n\n{entries}\n"


def entries_en(versions):
    return "\n".join("- v%s (2026-11-0%d): Change." % (v, i + 1) for i, v in enumerate(versions))


def entries_zh(versions):
    return "\n".join("- v%s（2026-11-0%d）：改动。" % (v, i + 1) for i, v in enumerate(versions))


@unittest.skipIf(os.name == "nt" or not shutil.which("bash") or not shutil.which("unzip"),
                 "needs bash and unzip")
class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="prompt-kit-release-test-")
        self.addCleanup(shutil.rmtree, self.repo, True)
        for rel in (".github/scripts/release_skills.sh", "scripts/versions.py", "scripts/build_skill.py"):
            os.makedirs(os.path.dirname(os.path.join(self.repo, rel)), exist_ok=True)
            shutil.copy(os.path.join(ROOT, rel), os.path.join(self.repo, rel))
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "tag.gpgsign", "false")
        self.write("LICENSE", "MIT\n")
        self.kit("1.0")
        self.skill("alpha", "1.0")

    # ---------- helpers ----------

    def git(self, *args):
        p = subprocess.run(("git",) + args, cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout.strip()

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def readmes(self, base, name, en, zh=None, extra=""):
        self.write(base + "README.md", EN.format(name=name, entries=entries_en(en)) + extra)
        self.write(base + "README.zh-CN.md", ZH.format(name=name, entries=entries_zh(zh or en)) + extra)

    def kit(self, *versions, extra=""):
        self.readmes("", "prompt-kit", versions, extra=extra)

    def skill(self, name, *versions, prompt="规则一。", extra=""):
        base = "skills/%s/" % name
        self.write(base + "SKILL.md", "---\nname: %s\ndescription: Test.\n---\n\n%s\n" % (name, prompt))
        self.write(base + "prompt.md", "适用场景：测试\n\n```text\n%s\n```\n" % prompt)
        self.readmes(base, name, versions, extra=extra)

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "change")

    def release(self, *skills):
        env = dict(os.environ, DRY_RUN="1", OUT_DIR=os.path.join(self.repo, ".out"), FORCE="0")
        env.pop("GITHUB_REPOSITORY", None)
        p = subprocess.run(["bash", ".github/scripts/release_skills.sh"] + list(skills), cwd=self.repo,
                           capture_output=True, text=True, env=env)
        return p.returncode, p.stderr

    def check(self):
        p = subprocess.run([sys.executable, "scripts/versions.py", "check"], cwd=self.repo,
                           capture_output=True, text=True)
        return p.returncode, p.stderr

    # ---------- cases ----------

    def test_first_release(self):
        self.commit()
        rc, err = self.release()
        self.assertEqual(rc, 0, err)
        self.assertIn("alpha: last=none new=alpha-v1.0.0", err)
        self.assertIn("prompt-kit: last=none new=prompt-kit-v1.0.0", err)
        self.assertTrue(os.path.isfile(os.path.join(self.repo, ".out", "alpha-v1.0.0.zip")))

    def test_version_bump_releases_dot_0(self):
        self.commit()
        self.git("tag", "alpha-v1.0.0")
        self.git("tag", "alpha-v1.0.1")
        self.git("tag", "prompt-kit-v1.0.0")
        self.skill("alpha", "1.0", "1.1", prompt="规则二。")
        self.kit("1.0", "1.1")
        self.commit()
        rc, err = self.release()
        self.assertEqual(rc, 0, err)
        self.assertIn("alpha: last=alpha-v1.0.1 new=alpha-v1.1.0", err)
        self.assertIn("prompt-kit: last=prompt-kit-v1.0.0 new=prompt-kit-v1.1.0", err)

    def test_readme_only_change_releases_z_plus_1(self):
        self.commit()
        self.git("tag", "alpha-v1.0.0")
        self.git("tag", "prompt-kit-v1.0.0")
        self.skill("alpha", "1.0", extra="\nMore words.\n")
        self.commit()
        rc, err = self.release()
        self.assertEqual(rc, 0, err)
        self.assertIn("new=alpha-v1.0.1", err)
        self.assertIn("new=prompt-kit-v1.0.1", err)   # skills/ README changes count as README-only for the kit too

    def test_prompt_change_without_bump_fails(self):
        self.commit()
        self.git("tag", "alpha-v1.0.0")
        self.git("tag", "prompt-kit-v1.0.0")
        self.skill("alpha", "1.0", prompt="规则改了。")
        self.commit()
        rc, err = self.release()
        self.assertEqual(rc, 1)
        self.assertIn("::error::alpha: skills/alpha/SKILL.md, skills/alpha/prompt.md changed since alpha-v1.0.0", err)
        self.assertIn("::error::prompt-kit:", err)
        self.assertNotIn("new=alpha-", err)
        rc, err = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("raise X.Y", err)

    def test_mixed_tags_find_previous_release_by_commit_order(self):
        self.commit()
        self.git("tag", "alpha-v2026.10.16")
        self.skill("alpha", "1.0", extra="\nMore.\n")
        self.commit()
        self.git("tag", "alpha-v1.0.0")
        self.skill("alpha", "1.0", extra="\nMore again.\n")
        self.commit()
        rc, err = self.release("alpha")
        self.assertEqual(rc, 0, err)
        self.assertIn("alpha: last=alpha-v1.0.0 new=alpha-v1.0.1", err)
        self.assertIn("prompt-kit: skills given, skipped", err)

    def test_date_and_new_tag_on_one_commit_prefers_new(self):
        self.commit()
        self.git("tag", "alpha-v2026.11.01")
        self.git("tag", "alpha-v1.0.0")
        self.skill("alpha", "1.0", extra="\nMore.\n")
        self.commit()
        rc, err = self.release("alpha")
        self.assertIn("last=alpha-v1.0.0 new=alpha-v1.0.1", err)

    def test_after_date_tag_first_release_is_dot_0(self):
        self.commit()
        self.git("tag", "alpha-v2026.10.16")
        self.git("tag", "prompt-kit-v2026.10.16.2")
        self.skill("alpha", "1.0", prompt="规则改了。")
        self.commit()
        rc, err = self.release()
        self.assertEqual(rc, 0, err)
        self.assertIn("alpha: last=alpha-v2026.10.16 new=alpha-v1.0.0", err)
        self.assertIn("prompt-kit: last=prompt-kit-v2026.10.16.2 new=prompt-kit-v1.0.0", err)

    def test_unchanged_skill_is_skipped(self):
        self.commit()
        self.git("tag", "alpha-v1.0.0")
        self.git("tag", "prompt-kit-v1.0.0")
        rc, err = self.release()
        self.assertEqual(rc, 0, err)
        self.assertIn("alpha: unchanged since alpha-v1.0.0, skipped", err)
        self.assertIn("prompt-kit: unchanged since prompt-kit-v1.0.0, skipped", err)

    def test_readme_version_mismatch_fails(self):
        self.write("skills/alpha/README.zh-CN.md", ZH.format(name="alpha", entries=entries_zh(["1.0", "1.1"])))
        self.commit()
        rc, err = self.release()
        self.assertEqual(rc, 1)
        self.assertIn("alpha: README.md names v1.0 but README.zh-CN.md names v1.1", err)
        rc, err = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("names v1.0 but README.zh-CN.md names v1.1", err)

    def test_missing_or_three_part_version_notes_fail(self):
        self.write("skills/alpha/README.md", "# alpha\n\n## Version notes\n\n- First open-source release.\n")
        self.write("README.zh-CN.md", ZH.format(name="kit", entries="- v1.0.1（2026-11-01）：三段。"))
        self.commit()
        rc, err = self.check()
        self.assertEqual(rc, 1)
        self.assertIn('skills/alpha/README.md: no "## Version notes" entry', err)
        self.assertIn("README.zh-CN.md: version note", err)

    def test_check_counts_uncommitted_changes(self):
        self.commit()
        self.git("tag", "alpha-v1.0.0")
        self.git("tag", "prompt-kit-v1.0.0")
        self.assertEqual(self.check()[0], 0)
        self.write("skills/alpha/prompt.md", "适用场景：测试\n\n```text\n新规则。\n```\n")
        rc, err = self.check()
        self.assertEqual(rc, 1)
        self.skill("alpha", "1.0", "1.1", prompt="新规则。")
        self.kit("1.0", "1.1")
        rc, err = self.check()
        self.assertEqual(rc, 0, err)


if __name__ == "__main__":
    unittest.main()
