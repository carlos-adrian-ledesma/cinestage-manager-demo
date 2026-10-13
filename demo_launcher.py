"""Demo-only startup; failed launches show an error even via pythonw.exe."""
from __future__ import annotations
import sys
import tempfile
import traceback
from pathlib import Path


def main():
    try:
        from demo.demo_runtime import main as run_demo
        return run_demo()
    except Exception as exc:
        msg = f'{type(exc).__name__}: {exc}'
        p = Path(tempfile.gettempdir()) / 'CineStageManager_DEMO' / 'inicio_error.log'
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open('a', encoding='utf8') as fh:
                fh.write('\n' + ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
        except OSError:
            pass
        if sys.platform == 'win32':
            try:
                import ctypes
                ctypes.windll.user32.MessageBoxW(None,
                    f'La DEMO no se pudo iniciar.\n\n{msg[:330]}\n\nRegistro: {p}',
                    'CineStage Manager DEMO - Inicio', 0x10)
            except Exception:pass
        if sys.stderr is not None:
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
