import os
import sys
import subprocess
import shutil
import traceback
from datetime import datetime
from pathlib import Path

def is_frozen() -> bool:
    return getattr(sys, "frozen", False)

def root_dir() -> Path:
    # When frozen, the EXE directory; otherwise, script directory
    return Path(sys.executable).resolve().parent if is_frozen() else Path(__file__).resolve().parent

ROOT = root_dir()
LOG = ROOT / "runner.log"

def log(msg: str):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{stamp} {msg}"
    print(line)
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def find_system_python() -> list[str]:
    # Prefer 'py -3' on Windows, else 'python', else 'python3'
    candidates = [["py", "-3"], ["py"], ["python"], ["python3"]]
    for args in candidates:
        if shutil.which(args[0]):
            return args
    return []

def run(args: list[str], check: bool = True) -> int:
    pretty = " ".join(f'"{a}"' if " " in a else a for a in args)
    log(f"[RUN] {pretty}")
    return subprocess.run(args, check=check, shell=False).returncode

def ensure_dirs():
    for d in ("reports", "logs", "screenshots"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)

def main():
    log("=== Selenium UI Tests Runner (.exe) ===")
    ensure_dirs()

    # 1) check requirements file
    req = ROOT / "requirements.txt"
    if not req.exists():
        raise FileNotFoundError(
            f"requirements.txt not found at {req}. "
            "Keep run_tests.exe inside the project (next to requirements.txt), "
            "or copy requirements.txt beside the EXE."
        )

    # 2) resolve bootstrap Python
    if is_frozen():
        py_boot = find_system_python()
        if not py_boot:
            raise EnvironmentError(
                "Python not found on PATH. Install Python 3 from https://www.python.org/downloads/ "
                "and tick 'Add python.exe to PATH'. Alternatively, use RUNME.bat."
            )
    else:
        py_boot = [sys.executable]

    # 3) venv next to EXE/script
    venv = ROOT / ".venv"
    vpy = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    if not venv.exists():
        run(py_boot + ["-m", "venv", str(venv)])

    # 4) deps (once)
    marker = venv / ".deps_installed.ok"
    if not marker.exists():
        run([str(vpy), "-m", "pip", "install", "--upgrade", "pip"])
        run([str(vpy), "-m", "pip", "install", "-r", str(req)])
        marker.write_text("ok", encoding="utf-8")

    # 5) prompt: headless?
    headless = False
    try:
        ans = input("Run headless? [y/N]: ").strip().lower()
        headless = (ans == "y")
    except Exception:
        pass

    # 6) run tests
    report_html = ROOT / "reports" / "report.html"
    pytest_cmd = [
        str(vpy), "-m", "pytest", "-n", "auto", "--env=test",
        "--html", str(report_html), "--self-contained-html"
    ]
    if headless:
        pytest_cmd.append("--headless")

    code = run(pytest_cmd, check=False)

    # 7) open report
    if report_html.exists():
        try:
            if os.name == "nt":
                os.startfile(str(report_html))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                run(["open", str(report_html)], check=False)
            else:
                run(["xdg-open", str(report_html)], check=False)
        except Exception:
            pass

    log(f"Done. Exit code: {code}")
    sys.exit(code)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        log(f"[FATAL] {e}")
        tb = traceback.format_exc()
        try:
            with (ROOT / "runner-error.log").open("w", encoding="utf-8") as f:
                f.write(tb)
        except Exception:
            pass
        print("\nAn unrecoverable error occurred. See runner.log / runner-error.log for details.")
        input("Press Enter to close...")
        sys.exit(1)
