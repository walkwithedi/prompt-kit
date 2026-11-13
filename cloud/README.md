# Cloud workspace setup

Install the root AGENTS.md into the workspace before the assistant starts:

```bash
kit_dir=$(mktemp -d)
git clone --depth 1 https://github.com/walkwithedi/prompt-kit.git "$kit_dir/prompt-kit"
python3 "$kit_dir/prompt-kit/cloud/setup.py" --workspace /workspace
rm -rf "$kit_dir"
```

Add these commands to the cloud environment setup or startup script. Use the
actual workspace path if it differs from /workspace. The environment must run
the script before task instructions are loaded. Configure any resume hook
separately if setup runs only when the environment is first created.

The installer preserves existing instructions and replaces only its marked
section on repeat runs. Git and Python 3.8 or newer are required. Download
failure stops installation when the setup shell uses `set -e`.

Repository descriptions and candidate READMEs are read through the authenticated
GitHub connection when a relevant task begins. This requires the connection to
be available in that task. Private repository execution additionally requires
authorized local Git access; connector access does not imply shell access.

The installer does not change platform settings, install MCP tools, or export
shell variables. Reading repository skills is separate from installing plugins.
