"""LLM backend for the eval suite. Zero-dependency.

Backend resolution order (override with CLAUDE_EVALS_BACKEND or --backend):
  1. api  — ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN set. Raw HTTPS to
            /v1/messages (honors ANTHROPIC_BASE_URL).
  2. cli  — a logged-in `claude` CLI on PATH (headless: claude -p).
  3. mock — CLAUDE_EVALS_MOCK_DIR set; complete(tag=...) returns the
            contents of <dir>/<tag>.txt. For plumbing tests and CI.

If none is available, LLM-backed tiers raise BackendUnavailable with
setup instructions; the static tier never needs a backend.
"""

import json
import os
import shutil
import subprocess
import urllib.request

DEFAULT_MODEL = "claude-opus-4-8"


class BackendUnavailable(RuntimeError):
    pass


def resolve_backend(explicit=None):
    b = explicit or os.environ.get("CLAUDE_EVALS_BACKEND")
    if b:
        return b
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return "api"
    if shutil.which("claude"):
        return "cli"
    if os.environ.get("CLAUDE_EVALS_MOCK_DIR"):
        return "mock"
    raise BackendUnavailable(
        "No LLM backend available. Either:\n"
        "  - export ANTHROPIC_API_KEY=... (or ANTHROPIC_AUTH_TOKEN), or\n"
        "  - install + log in the Claude Code CLI: npm i -g @anthropic-ai/claude-code"
        " && claude (then /login), or\n"
        "  - set CLAUDE_EVALS_MOCK_DIR for plumbing tests.\n"
        "The `static` tier runs without any backend.")


def complete(prompt, model=None, max_tokens=8000, backend=None, tag="response"):
    """Return the model's text completion for `prompt`."""
    b = resolve_backend(backend)
    model = model or os.environ.get("CLAUDE_EVALS_MODEL") or DEFAULT_MODEL
    if b == "api":
        return _api_complete(prompt, model, max_tokens)
    if b == "cli":
        return _cli_complete(prompt, model)
    if b == "mock":
        return _mock_complete(tag)
    raise BackendUnavailable("unknown backend %r" % b)


def _api_complete(prompt, model, max_tokens):
    import urllib.error
    base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if api_key:
        headers["x-api-key"] = api_key
    elif auth_token:
        headers["authorization"] = "Bearer " + auth_token
        headers["anthropic-beta"] = "oauth-2025-04-20"
    req = urllib.request.Request(base + "/v1/messages",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise BackendUnavailable("API request failed (%s): %s"
                                 % (e.code, e.read()[:300])) from e
    except urllib.error.URLError as e:
        raise BackendUnavailable("API unreachable: %s" % e) from e
    return "".join(b.get("text", "") for b in data.get("content", [])
                   if b.get("type") == "text")


def _cli_complete(prompt, model):
    # prompt goes via stdin: apply-tier prompts can exceed the OS argv limit
    cmd = ["claude", "-p", "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, input=prompt, capture_output=True,
                             text=True, timeout=900)
        data = json.loads(out.stdout)
    except subprocess.TimeoutExpired as e:
        raise BackendUnavailable("claude CLI timed out") from e
    except ValueError as e:
        raise BackendUnavailable("claude CLI emitted non-JSON: %r"
                                 % (out.stdout[:200] if out else "")) from e
    if out.returncode != 0:
        raise BackendUnavailable("claude CLI failed: %s" % out.stderr[:500])
    if data.get("is_error"):
        raise BackendUnavailable("claude CLI error (try /login?): %s"
                                 % str(data.get("result", ""))[:500])
    return data.get("result", "")


def _mock_complete(tag):
    d = os.environ.get("CLAUDE_EVALS_MOCK_DIR")
    if not d:
        raise BackendUnavailable("mock backend requires CLAUDE_EVALS_MOCK_DIR")
    path = os.path.join(d, tag + ".txt")
    if not os.path.isfile(path):
        raise BackendUnavailable("mock backend: %s not found" % path)
    return open(path, encoding="utf-8").read()


def extract_json(text):
    """Pull the first JSON array or object out of a model response."""
    pairs = [("[", "]"), ("{", "}")]
    # try whichever opener occurs first in the text, then the other
    pairs.sort(key=lambda p: text.find(p[0]) if p[0] in text else len(text))
    for opener, closer in pairs:
        start = text.find(opener)
        while start != -1:
            depth = 0
            in_str = False
            esc = False
            for i in range(start, len(text)):
                c = text[i]
                if esc:
                    esc = False
                    continue
                if c == "\\":
                    esc = True
                elif c == '"' and not esc:
                    in_str = not in_str
                elif not in_str:
                    if c == opener:
                        depth += 1
                    elif c == closer:
                        depth -= 1
                        if depth == 0:
                            try:
                                return json.loads(text[start:i + 1])
                            except ValueError:
                                break
            start = text.find(opener, start + 1)
    raise ValueError("no parseable JSON in model response (first 200 chars: %r)"
                     % text[:200])
