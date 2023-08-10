# spotify-music-analysis
Análise descritiva, sem treinamento, de dados obtidos pela API do spotify.

* Criar supergêneros, um supergênero é um conjunto de gẽneros que, devido à sua similaridade, podem ser agrupados e representados por um único representante, o supergênero. 
  - Buscar os gêneros do spotify (https://developer.spotify.com/documentation/web-api/reference/get-recommendation-genres) e de alguma forma agregá-los por supergêneros; pode servir de ajuda: https://zenodo.org/record/4778563
  - É importante ressaltar que este mapeamento para supergêneros deve ser realizado na hora de popular o banco, transformando os gêneros -> supergêneros.
  
* Popular o banco com nós de supergêneros e músicas, músicas que estão relacionadas a um artista de gênero x, que pertence a um supergêro X, estão ligadas ao nó deste supergênero.
  - Para encontrar estas músicas, a ideia é fazer um search por gênero e market BR, e popular o banco com as músicas dos top y artistas.
  
  
* Lista de Análises:
	- Fazer acompanhamento anual das músicas de determinados gêneros, observando as variações nas métricas
	- Fazer comparação entre gêneros de diferentes mercados
	- Média das métricas por top X 
	- (Se possível) Geração de regras de subgrupos baseado nas métricas

### TODO List:
   - [x] Definir e documentar os supergêneros
   - [x] Popular o banco com todos os supergêneros definidos
   - [ ] Adaptar o Script para transformar gêneros da música lida em supergêneros durante persistência
   - [ ] Popular o banco com as relações entre supergêneros e músicas
   - [ ] Plotar acompanhamento anual das músicas de N gêneros distintos
   - [ ] Plotar popularidade de gêneros em diferentes mercados
   - [ ] Realizar a média das métricas no TOP X dos mercados
   - [ ] (Se possível) Realizar geração de regras de subgrupos baseados nas métricas das músicas