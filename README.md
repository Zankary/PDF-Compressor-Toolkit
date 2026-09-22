# 📄 PDF Compressor Toolkit

> Conjunto de scripts em Python para **analisar, inspecionar e otimizar arquivos PDF**, com foco em identificar imagens pesadas e reduzir o tamanho final do arquivo.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.24%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🎯 Objetivo

PDFs digitalizados (scans, livros, apostilas) costumam ser **enormes** porque armazenam imagens em altíssima resolução. Este projeto reúne um conjunto de scripts para:

- 🔍 **Verificar** o posicionamento e a cobertura das imagens em cada página;
- 📊 **Analisar** quantas imagens existem, quais são as maiores e quanto ocupam;
- 🧪 **Testar** reduções de qualidade (JPEG, escala, DPI) em amostras;
- ⚙️ **Reescrever** imagens do PDF inteiro com `rewrite_images()`, reduzindo DPI e qualidade JPEG.

O foco é **diagnóstico técnico**: entender *por que* o PDF é grande antes de aplicar qualquer compressão.

---

## 🗂️ Estrutura do projeto

```
.
├── verificar_paginas.py    # Inspeciona posição/tamanho das imagens por página
├── analisar_pdf.py         # Relatório geral: imagens, páginas, maiores arquivos
├── teste_imagens.py        # Testa redução em 10 páginas (escala + JPEG)
├── teste_rewrite.py        # rewrite_images() com DPI 75 / qualidade 40
├── teste_rewrite2.py       # rewrite_images() agressivo: 50 DPI / qualidade 25
└── requirements.txt
```

---

## 🔧 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/pdf-compressor-toolkit.git
cd pdf-compressor-toolkit

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## 🚀 Como usar

Antes de rodar, **edite a variável `PDF`** (ou `ORIGINAL`) no topo de cada script apontando para o seu arquivo.

### 1️⃣ `verificar_paginas.py` — Diagnóstico de layout

Mostra, para as **20 primeiras páginas**, o tamanho da página e quanto cada imagem ocupa (em % de largura e altura).

```bash
python verificar_paginas.py
```

**Saída esperada:**
```
PÁGINA 1
Tamanho da página: 595.0 x 842.0
Imagens: 1
  XREF 12: 595.0 x 842.0 (100.0% largura, 100.0% altura)
```

---

### 2️⃣ `analisar_pdf.py` — Relatório completo

Gera um resumo com:
- Tamanho do arquivo e número de páginas;
- Quantidade de imagens **únicas**;
- Páginas com imagem / sem texto selecionável;
- **Top 30 maiores imagens** (XREF, resolução, formato, tamanho, reaproveitamento).

```bash
python analisar_pdf.py
```

**Saída esperada:**
```
Imagens diferentes: 245
Páginas com imagens: 300
Páginas sem texto selecionável: 12
Tamanho das imagens extraídas: 87.43 MB

MAIORES IMAGENS
01. XREF=1042 | 2480x3508 | JPEG |    2.31 MB | 1 página(s)
02. XREF=1103 | 2480x3508 | JPEG |    2.18 MB | 1 página(s)
...
```

---

### 3️⃣ `teste_imagens.py` — Teste controlado (10 páginas)

Aplica redução de **escala (50%)** + **JPEG qualidade 40** apenas nas 10 primeiras páginas, salvando em `teste_10_paginas_v2.pdf`. Ideal para **calibrar parâmetros** antes de aplicar no arquivo inteiro.

```bash
python teste_imagens.py
```

Saída exemplo:
```
Página 1
  2480x3508 (1843.2 KB) -> 1240x1754 (312.7 KB)
Página 2
  2480x3508 (2011.5 KB) -> 1240x1754 (298.4 KB)
...
TESTE CONCLUÍDO
Tamanho: 4.87 MB
```

---

### 4️⃣ `teste_rewrite.py` — Otimização moderada

Usa `doc.rewrite_images()` com:
- `dpi_target=75`
- `quality=40`
- bitonal / color / gray habilitados

Resultado: boa redução mantendo legibilidade.

```bash
python teste_rewrite.py
```

---

### 5️⃣ `teste_rewrite2.py` — Otimização agressiva

Configuração mais forte (gera `lipe_30mb.pdf`):
- `dpi_target=50`
- `quality=25`

Ideal para PDFs que precisam caber em limites rígidos (ex.: 30 MB).

```bash
python teste_rewrite2.py
```

---

## 📊 Comparativo de abordagens

| Script | Método | DPI | Qualidade | Uso típico |
|---|---|---|---|---|
| `teste_imagens.py` | `replace_image()` manual | escala 50% | JPEG 40 | Calibração fina |
| `teste_rewrite.py` | `rewrite_images()` | 75 | 40 | Redução moderada |
| `teste_rewrite2.py` | `rewrite_images()` | 50 | 25 | Redução agressiva |

---

## ⚠️ Limitações conhecidas

- PDFs com **imagens vetoriais** ou **texto embutido** não são afetados por `rewrite_images()`.
- PDFs com **JBIG2 / JPEG2000** podem não ser reprocessados corretamente em versões antigas do PyMuPDF.
- Reduzir DPI abaixo de **~70** pode prejudicar OCR e leitura em telas grandes.
- `rewrite_images()` atua **no documento inteiro**; para testes parciais, use `replace_image()` (como em `teste_imagens.py`).

---

## 🛠️ Tecnologias

- **Python 3.9+**
- **PyMuPDF** (fitz) — leitura, renderização e reescrita de imagens em PDF
- **os**, **collections.Counter** — utilitários padrão

---

## 🗺️ Roadmap

- [ ] CLI unificada (`python -m pdfkit compress --dpi 75 --quality 40`)
- [ ] Relatório em JSON / CSV
- [ ] Detecção automática do "melhor" DPI com base em OCR
- [ ] Interface web simples (Streamlit)
- [ ] Suporte a comparação antes/depois lado a lado

---

## 📜 Licença

MIT — sinta-se livre para usar, modificar e distribuir.

---

## 🙋 Autor

**Roger Dias**
- GitHub: [@Zankary](https://github.com/Zankary)
- LinkedIn: [roger-dias-da-silva-071251428/](https://linkedin.com/in/roger-dias-da-silva-071251428/)

> Projeto desenvolvido como estudo de **otimização de PDFs com Python**, explorando o poder do PyMuPDF para diagnóstico e recompressão de imagens.
