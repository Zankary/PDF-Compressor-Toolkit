import pymupdf
import os

PDF_ORIGINAL = r"C:\PDF\lipe.pdf"
PDF_TESTE = r"C:\PDF\teste_10_paginas_v2.pdf"

QUALIDADE = 40
ESCALA = 0.5

doc = pymupdf.open(PDF_ORIGINAL)

print("Testando as primeiras 10 páginas")
print(f"JPEG qualidade: {QUALIDADE}")
print(f"Escala: {ESCALA}")
print()

for numero in range(min(10, len(doc))):

    pagina = doc[numero]
    imagens = pagina.get_images(full=True)

    print(f"Página {numero + 1}")

    for img in imagens:

        xref = img[0]

        try:

            info = doc.extract_image(xref)

            largura_original = info["width"]
            altura_original = info["height"]
            tamanho_original = len(info["image"])

            pix = pymupdf.Pixmap(doc, xref)

            # Reduz a resolução pela metade
            nova_largura = max(1, int(largura_original * ESCALA))
            nova_altura = max(1, int(altura_original * ESCALA))

            pix = pymupdf.Pixmap(
                pix,
                nova_largura,
                nova_altura
            )

            if pix.alpha:
                pix = pymupdf.Pixmap(pix, 0)

            jpeg = pix.tobytes(
                "jpeg",
                jpg_quality=QUALIDADE
            )

            print(
                f"  {largura_original}x{altura_original} "
                f"({tamanho_original / 1024:.1f} KB)"
                f" -> "
                f"{nova_largura}x{nova_altura} "
                f"({len(jpeg) / 1024:.1f} KB)"
            )

            pagina.replace_image(
                xref,
                stream=jpeg
            )

            pix = None

        except Exception as e:

            print(f"  ERRO XREF {xref}: {e}")

print()
print("Salvando...")

doc.save(
    PDF_TESTE,
    garbage=4,
    deflate=True,
    clean=True
)

doc.close()

tamanho = os.path.getsize(PDF_TESTE) / (1024 * 1024)

print()
print("=" * 60)
print("TESTE CONCLUÍDO")
print(f"Tamanho: {tamanho:.2f} MB")
print("=" * 60)