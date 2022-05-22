# Segmentos visíveis a partir de um ponto

O algoritmo detecta segmentos visíveis a partir da estratégia de linha de varredura radial.
Os pontos são convertidos em coordenadas polares e em seguida a fila de eventos é criada.
A cada ponto evento, se o ponto é "final" do segmento, o segmento é adicionado na
árvore de busca rubro negra, se é ponto de "inicio", o segmento é removido. A chave da árvore de busca é
o raio do ponto cujo evento o inseriu. A cada inserção/remoção, o segmento de valor mínimo na árvore é
considerado como ponto visível. O programa lê um arquivo com um ponto na primeira linha e os dados dos
segmentos nas demais.

A estratégia funciona para o caso geral, porém falha em vários casos. 
São eles:

> Segmentos ortogonais aos eixos (tomando o ponto como referência)

> Segmentos no início da linha de varredura

> Segmentos cujos pontos estão antes e depois do início da linha de varredura

> Empate no cálculo do raio ou do ângulo. 


Os testes foram realizados com os arquivos da pasta "dados/SEG_VISIVEIS_PTO", cada arquivo simula uma
ou mais falhas do caso geral. O ponto (0,0) foi utilizado como referência nos testes, uma vez que a translação
do espaço não altera o problema.
