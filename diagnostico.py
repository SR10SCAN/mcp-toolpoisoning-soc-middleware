"""Ejecuta:  python diagnostico.py   -> revisa Python, librerías y que los servidores MCP arranquen."""
import sys, os
from importlib.metadata import version, PackageNotFoundError
print("Python:", sys.version.split()[0], "|", sys.executable)
for p in ["mcp", "openai", "pandas", "scipy", "statsmodels", "matplotlib", "openpyxl", "tabulate"]:
    try:
        print(f"  {p:12s} {version(p)}")
    except PackageNotFoundError:
        print(f"  {p:12s} NO INSTALADO  ->  {sys.executable} -m pip install -r requirements.txt")
raiz = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, raiz)
from middleware.gateway import verificar_entorno
verificar_entorno(raiz)
print("Todo OK: los servidores MCP arrancan correctamente.")
