# Imagens ilustrativas geradas por IA

A branch tem integração em `bot.py` para ler os arquivos `preview/assets/generated/<id>.webp` e copiá-los para `site/assets/generated/` durante a publicação.

**As imagens WebP ainda precisam estar efetivamente presentes no repositório** antes do merge. Elas estão no pacote `SeuPetFeliz-imagens-34-produtos.zip` gerado na conversa. Não realizar merge sem confirmar isso.

Os 34 IDs no pacote correspondem às imagens genéricas criadas; `bs-024` mantém a ilustração antiga. O gerador conserva os links da Amazon, a pesquisa, o GA4 e usa SVG como fallback.

As fotografias são representações geradas por IA, não fotos oficiais das embalagens. Identificá-las como "Imagem ilustrativa · IA".

Validação: `python bot.py && python -m unittest discover -s tests -v`; verificar arquivo `site/assets/generated/bs-001.webp` e assim por diante.