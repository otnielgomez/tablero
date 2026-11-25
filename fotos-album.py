#!/usr/bin/env python3
"""Álbumes compartidos de Google Fotos para el protector de pantalla del tablero.

Uso:
  fotos-album.py                         actualiza todos los álbumes
  fotos-album.py --agregar NOMBRE LINK   agrega un álbum (link "Compartir" de Google Fotos) y lo descarga
  fotos-album.py --quitar NOMBRE         quita un álbum

Guarda la lista de álbumes en albumes.json y las fotos en fotos.json (carpeta www/tablero).
Método no oficial: lee la página pública del álbum; si Google la cambia, puede dejar de funcionar.
"""
import json, os, re, sys, time, urllib.request

BASE = "/data/data/com.termux/files/home/hass-config/www/tablero"   # misma ruta en Termux y dentro de Ubuntu
ALBUMES = os.path.join(BASE, "albumes.json")
SALIDA = os.path.join(BASE, "fotos.json")
INICIAL = [{"nombre": "Principal", "url": "https://photos.app.goo.gl/TU_ALBUM"}]
LINK_OK = re.compile(r"^https://(photos\.app\.goo\.gl|photos\.google\.com)/[A-Za-z0-9_\-/?=&.]+$")


def guardar(ruta, datos):
    tmp = ruta + ".tmp"
    with open(tmp, "w") as f:
        json.dump(datos, f, ensure_ascii=False)
    os.replace(tmp, ruta)


def leer(ruta, defecto):
    try:
        with open(ruta) as f:
            return json.load(f)
    except Exception:
        return defecto


def fotos_de(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    vistas = []
    for u in re.findall(r'\["(https://lh3\.googleusercontent\.com/pw/[A-Za-z0-9_\-]+)",\s*\d+,\s*\d+', html):
        if u not in vistas:
            vistas.append(u)
    return vistas


def actualizar(albumes):
    previo = {a["nombre"]: a.get("fotos", []) for a in leer(SALIDA, {}).get("albumes", [])}
    salida, errores = [], []
    for a in albumes:
        try:
            f = fotos_de(a["url"])
            if not f:
                raise ValueError("sin fotos")
        except Exception as e:
            f = previo.get(a["nombre"], [])          # si falla, conserva las fotos anteriores
            errores.append(f"{a['nombre']}: {e}")
        salida.append({"nombre": a["nombre"], "fotos": f})
    todas = [u for a in salida for u in a["fotos"]]
    guardar(SALIDA, {"actualizado": time.strftime("%Y-%m-%d %H:%M"), "albumes": salida, "fotos": todas, "errores": errores})
    for a in salida:
        print(f"{a['nombre']}: {len(a['fotos'])} fotos")
    for e in errores:
        print("ERROR", e)


def main():
    albumes = leer(ALBUMES, None) or INICIAL
    args = sys.argv[1:]
    if args[:1] == ["--agregar"] and len(args) == 3:
        nombre, url = args[1].strip()[:40], args[2].strip()
        if not nombre or not LINK_OK.match(url):
            sys.exit("Nombre vacío o link no válido (debe ser un link compartido de Google Fotos).")
        albumes = [a for a in albumes if a["nombre"] != nombre] + [{"nombre": nombre, "url": url}]
    elif args[:1] == ["--quitar"] and len(args) == 2:
        albumes = [a for a in albumes if a["nombre"] != args[1].strip()]
    elif args:
        sys.exit(__doc__)
    guardar(ALBUMES, albumes)
    actualizar(albumes)


if __name__ == "__main__":
    main()
