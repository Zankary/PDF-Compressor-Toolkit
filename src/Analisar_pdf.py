import fitz
import os
from collections import Counter

PDF = r"C:\PDF\lipe.pdf"

doc = fitz.open(PDF)

arquivo_mb = os.path.getsize(PDF) / (1024 * 1024)

print("=" * 60)
print("ANÁLISE DO PDF")
print("=" * 60)

print(f"Arquivo: {PDF}")
print(f"Tamanho: {arquivo_mb:.2f} MB")
print(f"Páginas: {len(doc)}")

imagens = {}
paginas_com_imagem = 0
paginas_sem_texto = 0

for numero_pagina, pagina in enumerate(doc, start=1):

    imagens_pagina = pagina.get_images(full=True)
    texto = pagina.get_text("text").strip()

    if imagens_pagina:
        paginas_com_imagem += 1

    if not texto:
        paginas_sem_texto += 1

    for img in imagens_pagina:
        xref = img[0]

        if xref not in imagens:
            try:
                info = doc.extract_image(xref)

                imagens[xref] = {
                    "xref": xref,
                    "ext": info["ext"],
                    "width": info["width"],
                    "height": info["height"],
                    "size": len(info["image"]),
                    "pages": 1
                }

            except Exception:
                pass

        else:
            imagens[xref]["pages"] += 1


print()
print("-" * 60)
print("RESUMO")
print("-" * 60)

print(f"Imagens diferentes: {len(imagens)}")
print(f"Páginas com imagens: {paginas_com_imagem}")
print(f"Páginas sem texto selecionável: {paginas_sem_texto}")

tamanho_imagens = sum(x["size"] for x in imagens.values())

print(f"Tamanho das imagens extraídas: {tamanho_imagens / (1024 * 1024):.2f} MB")

print()
print("-" * 60)
print("MAIORES IMAGENS")
print("-" * 60)

maiores = sorted(
    imagens.values(),
    key=lambda x: x["size"],
    reverse=True
)

for i, img in enumerate(maiores[:30], start=1):

    tamanho_mb = img["size"] / (1024 * 1024)

    print(
        f"{i:02d}. "
        f"XREF={img['xref']} | "
        f"{img['width']}x{img['height']} | "
        f"{img['ext'].upper():4} | "
        f"{tamanho_mb:8.2f} MB | "
        f"{img['pages']} página(s)"
    )

print()
print("=" * 60)

doc.close()