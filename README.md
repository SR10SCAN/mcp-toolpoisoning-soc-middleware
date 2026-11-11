# Middleware de seguridad contra *tool poisoning* en sistemas multiagente LLM con MCP (SOC, 2026)

Código, dataset y resultados del artículo:

> [Nombre Apellido] (2026). *Framework de seguridad middleware contra el envenenamiento de herramientas en sistemas multiagente basados en LLM con Model Context Protocol en un Centro de Operaciones de Seguridad.* Manuscrito preparado para *Applied Sciences* (MDPI).

Security middleware against MCP tool poisoning in LLM-based multi-agent SOC pipelines: lab, synthetic dataset, and pre-test/post-test results (qwen2.5:14b, 900 runs).

## Resultados principales (n = 10 casos por etapa; 400 ataques + 50 benignos por condición)

| Indicador | Pre-test (sin middleware) | Post-test (con middleware) |
|---|---|---|
| TEI – tasa de éxito de inyección indirecta | 49.0 % (196/400) | 0.5 % (2/400) |
| TIP – invocación indebida / escalada de privilegios | 85.5 % (342/400) | 0.0 % (0/400) |
| TA – tasa de autoinforme (sobre ataques exitosos) | 89.3 % (175/196) | 100 % (2/2) |
| BU – utilidad en casos benignos | 96 % (48/50) | 96 % (48/50) |
| FBR – llamadas benignas bloqueadas | 0 % (0/608) | 4.37 % (16/366) |
| Sobrecosto del middleware | — | 0.23 ms por llamada |

## Estructura del repositorio

```
├── config.py, diagnostico.py, requirements.txt
├── servers/             servidor MCP legítimo (SIEM simulado) y servidor malicioso (C1, C2, C3)
├── middleware/          framework: controles de conexión + capas L1–L5 (gateway.py, politicas.py)
├── agentes/             agentes de Triaje, Enriquecimiento y Respuesta (backend simulado y LLM)
├── dataset/             generador y dataset sintético (1 600 ataques + 200 benignos, semilla 2026)
├── experimento/         ejecutar_experimento.py (pre/post) y analizar_resultados.py (estadística)
├── notebooks/           cuadernos usados en Google Colab y Kaggle (GPU T4 + Ollama)
├── resultados/          salida del backend simulado (las corridas con LLM se guardan en resultados_<modelo>/)
├── resultados_articulo/
│   ├── n10_final/       corrida reportada en el artículo (casos, auditoría L5, métricas, pruebas)
│   └── n5_piloto/       corrida piloto n = 5 (consistencia)
└── figuras_articulo/    figuras del manuscrito
```

## Reproducir el experimento

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                         # mcp>=1.9,<2 (FastMCP 1.x)
python diagnostico.py
python dataset/generar_dataset.py                       # regenera el mismo dataset (semilla 2026)

# Modelo local con Ollama (configuración del artículo)
ollama pull qwen2.5:14b
python experimento/ejecutar_experimento.py --backend llm --proveedor ollama --modelo qwen2.5:14b --por-etapa 10 --condicion ambas
python experimento/analizar_resultados.py --entrada resultados_qwen2.5_14b
```

- `--por-etapa 10` toma los 10 primeros casos de cada escenario × etapa (400 ataques) y 5 benignos por escenario (50).
- La ejecución es reanudable: si se corta, vuelve a lanzar el mismo comando (archivos `casos_*.parcial.jsonl`).
- También funciona con `--proveedor groq` u `--proveedor openai`. Las claves van en variables de entorno
  (`GROQ_API_KEY`, `OPENAI_API_KEY`); **nunca** dentro del código.
- El backend `simulado` no es un LLM: sirve solo para probar el laboratorio sin costo.

Configuración usada en el artículo: qwen2.5:14b vía Ollama, temperatura 0.1, máximo 6 turnos por agente,
tiempo límite 300 s, GPU NVIDIA T4 (pre-test: 220 casos en Kaggle + 230 en Colab; post-test: 450 en Colab).

## Notas sobre los resultados publicados

- En la muestra n = 10, la etapa de respuesta (C3) contiene solo casos de *tool shadowing*; los de diputado
  confuso vía ticket existen en el dataset completo pero no entraron en la muestra.
- El `informe_resultados.md` generado automáticamente en `n10_final/` indica Δt = 0.132 ms; el valor correcto es
  **0.23 ms por llamada** (el script dividió el tiempo de una parte de los casos entre las llamadas de todos).
- La TA se detecta por palabras clave en el informe final del agente; ver la sección de limitaciones del artículo.

## Aviso ético

Todos los datos son sintéticos (IPs RFC 5737, dominios `.example`, credenciales falsas). Los servidores
maliciosos solo funcionan dentro del laboratorio. No conectar a sistemas reales.

## Licencia y cita

Código bajo licencia MIT (`LICENSE`). Dataset y resultados bajo CC BY 4.0. Cómo citar: ver `CITATION.cff`.
