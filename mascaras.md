# KNN

KNN é um modelo de aprendizado de máquina que busca encontrar as k correspondências mais próximas para determinar a qual classe pertence um item. Um exemplo: temos uma matriz de pixels brancos e pretos, na qual os brancos representam um objeto qualquer e os pretos o plano de fundo, como mostrado na imagem abaixo:

Sabendo que os pixels pretos e brancos não estão completamente isolados, como poderíamos identificar o que é objeto e plano de fundo? O KNN permite fazer isso, pois ele vai utilizar as distâncias dos pixels para definir o que é cada plano. Os cuidados que devemos ter ao utilizar essa máscara são quanto aos seus parâmetros como o nível de detecção de sombras nos objetos ou o limiar de distância entre o pixel e a amostra que podem influenciar bastante no resultado final do projeto.

# CMG

Método desenvolvido por Godbehere, Matsukawa e Goldberg que utiliza a inferência Bayesiana para definir objetos de primeiro plano e diferenciá-los do plano de fundo. Para definir um novo pixel, o algoritmo segue a fórmula de probabilidade dada por inferência bayesiana, mostrada abaixo:

alt text: Fórmula matemática da função de probabilidade P de A|B igual a P de A|B vezes P de A sobre B de B.

Uma forma de obter estimativas mais confiáveis em vídeo para as classificações de pixels é utilizar o filtro de Kalman. Também conhecido como estimativa quadrática linear (EQL), ele organiza os frames do vídeo de entrada para que construam o modelo. Após a etapa de previsão, temos a etapa de correção que reduz o ruído do primeiro estágio através de uma ponderação de pixels, obtendo um resultado final separando o objeto do primeiro plano do plano de fundo.

# CNT

CNT é uma abreviação para Count, ou contagem. Esse método tem uma lógica simples: é utilizado na contagem de frames para encontrar o fundo ou o objeto de primeiro plano da imagem. De modo que, se forem encontrados pixels que estejam estáveis por uma quantidade de frames, eles serão considerados plano de fundo. Caso esses pixels não permaneçam estáveis, serão considerados um objeto de primeiro plano.

Uma curiosidade é que o CNT é muito mais rápido que qualquer outra solução de subtração de fundo no OpenCV.

# MOG

MOG é uma abreviação de Mixture of Gaussians, que em português podemos adaptar para Mistura de fundo adaptativa. Nela é feita uma distribuição gaussiana (também conhecida como distribuição normal para cada pixel, de forma que seja caracterizado por sua intensidade no espaço de cores RGB.

A cada nova cena (ou frame) são feitas distribuições gaussianas que contribuem para a modelação do plano de fundo de um pixel. No cálculo é feita a soma das múltiplas distribuições de forma que 3 parâmetros principais são considerados em cada gaussiano:

Média: estimativas das médias de intensidade da cor;
Variância: estimativas da variação da média;
Peso: número de gaussianas por pixel que representam a quantidade de tempo que essas cores estiveram presentes na cena.
Depois dessa etapa, é feita a classificação de pixels como fundo ou objeto de primeiro plano. Essa classificação consiste em definir se o pixel é gaussiano de plano de fundo. Aqueles que não forem são classificados como objeto de primeiro plano.

