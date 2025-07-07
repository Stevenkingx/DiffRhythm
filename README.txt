Nombre del proyecto: DiffRhythm-Docker
Uso: Backend Flask con DiffRhythm funcionando en GPU para generar música vocal AI

📦 Contenido del paquete:

DiffRhythm-Docker/
├── app.py                  ← API Flask principal
├── Dockerfile              ← Clona DiffRhythm de GitHub
├── requirements.txt        ← Dependencias PyPI mínimas
├── runpod_docker_start.sh  ← Script opcional de arranque
└── templates/
    └── index.html          ← Interfaz web de prueba

🚀 Instrucciones para RunPod

1. Ve a: https://runpod.io/console
2. Crea un nuevo "Custom Image GPU Pod"
3. Sube el .zip del proyecto (DiffRhythm-Docker.zip)
4. Configura:
   - Container Port: 8080
   - Command: python3 app.py
     (o ./runpod_docker_start.sh si quieres usar el script)
5. Espera 2–3 minutos. Cuando esté listo, abre el puerto público 8080.

🔍 Para probar la API

Abre tu navegador en:

http://<public-ip>:8080/

O prueba con curl:

curl -X POST http://<public-ip>:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "demo",
    "use_example_lrc": true,
    "genre": "hip hop",
    "style": "energetic male vocal",
    "instruments": "808s"
  }'
