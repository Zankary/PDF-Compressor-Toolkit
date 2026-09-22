import pymupdf
import os

ORIGINAL = r"C:\PDF\lipe.pdf"
SAIDA = r"C:\PDF\lipe_30mb.pdf"

doc = pymupdf.open(ORIGINAL)

print("PDF aberto.")
print(f"Páginas: {len(doc)}")
print("Reprocessando TODAS as imagens...")
print("Configuração: 50 DPI / qualidade JPEG 25")
print()

doc.rewrite_images(
    dpi_target=50,
    dpi_threshold=51,
    quality=25,
    lossy=True,
    lossless=True,
    bitonal=True,
    color=True,
    gray=True,
)

print("Imagens processadas.")
print("Salvando PDF...")
print()

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