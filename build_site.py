#!/usr/bin/env python3
"""Rebuild Volo Spot landing page with external assets."""
import re
from pathlib import Path

SRC = Path("/Users/douglasrinckus/Downloads/volo_spot_investidores.html")
DST = Path(__file__).parent / "index.html"

html = SRC.read_text(encoding="utf-8")

html = re.sub(r"  \.gallery-item:nth-child\(\d+\) \{ width: \d+px; \}\n", "", html)
html = html.replace(
    "  .gallery-item { flex: 0 0 auto; overflow: hidden; position: relative; }",
    "  .gallery-item { flex: 0 0 auto; overflow: hidden; position: relative; width: 340px; }",
)
html = html.replace(
    "  .map-box svg { width: 100%; height: auto; display: block; }",
    "  .map-box img { width: 100%; height: auto; display: block; object-fit: cover; }",
)

GALLERY = [
    ("assets/fachada-noturna.jpg", "Fachada — Perspectiva Noturna"),
    ("assets/fachada-diurna.jpg", "Fachada — Perspectiva Diurna"),
    ("assets/studio-mobiliado.jpg", "Studio Mobiliado"),
    ("assets/studio-cozinha-integrada.jpg", "Studio — Cozinha Integrada"),
    ("assets/piscina-gourmet.jpg", "Piscina & Espaço Gourmet"),
    ("assets/academia-elevate-fitness.jpg", "Academia Elevate Fitness"),
    ("assets/rooftop-lounge.jpg", "Rooftop Lounge"),
    ("assets/salao-gourmet.jpg", "Salão Gourmet & Terraço"),
    ("assets/salao-jogos.jpg", "Salão de Jogos & Convivência"),
    ("assets/home-cinema.jpg", "Home Cinema"),
    ("assets/lobby.jpg", "Lobby"),
    ("assets/lavanderia.jpg", "Lavanderia"),
    ("assets/pet-place.jpg", "Pet Place"),
]

gallery_html = "\n".join(
    f"""    <div class="gallery-item">
      <img src="{src}" alt="{cap}" loading="lazy">
      <div class="caption">{cap}</div>
    </div>"""
    for src, cap in GALLERY
)

html = re.sub(
    r'<img class="hero-bg" src="data:image[^"]+"[^>]*>',
    '<img class="hero-bg" src="assets/fachada-noturna.jpg" alt="Volo Spot — Fachada noturna">',
    html,
    count=1,
)

html = re.sub(
    r'<img class="about-img" src="data:image[^"]+"[^>]*>',
    '<img class="about-img" src="assets/fachada-diurna.jpg" alt="Volo Spot — Fachada diurna">',
    html,
    count=1,
)

html = re.sub(
    r'<div class="gallery-scroll" id="gallery">.*?</div>\s*</div>\s*<!-- AMENITIES -->',
    f'<div class="gallery-scroll" id="gallery">\n{gallery_html}\n  </div>\n</div>\n\n<!-- AMENITIES -->',
    html,
    flags=re.DOTALL,
    count=1,
)

map_block = """<div class="map-box">
        <img src="assets/mapa-localizacao.jpg" alt="Mapa de localização — Centro de Itajaí, Volo Spot">
        <p style="font-size:9px;color:#666;padding:8px 12px 0;margin:0;">© OpenStreetMap contributors</p>
      </div>"""
html = re.sub(
    r'<div class="map-box">\s*<svg.*?</svg>\s*</div>',
    map_block,
    html,
    flags=re.DOTALL,
    count=1,
)

html = re.sub(
    r'<img class="floorplan-img" src="data:image[^"]+"[^>]*>',
    '<img class="floorplan-img" src="assets/planta-pavimento.jpg" alt="Planta do pavimento tipo — 8º andar">',
    html,
    count=1,
)
if 'class="floorplan-img"' not in html:
    html = re.sub(
        r'(<!-- FLOOR PLAN -->.*?<motion.div class="divider"></div>)'.replace("motion.", ""),
        r'\1\n  <img class="floorplan-img" src="assets/planta-pavimento.jpg" alt="Planta do pavimento tipo — 8º andar">',
        html,
        flags=re.DOTALL,
        count=1,
    )
if 'class="floorplan-img"' not in html:
    html = re.sub(
        r'(<!-- FLOOR PLAN -->.*?<div class="divider"></div>)',
        r'\1\n  <img class="floorplan-img" src="assets/planta-pavimento.jpg" alt="Planta do pavimento tipo — 8º andar">',
        html,
        flags=re.DOTALL,
        count=1,
    )

DST.write_text(html, encoding="utf-8")
print(f"Written {DST} ({DST.stat().st_size // 1024} KB)")
