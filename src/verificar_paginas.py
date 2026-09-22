import pymupdf

PDF = r"C:\PDF\lipe.pdf"

doc = pymupdf.open(PDF)

print("=" * 70)
print("VERIFICANDO POSIÇÃO DAS IMAGENS")
print("=" * 70)

for numero in range(min(20, len(doc))):

    pagina = doc[numero]

    largura = pagina.rect.width
    altura = pagina.rect.height

    imagens = pagina.get_images(full=True)

    print()
    print(f"PÁGINA {numero + 1}")
    print(f"Tamanho da página: {largura:.1f} x {altura:.1f}")
    print(f"Imagens: {len(imagens)}")

    for img in imagens:

        xref = img[0]

        rects = pagina.get_image_rects(xref)

        for rect in rects:

            cobre_largura = rect.width / largura * 100
            cobre_altura = rect.height / altura * 100

            print(
                f"  XREF {xref}: "
                f"{rect.width:.1f} x {rect.height:.1f} "
                f"({cobre_largura:.1f}% largura, "
                f"{cobre_altura:.1f}% altura)"
            )

doc.close()