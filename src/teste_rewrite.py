import pymupdf
import os

ORIGINAL = r"C:\PDF\lipe.pdf"
SAIDA = r"C:\PDF\teste_rewrite.pdf"

doc = pymupdf.open(ORIGINAL)

print("PDF aberto.")
print(f"Páginas: {len(doc)}")
print("Reescrevendo imagens...")
print()

doc.rewrite_images(
    dpi_target=75,
    dpi_threshold=100,
    quality=40,
    lossy=True,
    lossless=True,
    bitonal=True,
    color=True,
    gray=True,
)

print("Salvando...")

doc.save(
    SAIDA,
    garbage=4,
    deflate=True,
    use_objstms=True,
    compression_effort=100
)

doc.close()

tamanho = os.path.getsize(SAIDA) / (1024 * 1024)

print()
print("=" * 60)
print("CONCLUÍDO")
print(f"Arquivo: {SAIDA}")
print(f"Tamanho: {tamanho:.2f} MB")
print("=" * 60)