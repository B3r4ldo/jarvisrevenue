# SeuPetFeliz — fotografias oficiais e métricas

## Imagens dos produtos
O catálogo `data/products.csv` tem colunas `image_url` e `image_source`. Cada foto deve corresponder exatamente ao anúncio (marca, sabor, tamanho e embalagem). Só preencher URL quando houver permissão comercial documentada.

Fontes aceitas: `amazon-creators-api`, `brand-authorized`, `owner-licensed`. Não baixar ou reproduzir fotos de anúncios da Amazon sem licença, nem usar fotos de outros produtos para mascarar ausência da imagem. Imagens sem fonte permanecem como ilustração.

Exemplo: `image_url=https://.../embalagem-autorizada.jpg`, `image_source=brand-authorized`.

## Analytics
Crie propriedade Google Analytics 4 e um fluxo Web. Copie o ID de medição `G-XXXXXXXXXX` (não é segredo). No GitHub, configure Settings → Secrets and variables → Actions → Variables → New repository variable: `GA4_MEASUREMENT_ID` com esse valor. O workflow `publish.yml` injetará o identificador na página. Visitantes podem aceitar/recusar rastreamento no aviso. A ausência do ID mantém o analytics desligado.

Eventos: `view_home`, `view_category`, `search_products` e `click_affiliate_link`. Eventos de clique não comprovam vendas; acompanhe conversões e comissões pelo painel de Associados.

## Fluxo de publicação
Testar primeiro na branch `feature/seupetfeliz-imagens-analytics`; publicar em `main` apenas após aprovação dos testes e revisão. A associação de imagens reais requer direitos de uso e fornecimento das URLs, e a configuração do GA4 requer o ID do fluxo.
