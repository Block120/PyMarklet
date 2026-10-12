from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from urllib.parse import quote

PYODIDE_VERSION = "0.27.5"
PYODIDE_BASE_URL = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/"
PYODIDE_SCRIPT_URL = f"{PYODIDE_BASE_URL}pyodide.js"


# Final optimized, pre-minified JavaScript layout shell
JAVASCRIPT_TEMPLATE = r"""(() => {
const cId = "py-bookmarklet-container";
if (document.getElementById(cId)) return;
const c = document.createElement("section");
c.id = cId;
c.style.cssText = "position:fixed;top:10px;right:10px;width:400px;height:500px;z-index:2147483647;display:flex;flex-direction:column;overflow:hidden;box-sizing:border-box;border:1px solid #333;border-radius:8px;background:#1e1e1e;color:#f4f4f4;font-family:monospace;box-shadow:0 4px 15px rgba(0,0,0,.3)";
const h = document.createElement("header");
h.style.cssText = "display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:#2d2d2d;border-bottom:1px solid #333;cursor:grab;user-select:none;touch-action:none";
const s = document.createElement("span");
s.textContent = "Loading Pyodide...";
s.style.cssText = "overflow:hidden;color:#6f6;font-size:12px;font-weight:bold;text-overflow:ellipsis;white-space:nowrap";
const cb = document.createElement("button");
cb.type = "button"; cb.textContent = "×"; cb.setAttribute("aria-label", "Close");
cb.style.cssText = "margin-left:12px;border:0;background:transparent;color:#f66;cursor:pointer;font-size:20px;font-weight:bold;line-height:1";
const ct = document.createElement("div");
ct.style.cssText = "flex:1;min-height:0;display:flex;flex-direction:column;overflow:hidden";
const cv = document.createElement("canvas");
cv.id = "canvas"; cv.tabIndex = 0; cv.style.cssText = "display:block;max-width:100%;max-height:70%;margin:0 auto;background:#000;image-rendering:pixelated;outline:none";
cv.addEventListener("pointerdown", () => cv.focus());
const o = document.createElement("pre");
o.style.cssText = "flex:1;min-height:0;overflow:auto;margin:0;padding:15px;box-sizing:border-box;white-space:pre-wrap;overflow-wrap:anywhere";
h.append(s, cb); ct.append(cv, o); c.append(h, ct); document.body.appendChild(c);
const setStatus = (msg, isErr = false) => { s.textContent = msg; s.style.color = isErr ? "#f66" : "#6f6"; };
const log = (val) => { o.textContent += `${String(val)}\n`; o.scrollTop = o.scrollHeight; };
cb.addEventListener("click", () => c.remove());
let dx = 0, dy = 0;
h.addEventListener("pointerdown", (e) => {
  if (e.target === cb) return;
  const b = c.getBoundingClientRect();
  dx = e.clientX - b.left; dy = e.clientY - b.top;
  h.setPointerCapture(e.pointerId); h.style.cursor = "grabbing";
});
h.addEventListener("pointermove", (e) => {
  if (!h.hasPointerCapture(e.pointerId)) return;
  const ml = Math.max(0, window.innerWidth - c.offsetWidth);
  const mt = Math.max(0, window.innerHeight - c.offsetHeight);
  const left = Math.min(ml, Math.max(0, e.clientX - dx));
  const top = Math.min(mt, Math.max(0, e.clientY - dy));
  c.style.left = `${left}px`; c.style.top = `${top}px`; c.style.right = "auto";
});
const stop = (e) => { if (h.hasPointerCapture(e.pointerId)) h.releasePointerCapture(e.pointerId); h.style.cursor = "grab"; };
h.addEventListener("pointerup", stop); h.addEventListener("pointercancel", stop);

__DATA_SPLICING_PLACEHOLDER__

async function runPython() {
  try {
    setStatus("Starting Python...");
    const pyodide = await globalThis.loadPyodide({ indexURL: "__PYODIDE_BASE_URL__", stdout: log, stderr: log });
    pyodide._api._skip_unwind_fatal_error = true;
    pyodide.canvas.setCanvas2D(cv);
    
    setStatus("Resolving Pyodide imports...");
    await pyodide.loadPackagesFromImports(pyCode);

    const installPyPiPackages = async (packages) => {
      if (!packages.length) return;
      setStatus(`Installing PyPI packages: ${packages.join(", ")}...`);
      await pyodide.loadPackage("micropip");
      const micropip = pyodide.pyimport("micropip");
      try {
        await micropip.install(packages);
      } finally {
        micropip.destroy();
      }
    };

    // The optional first-line # PKGS: manifest specifies PyPI distribution
    // names, covering cases such as `scikit-learn` -> `sklearn`.
    await installPyPiPackages(declaredPackages);

    // Check after both resolvers so conventional import names still install
    // automatically when a script does not declare a distribution.
    const pypiPackages = packageModules.filter((moduleName) => !pyodide.runPython(
      `import importlib.util\nimportlib.util.find_spec(${JSON.stringify(moduleName)}) is not None`,
    ));
    await installPyPiPackages(pypiPackages);
    
    setStatus("Starting Python...");
    await pyodide.runPythonAsync(pyCode);
    setStatus("Execution finished.");
  } catch (err) {
    setStatus("Python execution failed.", true);
    log(err instanceof Error ? err.stack || err.message : err);
  }
}
function loadPyodideScript() {
  if (typeof globalThis.loadPyodide === "function") { void runPython(); return; }
  const scriptNode = document.createElement("script"); scriptNode.src = "__PYODIDE_SCRIPT_URL__"; scriptNode.async = true;
  scriptNode.onload = () => void runPython();
  scriptNode.onerror = () => setStatus("Could not load Pyodide (possibly blocked by CSP).", true);
  document.body.appendChild(scriptNode);
}
loadPyodideScript();
})();"""

def clean_python_code(code: str) -> str:
    """Preserve the user's program exactly; JSON encoding handles URL embedding."""
    return code

def declared_pypi_packages(python_code: str) -> list[str]:
    """Read comma-separated PyPI requirements from a first-line # PKGS: header."""
    first_line = python_code.split("\n", 1)[0].lstrip("\ufeff")
    match = re.fullmatch(r"\s*#\s*PKGS\s*:\s*(.*)\s*", first_line, flags=re.IGNORECASE)
    if not match or not match.group(1):
        return []

    packages = [package.strip() for package in match.group(1).split(",")]
    return list(dict.fromkeys(package for package in packages if package))


def imported_package_modules(python_code: str) -> list[str]:
    """Return third-party top-level modules imported by *python_code*."""
    try:
        tree = ast.parse(python_code)
    except SyntaxError:
        # Let Pyodide report the original syntax error when the bookmarklet runs.
        return []

    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported_modules.append(node.module.split(".", 1)[0])

    return list(dict.fromkeys(imported_modules))


def build_bookmarklet(python_code: str) -> str:
    cleaned_py = clean_python_code(python_code)
    package_modules = imported_package_modules(cleaned_py)
    declared_packages = declared_pypi_packages(cleaned_py)

    # Inject variables securely as valid JS.
    js_variables = (
        f"const pyCode = {json.dumps(cleaned_py)};\n"
        f"const declaredPackages = {json.dumps(declared_packages)};\n"
        f"const packageModules = {json.dumps(package_modules)};"
    )

    payload = JAVASCRIPT_TEMPLATE.replace('__DATA_SPLICING_PLACEHOLDER__', js_variables)
    payload = payload.replace("__PYODIDE_BASE_URL__", PYODIDE_BASE_URL)
    payload = payload.replace("__PYODIDE_SCRIPT_URL__", PYODIDE_SCRIPT_URL)

    # Keep line breaks: collapsing them can make a `//` comment consume the
    # remaining JavaScript. `quote` encodes them safely for a bookmarklet URL.
    return f"javascript:{quote(payload, safe='')}"

def generate_bookmarklet(python_file_path: Path, output_path: Path) -> bool:
    """Generate a bookmarklet from *python_file_path* and write it to *output_path*."""
    try:
        python_code = python_file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Error reading {python_file_path}: {error}")
        return False

    bookmarklet = build_bookmarklet(python_code)
    try:
        output_path.write_text(bookmarklet, encoding="utf-8")
    except OSError as error:
        print(f"Error writing {output_path}: {error}")
        return False

    print(f"Bookmarklet written to {output_path} ({len(bookmarklet)} characters).")
    return True
