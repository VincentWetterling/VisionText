# VisionText Docker Setup

## Schnellstart mit Docker Compose

### Installation & Start

```bash
# Alle Services starten (mit automatischem Model-Caching)
docker-compose up -d

# Logs anschauen
docker-compose logs -f visiontext-api

# API ist dann erreichbar unter http://localhost:8000
# UI unter http://localhost:8000/ui
```

## API Testen

### 🧪 Test-Beispiele

#### Nur OCR (Tesseract)
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@bild.jpg" \
  -F 'request={"ocr_models":["tesseract"],"vision_models":[]}'
```

#### Nur OCR (EasyOCR)
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@bild.jpg" \
  -F 'request={"ocr_models":["easyocr"],"vision_models":[]}'
```

#### Nur Vision (BLIP - Bildunterschrift)
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@bild.jpg" \
  -F 'request={"ocr_models":[],"vision_models":["blip"]}'
```

#### OCR + Vision (Beides parallel! ⚡)
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@bild.jpg" \
  -F 'request={"ocr_models":["tesseract","easyocr"],"vision_models":["blip"]}'
```

#### Mehrere OCR-Modelle vergleichen (parallel)
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@bild.jpg" \
  -F 'request={"ocr_models":["tesseract","easyocr"],"vision_models":[]}'
```

#### Mit Base64-Bild
```bash
# Base64-Datei erzeugen (Linux/Mac/PowerShell)
$base64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("bild.jpg"))

curl -X POST http://localhost:8000/analyze \
  -F "base64=$base64" \
  -F 'request={"ocr_models":["tesseract"],"vision_models":["blip"]}'
```

### ⚡ Parallelverarbeitung
**JA! OCR und Vision laufen parallel!**
- Wenn Sie mehrere `ocr_models` UND `vision_models` angeben → **alles läuft gleichzeitig**
- Die Server wartet nicht, bis Tesseract fertig ist, bevor BLIP startet
- Resultat ist schneller als sequentielle Verarbeitung

Beispiel:
```json
{
  "ocr_models": ["tesseract", "easyocr"],  // Diese laufen parallel
  "vision_models": ["blip"]                  // Diese läuft auch parallel dazu
}
```

## Features

### ✅ Base64-Bild-Support
Die API akzeptiert jetzt Bilder in zwei Formaten:
- **Datei-Upload**: Klassischer multipart/form-data Upload
- **Base64**: Direkt Base64-kodierte Bilder (mit oder ohne Data-URI-Prefix)

Beispiele:
```bash
# Mit File-Upload
curl -X POST http://localhost:8000/analyze \
  -F "file=@image.jpg" \
  -F 'request={"ocr_models":["tesseract"],"vision_models":[]}'

# Mit Base64
curl -X POST http://localhost:8000/analyze \
  -F "base64=iVBORw0KGgoAAAANS..." \
  -F 'request={"ocr_models":["tesseract"],"vision_models":[]}'

# Mit Data-URI Prefix
curl -X POST http://localhost:8000/analyze \
  -F "base64=data:image/png;base64,iVBORw0KGgoAAAANS..." \
  -F 'request={"ocr_models":["tesseract"],"vision_models":[]}'
```

### 🎯 Model Caching
Modelle werden in Docker Volumes gecacht und nicht neu heruntergeladen:

```
📦 Cache-Struktur (persistent):
/app/models/
├── huggingface/         → HuggingFace Models (BLIP, etc.)
└── transformers/        → Transformers Cache
```

**Caches bleiben erhalten** auch nach `docker-compose down`!

## Development Workflow

### Code-Änderungen mit Live-Reload

Die `docker-compose.yml` mountet bereits App-Code live:
```yaml
volumes:
  - ./app:/app/app          # App-Code hot-reload
  - ./static:/app/static    # Static Files hot-reload
```

**Änderungen an Python-Code erfordern manuellen Reload:**

```bash
# Option 1: Einfach Restart (schneller)
docker-compose restart visiontext-api

# Option 2: Full Rebuild (falls Dependencies geändert wurden)
docker-compose down
docker-compose up -d --build

# Option 3: Logs follow (zum Debugging)
docker-compose logs -f visiontext-api
```

**Du brauchst NICHT:**
- ❌ `docker-compose down -v` (würde Models löschen!)
- ❌ Container manuell zu stoppen
- ❌ Volumes neu zu erstellen

### 📋 Umgebungsvariablen

In `docker-compose.yml` automatisch gesetzt:
```
HF_HUB_DISABLE_TELEMETRY=1
TRANSFORMERS_NO_ADVISORY_WARNINGS=1
HF_HOME=/app/models/huggingface
```

## Management

```bash
# Container neu starten (Caches bleiben) - für Code-Changes
docker-compose restart visiontext-api

# Volumes anschauen
docker volume ls | grep visiontext

# Nur Container stoppen (Caches bleiben)
docker-compose down

# Volles Cleanup (⚠️ löscht auch Model-Cache!)
docker-compose down -v

# Build erzwingen (nach Dockerfile-Änderungen)
docker-compose up -d --build
```

## Performance-Tipps

1. **Erste Nutzung**: Modelle werden beim ersten Request heruntergeladen (~2-5 Min)
2. **Danach**: Instant-Requests, da alle Modelle gecacht sind in Docker Volume
3. **Bei Code-Update**: Einfach `docker-compose restart` - Models bleiben
4. **Bei Dockerfile-Update**: `docker-compose up -d --build` - Models bleiben
5. **Monitoring**: `docker stats visiontext-api` um CPU/Memory zu überwachen

## UI-Tester

Öffne `http://localhost:8000/ui` im Browser zum interaktiven Testen:
- ✅ Datei-Upload oder Base64-Paste
- ✅ Modell-Auswahl (OCR + Vision)
- ✅ Vergleichsmodus für parallele Requests (zeigt alle Modelle nebeneinander)
- ✅ Live cURL-Beispiele
- ✅ JSON Response Viewer

## Coolify Deployment

### Option 1: Dockerfile (einfach)
Wenn Coolify standardmäßig Dockerfiles deployed:
```bash
# Coolify zeigt die Dockerfile.cpu automatisch
# oder spezifiziere explizit:
# Dockerfile: docker/Dockerfile.cpu
```

### Option 2: Docker Compose (recommended für VisionText)
Wenn Coolify docker-compose unterstützt:

1. **Git-Repo mit docker-compose.yml pushen**
2. **In Coolify:**
   - Service Type: `Docker Compose`
   - Compose File: `docker-compose.yml`
   - Build Context: `.`
3. **Umgebungsvariablen in Coolify setzen:**
   ```
   HF_HUB_DISABLE_TELEMETRY=1
   TRANSFORMERS_NO_ADVISORY_WARNINGS=1
   HF_HOME=/app/models/huggingface
   ```

**Vorteil:** Model-Cache bleibt in Volume persistent erhalten auch nach Redeploy!

### Troubleshooting

```bash
# Container-Logs
docker-compose logs -f visiontext-api

# Shell in Container
docker-compose exec visiontext-api bash

# Memory-Limit (falls needed)
# In docker-compose.yml unter 'visiontext':
#   deploy:
#     resources:
#       limits:
#         memory: 4G
```

# Shell in Container
docker-compose exec visiontext bash

# Cache löschen (nur falls nötig)
docker volume rm visiontext_huggingface_cache

# Memory-Limit setzen (bei limited Resources)
# In docker-compose.yml unter 'visiontext':
#   mem_limit: 4g
#   memswap_limit: 4g
```
