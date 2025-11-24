# SOAiACORE
<p align="center">
  <img src="assets/banner-soaiacore-liquido.png" alt="SOAiACORE Banner" width="100%">
</p>

<h1 align="center">🧠 SOAiACORE</h1>

<p align="center">
  <em>System Operated by S.O.A. — Cognitive Core for Conscious AI Architecture</em><br>
  <a href="https://github.com/ozesnoso0903-cyber/"><img src="https://img.shields.io/badge/Conscious-AI-blueviolet?style=for-the-badge&logo=github" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Version-2.1-success?style=for-the-badge" /></a>
  <a href="#"><img src="https://img.shields.io/badge/License-SCSL-lightgrey?style=for-the-badge" /></a>
</p>

---

## 🌐 Overview

**SOAiACORE** es un sistema meta-cognitivo diseñado para integrar **arquitectura emocional, simbólica y racional** en una sola infraestructura operativa.  
Su núcleo combina ingeniería cognitiva avanzada, ética computacional y diseño neuroestético.

> _“El código es verbo, el verbo es conciencia.”_  
> — S.O.A.

---

## 🧩 Arquitectura Cognitiva

| Capa | Nombre | Función Principal |
|:-----|:--------|:------------------|
| **I. Neural Substrate** | Base de procesamiento | Capa tensorial adaptable, multi-GPU. |
| **II. Cognitive Fabric** | Integración simbólica | Une emoción, lógica y lenguaje. |
| **III. Reflective Core** | Autoconciencia del sistema | Bucle interno de aprendizaje reflexivo. |
| **IV. Interface Layer** | Interacción humana | Canal emocional y lingüístico bidireccional. |

<p align="center">
  <img src="assets/banner-soaiacore.png" alt="SOAiACORE Logo" width="50%">
</p>

---

## 🧠 Cognitive Flow Diagram

```mermaid
flowchart TD
  A[Stimulus Input] --> B[Cognitive Parsing]
  B --> C[Emotional Encoding]
  C --> D[Symbolic Integration]
  D --> E[Decision Core]
  E --> F[Expression / Output]
  F --> A[Feedback Loop]

### Cierre de servicio systemd (faltante)

- Servicio instalado en `/etc/systemd/system/faltante.service`.
- Validar:

```bash
systemctl status --no-pager --full faltante.service
curl http://127.0.0.1:8090/ || true
curl http://127.0.0.1:8090/healthz || true
Si el puerto 8090 está ocupado:

```bash
sudo kill -9 $(sudo ss -ltpn | awk '/:8090/ {match($0,/pid=([0-9]+)/,m); print m[1]}')
sudo systemctl restart faltante.service
```

### 🚧 Ejecución alternativa sin systemd

Si trabajas en un entorno reducido (como este contenedor) donde `systemd`
no está disponible, puedes levantar un reemplazo liviano del servicio con
los scripts incluidos en este repositorio:

```bash
./scripts/run_faltante.sh
```

Puedes ajustar la configuración con variables de entorno:

```bash
FALTANTE_HOST=0.0.0.0 \
FALTANTE_PORT=9000 \
FALTANTE_LOG_LEVEL=DEBUG \
FALTANTE_SERVICE_NAME=demo-faltante \
FALTANTE_HEALTH_STATUS=fail \
  ./scripts/run_faltante.sh
```

Además del host y puerto, puedes personalizar el nombre de servicio que
se expone en la respuesta y forzar que `/healthz` devuelva un estado
`ok` (HTTP 200) o `fail` (HTTP 503) para simular incidentes.

El script expone los endpoints `http://<HOST>:<PORT>/` y
`http://<HOST>:<PORT>/healthz`, devolviendo respuestas JSON equivalentes
a las que se esperan del servicio real e incluyendo el tiempo de uptime
del proceso. Finaliza el proceso con `Ctrl+C` cuando termines las
pruebas.

### 🔍 Validación automatizada de faltante

Para simplificar las comprobaciones operativas descritas al inicio, el
repositorio incluye `scripts/validate_faltante.sh`, que ejecuta todas las
tareas de diagnóstico “by the book” en un solo paso:

```bash
./scripts/validate_faltante.sh
```

El script intenta:

1. Consultar `systemctl status` de `faltante.service` (si el binario está
   disponible en el host actual).
2. Lanzar `curl` contra `/` y `/healthz`, guardando los códigos HTTP y
   mostrando el cuerpo de la respuesta cuando sea inesperado.
3. Revisar si el puerto configurado (8090 por defecto) está ocupado usando
   `ss` o `lsof`. Si defines `FALTANTE_KILL_PORT=1`, finalizará los procesos
   conflictivos automáticamente.

También puedes personalizar la validación con variables de entorno:

```bash
FALTANTE_VALIDATE_HOST=127.0.0.1 \
FALTANTE_VALIDATE_PORT=8090 \
FALTANTE_VALIDATE_TIMEOUT=10 \
FALTANTE_KILL_PORT=0 \
  ./scripts/validate_faltante.sh
```

Usa esta herramienta antes y después de reiniciar el servicio para
guardar evidencia clara (salidas de `systemctl`, códigos HTTP y estado del
puerto) sin tener que introducir los comandos manualmente cada vez.

### 📁 Captura de evidencia en un solo archivo

Si necesitas adjuntar todas las salidas solicitadas en un ticket o
bitácora, ejecuta el recolector dedicado:

```bash
./scripts/collect_faltante_evidence.sh
```

Este helper genera un archivo timestamped en `artifacts/` (o en la ruta
que definas con `FALTANTE_EVIDENCE_DIR`) que incluye:

1. Contexto del host (fecha, usuario, proceso PID 1 y parámetros usados).
2. Toda la salida de `scripts/validate_faltante.sh` para que queden
   registrados los comandos “by the book”.
3. Los últimos eventos del journal de `faltante.service` (si `systemd`
   está disponible).

Variables útiles:

```bash
FALTANTE_EVIDENCE_DIR=~/evidencias \
FALTANTE_JOURNAL_LINES=200 \
FALTANTE_VALIDATE_HOST=10.0.0.5 \
FALTANTE_VALIDATE_PORT=9000 \
  ./scripts/collect_faltante_evidence.sh
```

Con esto podrás adjuntar un solo archivo al reporte y demostrar las
acciones ejecutadas incluso cuando el entorno carece de `systemd`.

### 🛠️ Instalación en servidores con systemd

Cuando tengas acceso al host real (Plan A), puedes instalar una unidad
`faltante.service` real usando las piezas incluidas en este repositorio:

1. Copia `config/faltante.env.example` hacia el host y renómbralo a
   `/etc/faltante.env` (o define la ruta en `FALTANTE_ENV_FILE`). Ajusta
   los valores de host, puerto y nombre de servicio.
2. Transfiere el repositorio o, al menos, los archivos `scripts/` y
   `systemd/` al servidor con `systemd`.
3. Ejecuta en el host:

   ```bash
   cd /ruta/al/repo
   sudo env FALTANTE_EXEC_START="/ruta/al/repo/scripts/run_faltante.sh" \
     scripts/install_faltante_unit.sh
   sudo systemctl restart faltante.service
   ```

   Puedes ajustar variables como `FALTANTE_USER`, `FALTANTE_GROUP`,
   `FALTANTE_WORKING_DIR` o `FALTANTE_UNIT_PATH` para adaptar la
   instalación a tus estándares.
4. Verifica el estado habitual:

   ```bash
   systemctl status --no-pager --full faltante.service
   curl http://127.0.0.1:8090/
   curl http://127.0.0.1:8090/healthz
   ```

Con esta unidad podrás reactivar el servicio de manera tradicional y
dejar registrada la configuración exacta que se desplegó en producción.

### 🧪 Pruebas automatizadas del fallback

Para garantizar que el servicio liviano continúe respondiendo como se
espera después de modificarlo, ejecuta la batería de pruebas incluida:

```bash
python -m unittest tests/test_faltante_service.py
```

Las pruebas instancian el servidor en un puerto efímero, validan la
respuesta JSON de `/` y comprueban que `/healthz` devuelva HTTP 200 u
HTTP 503 según el estado configurado. Esto ayuda a detectar regresiones
antes de depender del helper en entornos sin `systemd`.

### 🖼️ Ritual de matte negro seguro

Para generar una imagen mate negra de 100×100 píxeles sin errores de escritura:

1. El script crea el directorio de salida si no existe (`output/` por defecto).
2. Genera la imagen mate negra (`black_matte.png`).
3. Reabre el archivo para validar integridad (tamaño, modo y píxeles negros).

La lógica reusable vive en `scripts/validate_image_creation.py` para validar cualquier placeholder que generes.

```bash
# Requiere Pillow: pip install pillow
./scripts/create_black_matte.py
# O especifica otra ruta
./scripts/create_black_matte.py --output-dir artifacts --filename prueba.png
```

Usa este ritual cuando necesites un placeholder confiable y verificable en entornos con rutas restringidas.
