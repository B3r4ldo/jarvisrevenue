# JARVIS Revenue Bot — MVP 1.0

Projeto Python sem dependências externas que transforma uma lista de produtos **aprovados manualmente** em um site estático de recomendações. **Nenhuma renda é garantida.**

## Rodar no Windows 11

1. Instale Python 3.12+ (https://www.python.org/downloads/), marcando **Add Python to PATH**.
2. Descompacte o projeto.
3. Abra PowerShell na pasta e execute:

```powershell
py -3 bot.py
py -3 -m http.server 8000 --directory site
```

4. Abra http://localhost:8000.

## Inserir produtos

Edite `data/products.csv` no Excel ou editor UTF-8. Campos obrigatórios:

- `id`: único, estável.
- `title`: nome verificável.
- `category`: grupo do produto.
- `description`: análise original, objetiva, sem promessas sem fonte.
- `url`: link HTTPS especial gerado pelo programa de afiliados, autorizado para publicação em **site público**.
- `status`: `draft` para não publicar; `approved` para publicar.

Os exemplos são **rascunhos** e não aparecem no site. Faça o cadastro de afiliado e obtenha seus links antes de marcar qualquer linha como `approved`. O bot não inventa preços, descontos, avaliações, disponibilidade nem utiliza raspagem de marketplaces.

## Publicação sem custos de servidor (GitHub Pages)

1. Crie repositório no GitHub, preferencialmente **público** para Pages no plano gratuito; **não armazene credenciais ou dados pessoais no repositório**.
2. Suba todo o conteúdo do projeto, incluindo `.github/workflows/publish.yml`.
3. Em Settings > Pages > Build and deployment, selecione Source: **GitHub Actions**.
4. Em Actions, execute `Build affiliate catalog` por `Run workflow`.
5. O site será publicado no endereço fornecido pelo GitHub Pages após o deploy, se o recurso estiver habilitado no plano/repositório.
6. O workflow também gera o site ao atualizar o catálogo na branch principal e tenta atualizá-lo diariamente (cron em UTC, sem garantia de horário exato).

**Nota**: o workflow só republica o catálogo já informado. Ele **não descobre ofertas, verifica preços, coleta comissões ou traz visitantes automaticamente**.

## Boas práticas e compliance

- Cadastre o site no programa de afiliados e mantenha aviso de comissão visível.
- Leia as políticas vigentes do programa, inclusive restrições de links em canais, uso de imagens e APIs.
- Não copie fotografias ou descrições de terceiros sem direito de uso.
- Crie avaliações editoriais úteis, com informação verificada. Evite páginas vazias ou conteúdo de baixa qualidade.
- Antes do lançamento, crie política de privacidade, canais de contato e identificação do responsável adequados à operação, principalmente se instalar analytics/cookies.
- Não publique links de afiliados no Telegram, WhatsApp ou email antes de confirmar que o programa escolhido permite tal canal. O MVP usa somente seu próprio site.
- Use exclusivamente o GitHub Pages para a parte estática; ele não executa Python quando alguém visita o site.
- Monitore resultados por relatórios oficiais de afiliados; não confunda cliques com vendas comissionadas.

## Arquivos

- `bot.py`: valida CSV, gera HTML, busca de produtos, disclosure e estatísticas básicas de catálogo.
- `data/products.csv`: conteúdo editorial sob controle humano.
- `.github/workflows/publish.yml`: execução agendada e publicação automática.
- `site/`: gerado pelo script, não é necessário versionar.

## Próximas versões

1. Importador via API oficial (somente após aprovação de acesso e validação dos termos).
2. Monitoramento de links e alertas privados de erros.
3. Analytics com privacidade e funil de conversão.
4. Testes A/B de páginas e conteúdo genuinamente útil.
5. Fluxo de revisão editorial antes de atualizar ofertas.
