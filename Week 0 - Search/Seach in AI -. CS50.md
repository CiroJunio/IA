## [Inteligência artificial](https://cs50.harvard.edu/ai/2024/notes/0/#artificial-intelligence)

A Inteligência Artificial (IA) abrange uma gama de técnicas que aparecem como comportamento senciente pelo computador. Por exemplo, a IA é usada para reconhecer rostos em fotografias nas suas redes sociais, vencer o Campeão do Mundo no xadrez e processar sua fala quando você fala com Siri ou Alexa no seu telefone.

Neste curso, exploraremos algumas das ideias que tornam a IA possível:

0. **Procurar**

Encontrar uma solução para um problema, como um aplicativo de navegação que encontra a melhor rota da sua origem até o destino, ou como jogar um jogo e descobrir o próximo movimento.

1. **Conhecimento**

Representar informações e tirar inferências delas.

2. **Incerteza**

Lidando com eventos incertos usando probabilidade.

3. **Otimização**

Encontrar não apenas uma maneira correta de resolver um problema, mas uma maneira melhor — ou a melhor — de resolvê-lo.

4. **Aprendizado**

Melhorando o desempenho com base no acesso a dados e experiência. Por exemplo, seu e-mail é capaz de distinguir spam de e-mails não spam com base em experiências passadas.

5. **Redes Neurais**

Uma estrutura de programa inspirada no cérebro humano que é capaz de executar tarefas de forma eficaz.

6. **Linguagem**

Processamento de linguagem natural, que é produzida e compreendida por humanos.

## [Procurar](https://cs50.harvard.edu/ai/2024/notes/0/#search)

Problemas de busca envolvem um agente que recebe um estado inicial e um estado objetivo, e ele retorna uma solução de como ir do primeiro para o último. Um aplicativo de navegação usa um processo de busca típico, onde o agente (a parte pensante do programa) recebe como entrada sua localização atual e seu destino desejado, e, com base em um algoritmo de busca, retorna um caminho sugerido. No entanto, existem muitas outras formas de problemas de busca, como quebra-cabeças ou labirintos.
![[Pasted image 20241122133351.png]]
Encontrar uma solução para um quebra-cabeça de 15 exigiria o uso de um algoritmo de busca.

- **Agente**
    
    Uma entidade que percebe seu ambiente e age sobre esse ambiente. Em um aplicativo de navegação, por exemplo, o agente seria uma representação de um carro que precisa decidir quais ações tomar para chegar ao destino.
    
- **Estado**
    
    Uma configuração de um agente em seu ambiente. Por exemplo, em um [quebra-cabeça 15](https://en.wikipedia.org/wiki/15_puzzle) , um estado é qualquer maneira em que todos os números são dispostos no tabuleiro.
    
    - **Estado Inicial**
        
        O estado do qual o algoritmo de busca começa. Em um aplicativo de navegação, seria a localização atual.
        
- **Ações**
    
    Escolhas que podem ser feitas em um estado. Mais precisamente, ações podem ser definidas como uma função. Ao receber o estado `s`como entrada, `Actions(s)`retorna como saída o conjunto de ações que podem ser executadas no estado `s`. Por exemplo, em um _quebra-cabeça 15_ , as ações de um dado estado são as maneiras pelas quais você pode deslizar quadrados na configuração atual (4 se o quadrado vazio estiver no meio, 3 se próximo a um lado, 2 se no canto).
    
- **Modelo de Transição**
    
    Uma descrição de qual estado resulta da execução de qualquer ação aplicável em qualquer estado. Mais precisamente, o modelo de transição pode ser definido como uma função. Ao receber estado `s`e ação `a`como entrada, `Results(s, a)`retorna o estado resultante da execução de ação `a`em estado `s`. Por exemplo, dada uma certa configuração de um _quebra-cabeça 15_ (estado `s`), mover um quadrado em qualquer direção (ação `a`) levará a uma nova configuração do quebra-cabeça (o novo estado).
    
- **Espaço de Estado**
    
    O conjunto de todos os estados alcançáveis ​​a partir do estado inicial por qualquer sequência de ações. Por exemplo, em um quebra-cabeça 15, o espaço de estados consiste em todas as 16!/2 configurações no tabuleiro que podem ser alcançadas a partir de qualquer estado inicial. O espaço de estados pode ser visualizado como um gráfico direcionado com estados, representados como nós, e ações, representadas como setas entre nós.
![[Pasted image 20241122133407.png]]
- **Teste de Metas**
    
    A condição que determina se um dado estado é um estado objetivo. Por exemplo, em um aplicativo de navegação, o teste objetivo seria se a localização atual do agente (a representação do carro) está no destino. Se estiver — problema resolvido. Se não estiver — continuamos a busca.
    
- **Custo do caminho**
    
    Um custo numérico associado a um determinado caminho. Por exemplo, um aplicativo de navegação não o leva simplesmente ao seu objetivo; ele faz isso minimizando o custo do caminho, encontrando o caminho mais rápido possível para você chegar ao seu estado de objetivo.
## [Resolvendo problemas de pesquisa](https://cs50.harvard.edu/ai/2024/notes/0/#solving-search-problems)

- **Solução**
    
    Uma sequência de ações que leva do estado inicial ao estado objetivo.
    
    - **Solução Ótima**
        
        Uma solução que tem o menor custo de caminho entre todas as soluções.
        

Em um processo de pesquisa, os dados geralmente são armazenados em um **_nó_** , uma estrutura de dados que contém os seguintes dados:

- Um _estado_
- Seu _nó pai_ , através do qual o nó atual foi gerado
- A _ação_ que foi aplicada ao estado do pai para chegar ao nó atual
- O _custo do caminho_ do estado inicial até este nó

_Os nós_ contêm informações que os tornam muito úteis para os propósitos de algoritmos de busca. Eles contêm um _estado_ , que pode ser verificado usando o _teste de meta_ para ver se é o estado final. Se for, o _custo do caminho do nó pode ser comparado aos_ _custos do caminho_ de outros nós , o que permite escolher a _solução ótima_ . Uma vez que o nó é escolhido, em virtude do armazenamento do _nó pai_ e da _ação_ que levou do _pai_ ao nó atual, é possível rastrear cada passo do caminho do _estado inicial_ até este nó, e esta sequência de ações é a _solução_ .

No entanto, _os nós_ são simplesmente uma estrutura de dados — eles não pesquisam, eles guardam informações. Para realmente pesquisar, usamos a **fronteira** , o mecanismo que “gerencia” os _nós_ . A _fronteira_ começa contendo um estado inicial e um conjunto vazio de itens explorados, e então repete as seguintes ações até que uma solução seja alcançada:

Repita:

1. Se a fronteira estiver vazia,
    
    - _Pare._ Não há solução para o problema.
2. Remova um nó da fronteira. Este é o nó que será considerado.
    
3. Se o nó contiver o estado objetivo,
    
    - Retorne a solução. _Pare_ .
    
    Outro,
    
    ```
    * Expand the node (find all the new nodes that could be reached from this node), and add resulting nodes to the frontier.
    * Add the current node to the explored set.
    ```
#### [Busca em profundidade](https://cs50.harvard.edu/ai/2024/notes/0/#depth-first-search)

Na descrição anterior da _fronteira_ , uma coisa não foi mencionada. No estágio 2 do pseudocódigo acima, qual nó deve ser removido? Essa escolha tem implicações na qualidade da solução e na rapidez com que ela é alcançada. Há várias maneiras de abordar a questão de quais nós devem ser considerados primeiro, duas das quais podem ser representadas pelas estruturas de dados de **pilha** (na busca _em profundidade_ ) e **fila** (na _busca em largura_ ; e [aqui está uma demonstração fofa de desenho animado](https://www.youtube.com/watch?v=2wM6_PuBIxY) da diferença entre os dois).

Começamos com a abordagem de busca _em profundidade_ ( _DFS_ ).

Um algoritmo de busca _em profundidade_ esgota cada direção antes de tentar outra direção. Nesses casos, a fronteira é gerenciada como uma estrutura de dados _de pilha_ . O slogan que você precisa lembrar aqui é “ _último a entrar, primeiro a sair_ ”. Depois que os nós são adicionados à fronteira, o primeiro nó a ser removido e considerado é o último a ser adicionado. Isso resulta em um algoritmo de busca que vai o mais fundo possível na primeira direção que atrapalha, enquanto deixa todas as outras direções para depois.

(Um exemplo de uma aula externa: imagine uma situação em que você está procurando suas chaves. Em uma abordagem de busca _em profundidade_ , se você escolher começar procurando em suas calças, você primeiro vasculharia cada bolso, esvaziando cada bolso e examinando o conteúdo cuidadosamente. Você parará de procurar em suas calças e começará a procurar em outro lugar somente quando tiver esgotado completamente a busca em cada bolso de suas calças.)

- Prós:
    - Na melhor das hipóteses, esse algoritmo é o mais rápido. Se ele “tiver sorte” e sempre escolher o caminho certo para a solução (por acaso), então a busca _em profundidade_ leva o menor tempo possível para chegar a uma solução.
- Contras:
    - É possível que a solução encontrada não seja a ideal.
    - Na pior das hipóteses, esse algoritmo explorará todos os caminhos possíveis antes de encontrar a solução, levando assim o maior tempo possível antes de chegar à solução.

Exemplo de código:
```python
  # Define the function that removes a node from the frontier and returns it.
    def remove(self):
    	  # Terminate the search if the frontier is empty, because this means that there is no solution.
        if self.empty():
            raise Exception("empty frontier")
        else:
        	  # Save the last item in the list (which is the newest node added)
            node = self.frontier[-1]
            # Save all the items on the list besides the last node (i.e. removing the last node)
            self.frontier = self.frontier[:-1]
            return node
```
#### [Busca em Largura](https://cs50.harvard.edu/ai/2024/notes/0/#breadth-first-search)

O oposto da busca _em profundidade_ seria a busca _em largura_ ( _BFS_ ).

Um algoritmo de busca _em largura_ seguirá várias direções ao mesmo tempo, dando um passo em cada direção possível antes de dar o segundo passo em cada direção. Neste caso, a fronteira é gerenciada como uma estrutura de dados _de fila_ . O slogan que você precisa lembrar aqui é “ _primeiro a entrar, primeiro a sair_ ”. Neste caso, todos os novos nós são somados em linha, e os nós estão sendo considerados com base em qual foi adicionado primeiro (primeiro a chegar, primeiro a ser atendido!). Isso resulta em um algoritmo de busca que dá um passo em cada direção possível antes de dar um segundo passo em qualquer direção.

(Um exemplo de uma aula externa: suponha que você esteja em uma situação em que está procurando suas chaves. Nesse caso, se você começar com suas calças, você vai olhar no seu bolso direito. Depois disso, em vez de olhar no seu bolso esquerdo, você vai olhar em uma gaveta. Depois na mesa. E assim por diante, em todos os lugares que você puder pensar. Somente depois de ter esgotado todos os lugares você vai voltar para suas calças e procurar no próximo bolso.)

- Prós:
    - Este algoritmo tem a garantia de encontrar a solução ótima.
- Contras:
    - É quase certo que esse algoritmo levará mais tempo do que o mínimo para ser executado.
    - Na pior das hipóteses, esse algoritmo leva o maior tempo possível para ser executado.

Exemplo de código:

```python
    # Define the function that removes a node from the frontier and returns it.
    def remove(self):
    	  # Terminate the search if the frontier is empty, because this means that there is no solution.
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Save the oldest item on the list (which was the first one to be added)
            node = self.frontier[0]
            # Save all the items on the list besides the first one (i.e. removing the first node)
            self.frontier = self.frontier[1:]
            return node
```
#### [Busca gananciosa do melhor primeiro](https://cs50.harvard.edu/ai/2024/notes/0/#greedy-best-first-search)

Os algoritmos de busca em largura e em profundidade são ambos **desinformados** . Ou seja, esses algoritmos não utilizam nenhum conhecimento sobre o problema que não tenham adquirido por meio de sua própria exploração. No entanto, na maioria das vezes, algum conhecimento sobre o problema está, de fato, disponível. Por exemplo, quando um solucionador de labirinto humano entra em uma junção, o humano pode ver qual caminho vai na direção geral da solução e qual caminho não vai. A IA pode fazer o mesmo. Um tipo de algoritmo que considera conhecimento adicional para tentar melhorar seu desempenho é chamado de algoritmo de busca **informado** .

**A busca gananciosa do melhor primeiro** expande o nó que está mais próximo do objetivo, conforme determinado por uma **função heurística** _h(n)_ . Como o nome sugere, a função estima o quão próximo do objetivo o próximo nó está, mas pode estar enganada. A eficiência do algoritmo _ganancioso do melhor primeiro_ depende de quão boa é a função heurística. Por exemplo, em um labirinto, um algoritmo pode usar uma função heurística que depende da **distância de Manhattan** entre os nós possíveis e o fim do labirinto. A _distância de Manhattan_ ignora paredes e conta quantos passos para cima, para baixo ou para os lados seriam necessários para ir de um local até o local do objetivo. Esta é uma estimativa fácil que pode ser derivada com base nas coordenadas (x, y) do local atual e do local do objetivo.
![[Pasted image 20241122133949.png]]
Distância de Manhattan

No entanto, é importante enfatizar que, como qualquer heurística, ela pode dar errado e levar o algoritmo por um caminho mais lento do que ele teria seguido de outra forma. É possível que um algoritmo de busca _desinformado_ forneça uma solução melhor mais rápido, mas é menos provável que faça isso do que um algoritmo _informado_ .

#### [A* Search](https://cs50.harvard.edu/ai/2024/notes/0/#a-search)

Um desenvolvimento do algoritmo _ganancioso best-first_ , _a busca A*_ considera não apenas _h(n)_ , o custo estimado do local atual até o objetivo, mas também _g(n)_ , o custo que foi acumulado até o local atual. Ao combinar esses dois valores, o algoritmo tem uma maneira mais precisa de determinar o custo da solução e otimizar suas escolhas em andamento. O algoritmo mantém o controle de ( _custo do caminho até agora_ + _custo estimado até o objetivo_ ) e, uma vez que ele exceda o custo estimado de alguma opção anterior, o algoritmo abandonará o caminho atual e retornará à opção anterior, evitando assim que ele próprio siga por um caminho longo e ineficiente que _h(n)_ erroneamente marcou como o melhor.

Mais uma vez, como esse algoritmo também depende de uma heurística, ele é tão bom quanto a heurística que ele emprega. É possível que em algumas situações ele seja menos eficiente do que a busca _gananciosa do melhor primeiro_ ou mesmo os algoritmos _desinformados . Para que_ _a busca A*_ seja ótima, a função heurística, _h(n)_ , deve ser:

1. _Admissível_ , ou nunca _superestimar_ o custo real, e
2. _Consistente_ , o que significa que o custo estimado do caminho para o objetivo de um novo nó, além do custo de transição para ele a partir do nó anterior, é maior ou igual ao custo estimado do caminho para o objetivo do nó anterior. Para colocá-lo em uma forma de equação, _h(n)_ é consistente se para cada nó _n_ e nó sucessor _n'_ com custo de passo _c_ , _h(n) ≤ h(n') + c_ .
### [Busca Adversária](https://cs50.harvard.edu/ai/2024/notes/0/#adversarial-search)

Enquanto, anteriormente, discutimos algoritmos que precisam encontrar uma resposta para uma pergunta, na **busca adversarial** o algoritmo enfrenta um oponente que tenta atingir o objetivo oposto. Frequentemente, a IA que usa busca adversarial é encontrada em jogos, como jogo da velha.

#### [Minimax](https://cs50.harvard.edu/ai/2024/notes/0/#minimax)

Um tipo de algoritmo em busca adversarial, **Minimax** representa condições vencedoras como (-1) para um lado e (+1) para o outro lado. Outras ações serão conduzidas por essas condições, com o lado minimizador tentando obter a pontuação mais baixa, e o maximizador tentando obter a pontuação mais alta.

**Representando uma IA do jogo da velha** :

- _S₀_ : Estado inicial (no nosso caso, um tabuleiro 3X3 vazio)
- _Jogadores(es)_ : uma função que, dado um estado _s_ , retorna a vez de qual jogador (X ou O).
- _Ações(ões)_ : uma função que, dado um estado _s_ , retorna todos os movimentos legais neste estado (quais espaços estão livres no tabuleiro).
- _Resultado(s, a)_ : uma função que, dado um estado _s_ e uma ação _a_ , retorna um novo estado. Este é o tabuleiro que resultou da execução da ação _a_ no estado _s_ (fazer um movimento no jogo).
- _Terminal(s)_ : uma função que, dado um estado _s_ , verifica se este é o último passo do jogo, ou seja, se alguém ganhou ou se há um empate. Retorna _True_ se o jogo terminou, _False_ caso contrário.
- _Utilidade(s)_ : uma função que, dado um estado terminal _s_ , retorna o valor de utilidade do estado: -1, 0 ou 1.

**Como o algoritmo funciona** :

Recursivamente, o algoritmo simula todos os jogos possíveis que podem ocorrer começando no estado atual e até que um estado terminal seja alcançado. Cada estado terminal é avaliado como (-1), 0 ou (+1).
![[Pasted image 20241122134025.png]]
Algoritmo Minimax no Jogo da Velha

Sabendo com base no estado de quem é a vez, o algoritmo pode saber se o jogador atual, ao jogar de forma otimizada, escolherá a ação que leva a um estado com um valor menor ou maior. Dessa forma, alternando entre minimizar e maximizar, o algoritmo cria valores para o estado que resultariam de cada ação possível. Para dar um exemplo mais concreto, podemos imaginar que o jogador maximizador pergunta a cada turno: "se eu tomar essa ação, um novo estado resultará. Se o jogador minimizador jogar de forma otimizada, que ação esse jogador pode tomar para levar ao menor valor?" No entanto, para responder a essa pergunta, o jogador maximizador tem que perguntar: "Para saber o que o jogador minimizador fará, preciso simular o mesmo processo na mente do minimizador: o jogador minimizador tentará perguntar: 'se eu tomar essa ação, que ação o jogador maximizador pode tomar para levar ao maior valor?'" Esse é um processo recursivo e pode ser difícil de entender; olhar o pseudocódigo abaixo pode ajudar. Eventualmente, por meio desse processo de raciocínio recursivo, o jogador maximizador gera valores para cada estado que podem resultar de todas as ações possíveis no estado atual. Após ter esses valores, o jogador maximizador escolhe o mais alto.
![[Pasted image 20241122134040.png]]
O Maximizador considera os valores possíveis de estados futuros.

Para colocar em pseudocódigo, o algoritmo Minimax funciona da seguinte maneira:

- Dado um estado _s_
    
    - O jogador maximizador escolhe a ação _a_ em _Actions(s)_ que produz o maior valor de _Min-Value(Result(s, a))_ .
    - O jogador minimizador escolhe a ação _a_ em _Actions(s)_ que produz o menor valor de _Max-Value(Result(s, a))_ .
- Função _Max-Value(estado)_
    
    - _v = -∞_
        
    - se _Terminal(estado)_ :
        
        retornar _Utilitário(estado)_
        
    - para _ação_ em _Ações(estado)_ :
        
        v _= Max(v, Min-Value(Resultado(estado, ação)))_
        
        retornar _v_
        
- Função _Min-Value(estado)_ :
    
    - _v = ∞_
        
    - se _Terminal(estado)_ :
        
        retornar _Utilitário(estado)_
        
    - para _ação_ em _Ações(estado)_ :
        
        v _= Min(v, Max-Value(Resultado(estado, ação)))_
        
        retornar _v_
        

#### [Poda Alfa-Beta](https://cs50.harvard.edu/ai/2024/notes/0/#alpha-beta-pruning)

Uma maneira de otimizar _o Minimax_ , **Alpha-Beta Pruning** pula alguns dos cálculos recursivos que são decididamente desfavoráveis. Após estabelecer o valor de uma ação, se houver evidência inicial de que a ação seguinte pode levar o oponente a obter uma pontuação melhor do que a ação já estabelecida, não há necessidade de investigar mais essa ação porque ela será decididamente menos favorável do que a previamente estabelecida.

Isso é mais facilmente demonstrado com um exemplo: um jogador maximizador sabe que, na próxima etapa, o jogador minimizador tentará atingir a pontuação mais baixa. Suponha que o jogador maximizador tenha três ações possíveis, e a primeira delas vale 4. Então o jogador começa a gerar o valor para a próxima ação. Para fazer isso, o jogador gera os valores das ações do minimizador se o jogador atual fizer essa ação, sabendo que o minimizador escolherá a mais baixa. No entanto, antes de terminar o cálculo para todas as ações possíveis do minimizador, o jogador vê que uma das opções tem o valor três. Isso significa que não há razão para continuar explorando as outras ações possíveis para o jogador minimizador. O valor da ação ainda não valorizada não importa, seja 10 ou (-10). Se o valor for 10, o minimizador escolherá a opção mais baixa, 3, que já é pior do que o 4 pré-estabelecido. Se a ação ainda não valorizada for (-10), o minimizador escolherá esta opção, (-10), que é ainda mais desfavorável ao maximizador. Portanto, computar ações possíveis adicionais para o minimizador neste ponto é irrelevante para o maximizador, porque o jogador maximizador já tem uma escolha inequivocamente melhor cujo valor é 4.
![[Pasted image 20241122134052.png]]
#### [Minimax com profundidade limitada](https://cs50.harvard.edu/ai/2024/notes/0/#depth-limited-minimax)

Há um total de 255.168 jogos possíveis de Jogo da Velha, e 10²⁹⁰⁰⁰ jogos possíveis no Xadrez. O algoritmo minimax, como apresentado até agora, requer a geração de todos os jogos hipotéticos de um certo ponto até a condição terminal. Embora computar todos os jogos de Jogo da Velha não represente um desafio para um computador moderno, fazer isso com xadrez é atualmente impossível.

**O Minimax com profundidade limitada** considera apenas um número predefinido de movimentos antes de parar, sem nunca chegar a um estado terminal. No entanto, isso não permite obter um valor preciso para cada ação, uma vez que o fim dos jogos hipotéticos não foi alcançado. Para lidar com esse problema, _o Minimax com profundidade limitada_ depende de uma **função de avaliação** que estima a utilidade esperada do jogo a partir de um determinado estado ou, em outras palavras, atribui valores aos estados. Por exemplo, em um jogo de xadrez, uma função de utilidade tomaria como entrada uma configuração atual do tabuleiro, tentaria avaliar sua utilidade esperada (com base em quais peças cada jogador tem e suas localizações no tabuleiro) e, em seguida, retornaria um valor positivo ou negativo que representa o quão favorável o tabuleiro é para um jogador em relação ao outro. Esses valores podem ser usados ​​para decidir sobre a ação correta e, quanto melhor a função de avaliação, melhor o algoritmo Minimax que depende dela.
