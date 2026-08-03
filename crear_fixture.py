import subprocess
import sys

resultado = subprocess.run(
    [
        sys.executable,
        "manage.py",
        "dumpdata",
        "--natural-foreign",
        "--natural-primary",
        "-e",
        "contenttypes",
        "-e",
        "auth.Permission",
        "--indent",
        "2",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

if resultado.returncode != 0:
    print(resultado.stderr.decode("utf-8", errors="ignore"))
else:
    with open("datos.json", "wb") as f:
        f.write(resultado.stdout)

    print("datos.json creado")