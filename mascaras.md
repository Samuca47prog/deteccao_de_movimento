Cada máscara aplica um algorítmo diferente para identificar os pixels que se movem na imagem


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



---

Durante as aulas foram utilizados diferentes modelos de detecção de movimento e cada um deles apresentou um resultado distinto. Além da importância de comparar os resultados entre cada um dos modelos, pode ser interessante alterar os seus parâmetros na tentativa de melhorar ainda mais o resultado encontrado.

Vamos checar cada um dos parâmetros que podem ser modificados nos modelos e os valores padrões que foram utilizados durante os vídeos. A documentação de cada um deles também pode ser vista abaixo:

KNN: createBackgroundSubtractorKNN()

history=500 → comprimento da “história”, responsável pelo número de frames para acumular os pesos de todo o período de processamento. Quando o valor é muito pequeno tem maior sensibilidade a mudanças repentinas de luminosidade. Quando é muito grande pode atrapalhar no caso de termos um vídeo com muita variação de luminosidade.

dist2Threshold=400 → indica o limiar de distância entre o pixel e a amostra para decidir se um pixel está próximo de um outro (plano de fundo ou objeto detectado).

detectShadows=True → é o controle de detecção de sombras nos objetos. Usamos o parâmetro True para ativá-lo e False para desativá-lo. Se ativado, o tempo de processamento é maior.

GMG: createBackgroundSubtractorGMG()

initializationFrames = 120 → é o número de quadros para inicializar o modelo de fundo (120 quadros = 5s).

decisionThreshold=0.8 → valor limite em que os pixels são classificados como plano de fundo ou primeiro plano. Quanto maior o valor, mais objetos perdemos na imagem. Portanto, em um valor 0.9 ou 1.0 (90% e 100%) a detecção não fica tão boa.

MOG: createBackgroundSubtractorMOG()

history = 100 → comprimento da “história”, responsável pelo número de frames para acumular os pesos de todo o período de processamento. Quando o valor é muito pequeno tem maior sensibilidade a mudanças repentinas de luminosidade. Quando é muito grande, pode atrapalhar no caso de termos um vídeo com muita variação de luminosidade.

nmixtures = 5 → número de misturas gaussianas que serão usadas. Usar um valor alto aumenta drasticamente o tempo de processamento.

backgroundRatio = 0.7 → proporção de plano de fundo que será utilizado. Um valor muito baixo para esse valor pode resultar em muitos falsos positivos.

noiseSigma = 0 → nível de ruído aceito pelo algoritmo. Usando o valor 0 estamos deixando com que ele decida aleatoriamente o valor utilizado.

MOG2: createBackgroundSubtractorMOG2()

history = 500 → comprimento da “história”, responsável pelo número de frames para acumular os pesos de todo o período de processamento. Quando o valor é muito pequeno tem maior sensibilidade a mudanças repentinas de luminosidade. Quando é muito grande pode atrapalhar caso tenhamos um vídeo com muita variação de luminosidade.

detectShadows=True → diferente do MOG, o MOG2 tem um controle de detecção de sombras nos objetos e usa o parâmetro True para ativá-lo e False para desativá-lo. Se ativado, o tempo de processamento é maior.

varThreshold=100 → correlaciona o peso dos pixels no quadro atual com os valores do modelo. Valores mais baixos tendem a criar objetos falsos.

CNT: createBackgroundSubtractorCNT()

minPixelStability=15 → indica o número de frames a serem aguardados antes do pixel ser marcado como estável ou como plano de fundo.

useHistory =True → parecido com o history dos algoritmos anteriores, indica se estamos dando crédito para um pixel por ele ser estável por um longo período de tempo.

maxPixelStability=1560 → é o crédito máximo de um pixel dentro da história. O valor recomendado é 1560 (60 segundos).

isParallel=True → determina se estamos paralelizando o algoritmo.