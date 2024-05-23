# Contexto

Você tem disponível dados de coversão e impressões de 3 anúncios recentemente lançados. Seu objetivo é **recomendar qual anúncio deve ser exibido para cada segmento**. Essa campanha será lançada na segunda-feira e ficará no ar até a quinta-feira subsequente. Os resultados serão avaliados no fim de semana subsequente (sexta-feira, sábado e domingo).

# Dados

- `impressions.csv`
    - `ts`: timestamp da avaliação de exibição do anúncio
    - `ad`: ID do anúncio
    - `segment`: segmento que visualizou o anúncio
    - `impressions`: número de impressões
- `conversions.csv`
    - `ad`: ID do anúncio
    - `segment`: segmento que visualizou o anúncio
    - `date`: data avaliação de conversão do anúncio
    - `conversions`: número de conversões

# Entrega

Notebook R ou Python com o descritivo da solução, o código e a recomendação.