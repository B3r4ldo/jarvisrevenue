# Piloto comercial SeuPetFeliz — 14 dias

Estado: materiais preparados. Perfis sociais e conta de anúncios ainda não conectados. Nenhuma publicação social agendada; nenhum gasto realizado.

## Seleção e evidência

Seis produtos já existentes: Ultrapads Lavanda 80x60 30un, Blue Premium 30un, Good Pad 60x60 50un, Pipicat Classic 4kg, Viva Verde Grãos Finos 4kg e Dreamies Carne 150g.

Critério: indicadores públicos indexados de compras, presença em listas de mais vendidos e adequação à reposição de itens. Não é um ranking auditado de vendas atuais. Viva Verde tem evidência menos precisa para a variante; mantê-lo como teste comparativo. Evidências e URLs em selection.json, consultadas em 21/10/2026. Não divulgar as contagens nas peças: variam por data e variante. Não utilizar preços estáticos nem anunciar descontos não confirmados.

## Material preparado

- Três páginas geradas a cada build em /guias/: tapetes-higienicos.html, areia-para-gatos.html e petiscos-para-gatos.html.
- content-14-days.csv: 14 legendas, chamadas e links com UTMs, relativos ao dia de início; nenhuma data de postagem presumida.
- creatives/: 14 peças quadradas, uma por dia. Imagens genéricas identificadas como ilustrativas.
- ad-drafts.json: duas propostas de anúncios e orçamento sugerido, sem ativação.

## Lançamento

1. Confirmar o perfil oficial do Instagram e cadastrar o canal no Programa de Associados.
2. Conferir no painel Amazon se os links existentes têm a atribuição correta ao associado; não substituir links encurtados automaticamente por URLs inferidas.
3. Conectar o perfil a uma integração de publicação/agendamento compatível. Importar a fila e definir início e horário. Para posts no feed, o link não é clicável: atualizar o link do perfil para o guia correspondente ou usar uma página de links e medir os botões. Stories com adesivo de link podem usar o destino direto; exigem peças próprias no formato vertical.
4. Publicar organicamente. Conferir UTMs e cliques; os relatórios GA4 disponíveis dependem do consentimento.
5. Antes de ativar anúncios, revisar a campanha concreta e o limite de gasto com o proprietário. Evitar usar imagem ilustrativa como fotografia exata do item comercial.

## Orçamento proposto — R$ 300 de teto, condicionado à revisão da campanha

- Primeira tranche: R$ 100, até R$ 20/dia por 5 dias, R$ 50 para cada guia de higiene. Não dividir em muitos conjuntos.
- Segunda tranche: até R$ 100, somente após revisar tráfego, cliques e relatório Amazon; a ausência de evidência comercial não autoriza reinvestimento automático.
- Reserva: R$ 100. Liberar apenas se comissões qualificadas atribuíveis justificarem o investimento. Se o rastreamento não permitir atribuição confiável, manter orçamento pausado e registrar a incerteza.
- Sem aumentar orçamento automaticamente. Taxa de clique ou custo por clique baixos não comprovam lucro.

## Medição e critérios

GA4: sessões por source/medium/campaign, visitas aos guias e click_affiliate_link com product_id, product_category e campaign_page. Não somar o evento click automático aos cliques personalizados.

Amazon: pedidos, itens enviados, comissões e estornos. O GA4 não recebe confirmação de compra da Amazon. UTMs medem aquisição até o nosso site; não criam atribuição de comissão dentro da Amazon. Solicitar IDs de rastreamento separados no painel se disponíveis e preencher somente links oficiais efetivamente gerados; não inventar tags.

Indicadores: taxa de saída para Amazon = cliques únicos/sessões; receita por visita = comissões qualificadas atribuíveis/sessões; resultado do piloto = comissões atribuíveis menos mídia e ferramentas. Aguardar a consolidação das comissões, considerando cancelamentos/devoluções, antes de declarar rentabilidade.

Hipótese para dimensionamento, não previsão: receita qualificada de R$100 × comissão hipotética de 11% = R$11. Se 2% das sessões gerarem essa compra, R$0,22 por sessão seria o limite bruto ilustrativo. Usar valores reais do relatório para decidir.

## Automação entregue e limites

O build gera guias e uma fila determinística a partir dos produtos e textos revisados. O workflow existente publica o site automaticamente. Não coleta avaliações, preços ou imagens da Amazon por scraping. Agendamento social e leitura de relatórios ainda dependem de conexão de contas; não há robô de postagem ativo. Recomendações de orçamento exigem revisão humana.
