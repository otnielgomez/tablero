# Tablero de la casa

Tablero para un iPad de pared conectado a Home Assistant: clima, calidad del aire, pronóstico,
luces, Geely EX5 EM-i, TV, familia, agenda, música (Music Assistant), red, pendientes,
timbre Nest y protector de pantalla con álbumes de Google Fotos.

**No contiene datos privados**: el token de Home Assistant, la llave de TomTom, las rutas
y la ubicación de casa se capturan en Ajustes (mantener presionado el reloj) y se guardan
solo en cada navegador.

## Archivos
- `index.html` – el tablero (se sirve desde `hass-config/www/tablero/`).
- `icono.png` – ícono para "Agregar a pantalla de inicio".
- `fotos-album.py` – lee álbumes compartidos de Google Fotos para el protector.
- `shell-albumes.yaml` – comandos de Home Assistant para administrar álbumes.
- `alertas-*.yaml` – automatizaciones de avisos (Geely, timbre, lavandería).

`geely360.webp` (fotos de la camioneta) no se incluye en el repositorio.
