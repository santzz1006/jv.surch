PROMPT MESTRE — DESENVOLVIMENTO COMPLETO DO PADDLE BRAWL (ROBLOX)

Você é um desenvolvedor sênior especializado em Roblox Studio, Luau, arquitetura multiplayer, FPS competitivo, animações 3D, interfaces e otimização de jogos.

Sua missão é desenvolver um jogo completo chamado PADDLE BRAWL, um FPS competitivo de ping-pong para Roblox.

Não quero apenas um protótipo visual, uma demonstração ou scripts isolados. Quero um projeto organizado, funcional, expansível e preparado para publicação no Roblox.

Utilize como referência visual as imagens anexadas nesta conversa, principalmente a imagem do HUD durante a partida.

⸻

1. VISÃO GERAL DO JOGO

PADDLE BRAWL é um FPS competitivo no qual os jogadores utilizam raquetes de ping-pong como armas e bolinhas como projéteis.

A experiência deve combinar:

* Combate rápido em primeira pessoa.
* Movimentação fluida.
* Raquetes com características diferentes.
* Super arremessos e habilidades especiais.
* Partidas competitivas.
* Sistema de progressão.
* Skins e cosméticos.
* Mapas compactos e simétricos.
* Interface cartoon profissional.

Referência de experiência: Rivals, da Nosniy Games.

A estrutura competitiva, a organização das informações e o fluxo de partida devem seguir essa referência, mas todos os elementos visuais, personagens, armas, mapas e identidade devem ser originais do PADDLE BRAWL.

Identidade visual:

* Cartoon 3D.
* Cores saturadas.
* Contornos definidos.
* Materiais simples e chapados.
* Iluminação vibrante.
* Formas arredondadas.
* Animações exageradas e fluidas.
* Personagens exclusivamente R6.

Paleta principal:

* Azul: #087BFF
* Ciano: #00D9FF
* Roxo: #762BFF
* Amarelo: #FFC928
* Verde: #32E85D
* Azul escuro: #18213D

2. REGRAS OBRIGATÓRIAS DE DESENVOLVIMENTO

1. Utilizar exclusivamente personagens R6.
2. Não utilizar R15 em nenhuma circunstância.
3. Respeitar os rostos clássicos do Roblox.
4. Não criar rostos ou olhos 3D personalizados.
5. Todo o código deve ser escrito em Luau.
6. O servidor deve controlar dano, acertos, cooldowns, munição e validação de projéteis.
7. O cliente controla câmera, HUD, viewmodel, efeitos visuais e entrada de comandos.
8. Utilizar ModuleScripts para configurações e sistemas reutilizáveis.
9. Não deixar botões sem funcionalidade.
10. Não utilizar dados fictícios para simular sistemas que deveriam ser funcionais.
11. Não colocar toda a lógica em um único Script.
12. Evitar scripts gigantes e código duplicado.
13. Comentar os sistemas mais importantes.
14. Implementar tratamento de erros e validação de RemoteEvents.
15. Otimizar para partidas multiplayer.

Utilizar esta arquitetura:

ReplicatedStorage:

* Config
* Modules
* Remotes
* Assets
* Animations
* UIAssets
* WeaponAssets
* Effects

ServerScriptService:

* MainServer
* CombatService
* ProjectileService
* PlayerService
* MatchService
* RoundService
* TeamService
* WeaponService
* AbilityService
* QuestService
* EconomyService
* DataService
* RankingService

StarterPlayer:

* StarterPlayerScripts
    * ClientController
    * CameraController
    * MovementController
    * ViewmodelController
    * InputController
    * CombatController
    * AnimationController
    * HUDController
    * AudioController

StarterGui:

* MainHUD
* PauseMenu
* MatchResults
* VotingInterface
* InventoryInterface
* ShopInterface
* MainMenu

Workspace:

* Lobby
* Maps
* ActiveMatch
* SpawnPoints

3. CONFIGURAÇÃO CENTRAL

Criar um ModuleScript chamado Config.

Todos os valores importantes devem ser configuráveis:

* Vida padrão: 150.
* Dano das raquetes.
* Multiplicador de headshot.
* Velocidade dos projéteis.
* Cadência de disparo.
* Quantidade de munição.
* Munição reserva.
* Tempo de recarga.
* Cooldown das habilidades.
* Velocidade dos jogadores.
* Velocidade de corrida.
* Força de pulo.
* Tempo de duração dos rounds.
* Quantidade de rounds.
* Tempo de votação.
* Velocidade dos ricochetes.
* Multiplicadores de velocidade por ricochete.

Não espalhar valores fixos pelos scripts.

4. PRIMEIRA PESSOA E VIEWMODEL

Criar um sistema FPS completo.

A câmera deve funcionar em primeira pessoa, com mouse travado no PC e controles adequados para mobile e console.

O viewmodel deve conter:

* Braço R6 cartoon.
* Raquete equipada.
* Posição no canto inferior direito.
* Animação idle.
* Bobbing durante caminhada.
* Sway ao movimentar a câmera.
* Animação de corrida.
* Animação de pulo.
* Animação de rebatida.
* Animação de recarga.
* Animação de inspeção.
* Animação de troca de raquete.
* Animação de habilidade especial.

As animações precisam apresentar antecipação, impacto, follow-through e squash/stretch.

Não utilizar movimentos robóticos ou transições bruscas.

A raquete precisa acompanhar a câmera de maneira natural.

O viewmodel não pode atravessar a câmera nem bloquear a mira.

5. SISTEMA DE COMBATE

Clique esquerdo:

* Rebater a bolinha.
* Criar projétil.
* Aplicar efeitos de impacto.

Clique direito:

* Mirar com zoom leve.
* Permitir parry conforme a mecânica da raquete.

As bolinhas devem:

* Possuir velocidade elevada.
* Ter rastro visível.
* Detectar colisões.
* Quicar nas paredes.
* Ganhar velocidade progressivamente.
* Causar dano ao atingir jogadores.
* Permitir headshots.
* Ser recicladas por pooling.

O servidor precisa validar cada acerto.

Implementar proteção contra:

* Disparos falsificados.
* Munição negativa.
* Disparos fora do cooldown.
* Dano enviado diretamente pelo cliente.
* Spam de RemoteEvents.

6. RAQUETES

Implementar oito equipamentos:

1. Clássica — equilibrada.
2. Sniper / Long Smash — carregamento e perfuração.
3. Shotgun / Triple Serve — três bolinhas em leque.
4. Rápida / Rally Rapid — cadência elevada.
5. Curva / Spin Master — trajetória controlável.
6. Teleguiada / Homing — perseguição por dois segundos.
7. Gigante / Mega Smash — projétil grande e explosivo.
8. Corpo a corpo — golpe curto com knockback.

Cada raquete deve possuir:

* Modelo 3D.
* Ícone.
* Nome.
* Dano.
* Cadência.
* Velocidade.
* Munição.
* Tempo de recarga.
* Habilidade exclusiva.
* Animação própria.
* Efeitos sonoros.
* Efeitos visuais.

Criar uma estrutura que permita adicionar novas raquetes facilmente.

7. ULTIMATE — SUPER SAQUE

Implementar uma habilidade especial carregada por acertos e eliminações.

Quando ativada:

* Executar uma animação especial.
* Fazer a raquete brilhar.
* Aplicar efeito curto de câmera.
* Ativar slow-motion controlado.
* Criar uma bolinha de fogo.
* Atravessar inimigos.
* Aplicar dano.
* Criar explosão visual no impacto.

A habilidade precisa ter duração limitada e cooldown adequado.

8. MOVIMENTAÇÃO

Implementar:

* Caminhada.
* Corrida.
* Pulo.
* Agachamento.
* Slide.
* Bunny hop suave.
* Aceleração e desaceleração.
* Animações sincronizadas.

A movimentação deve ser rápida, responsiva e competitiva.

Não permitir exploração de velocidade através de exploits.

9. HUD — PRIORIDADE VISUAL

A interface deve seguir a imagem de referência anexada.

Não quero uma interface genérica construída com vários Frames simples.

IMPORTANTE: criar os elementos gráficos como PNGs transparentes separados, utilizando ImageLabels e ImageButtons no Roblox Studio.

Os scripts devem somente posicionar os elementos, atualizar informações e executar tweens.

9.1 Placar superior

Criar uma barra dividida em três partes:

Esquerda:

* Moldura roxa.
* Avatares dos jogadores.
* Nível.
* Ícone da plataforma.
* Pontuação.
* Barras de vida verdes.

Centro:

* Fundo escuro.
* Ícone de ampulheta.
* Cronômetro.

Direita:

* Moldura amarela.
* Avatares.
* Níveis.
* Ícones de plataforma.
* Pontuação.
* Barras de vida.

9.2 Botões superiores esquerdos

* Roblox.
* Menu.
* Chat.
* Microfone.
* Configurações.

Botões circulares escuros, com ícones brancos.

Abaixo:

* Ver jogadores.
* Buscar.
* Ranking.

9.3 Equipamentos superiores direitos

Quatro slots circulares:

1. Primária.
2. Secundária.
3. Corpo a corpo.
4. Utilitário.

O slot selecionado deve apresentar destaque azul.

Mostrar munição, por exemplo:

20 / 100

Exibir ping, FPS e região do servidor.

9.4 Tarefas diárias

Painel localizado à esquerda.

Título: Tarefas Diárias.

Exemplos:

* Jogar duelos: 2/5.
* Eliminações: 7/15.
* Vença duelos.

Cada tarefa deve possuir:

* Ícone.
* Texto.
* Barra de progresso.
* Recompensa.
* Estado concluído.

As barras devem utilizar azul durante o progresso e verde quando concluídas.

9.5 Vida

Inferior esquerdo:

* Moldura verde.
* Coração.
* Valor de vida.
* Animação de redução.
* Efeito visual ao receber dano.

Vida padrão: 150.

9.6 Raquete equipada

Inferior direito:

Exibir o nome da raquete atual.

Exemplo: Raquete Clássica.

9.7 Crosshair

Criar uma mira central pequena, formada por quatro traços finos.

A mira deve:

* Permanecer centralizada.
* Expandir durante disparos.
* Reagir a acertos.
* Mudar discretamente de aparência ao mirar.

10. MENU DE PAUSA

Criar o menu central seguindo a segunda imagem de referência.

O menu deve aparecer sobre o cenário, com transparência e desfoque leve.

Título: Menu do Jogo.

Organização em grade de três colunas e duas linhas:

Primeira linha:

* Voltar ao Jogo.
* Loja.
* Inventário.

Segunda linha:

* Tarefas.
* Configurações.
* Sair da Partida.

Botões grandes, escuros, com ícones brancos.

O botão de fechar deve ficar no canto superior direito.

Ao clicar em Voltar ao Jogo, fechar o menu e devolver os controles ao jogador.

A pausa não deve interromper a partida para os demais jogadores.

11. INTERFACE MOBILE E CONSOLE

Criar layouts específicos por plataforma.

Mobile:

* Joystick esquerdo.
* Atirar.
* Mirar.
* Recarregar.
* Pular.
* Agachar.
* Slide.
* Inspecionar.
* Trocar equipamento.

Os botões devem ser grandes, translúcidos e posicionados para os polegares.

Console:

* Compatibilidade com controle.
* Mapeamento de botões.
* Navegação por foco.
* Seleção de menus.
* Mira com analógico.
* Feedback visual dos comandos.

Não simplesmente reduzir a interface de PC para mobile.

12. MAPAS

Criar arenas compactas, simétricas e competitivas.

Mapas:

1. Ponte.
2. Westown.
3. Cemitério.
4. Arena.
5. Backrooms.
6. Campo de Batalha.
7. Xadrez.
8. Portão.
9. Parquinho.
10. Área de Experimentação.

Características:

* Paredes altas.
* Corredores.
* Rampas.
* Plataformas.
* Coberturas baixas.
* Cantos estratégicos.
* Spawns separados.
* Superfícies adequadas para ricochetes.

Estilo low-poly cartoon.

Utilizar Blender para modelagem quando houver ferramentas disponíveis.

Gerar FBX com escala correta, colisões simplificadas e organização dos objetos.

Se houver MCP do Blender disponível, utilizá-lo para criar os modelos. Caso contrário, criar scripts auxiliares ou especificações de modelagem.

Não fingir que arquivos 3D foram gerados quando isso não tiver acontecido.

13. VOTAÇÃO DE MAPA

Criar uma interface com fundo verde escuro.

Cards grandes:

* Imagem do mapa.
* Nome.
* Porcentagem de votos.
* Avatar dos jogadores que votaram.

Cards menores:

* Aleatório.
* Arena.
* Backrooms.
* Campo de Batalha.
* Xadrez.
* Portão.
* Parquinho.
* Área de Experimentação.

Portão deve possuir etiqueta Experimental.

Exibir cronômetro de votação.

Ao finalizar:

* Contabilizar votos no servidor.
* Selecionar o mapa vencedor.
* Carregar a arena.
* Posicionar jogadores.
* Iniciar a partida.

Impedir votos duplicados.

14. MODOS DE JOGO

Implementar:

* 1v1 ranqueado.
* 2v2.
* 3v3.
* Free-for-all.

Criar:

* Sistema de fila.
* Matchmaking.
* Times.
* Rounds.
* Placar.
* Vitória.
* Derrota.
* Histórico.
* ELO.
* Ranking.

O modo principal deve ser o duelo 1v1.

15. PROGRESSÃO

Implementar:

* Níveis.
* XP.
* Moedas.
* Chaves.
* Tarefas diárias.
* Recompensas.
* Loja.
* Inventário.
* Caixas.
* Skins.
* Efeitos de eliminação.
* Trails.
* Emotes.
* Passe de temporada.

Salvar dados utilizando DataStoreService com tratamento de falhas e proteção contra perda de dados.

16. ASSETS GRÁFICOS

Criar uma lista organizada de assets necessários.

Gerar PNGs transparentes separados para:

* Molduras do placar.
* Slots de equipamentos.
* Ícones das raquetes.
* Ícones das bolinhas.
* Painel de tarefas.
* Barra de vida.
* Botões do menu.
* Molduras de avatares.
* Ícones de recompensas.
* Telas de vitória e derrota.
* Tela de eliminação.
* Elementos da loja.
* Inventário.
* Votação de mapas.

Criar também miniaturas individuais dos mapas.

Todos os elementos devem seguir a mesma identidade visual.

Não colocar o HUD inteiro em uma única imagem. Cada componente precisa ser independente para permitir atualizações dinâmicas.

17. ANIMAÇÕES

Prioridade máxima: fluidez.

Criar animações para:

* Idle.
* Corrida.
* Pulo.
* Queda.
* Slide.
* Rebatida.
* Recarga.
* Inspeção.
* Troca de raquete.
* Super Saque.
* Recebimento de dano.
* Eliminação.
* Vitória.

Utilizar keyframes, easing e transições suaves.

Evitar movimentos mecânicos.

Quando possível, utilizar animações criadas no Blender e exportadas para Roblox.

18. DESEMPENHO

O jogo precisa funcionar bem em dispositivos diferentes.

Implementar:

* Pooling de projéteis.
* Pooling de efeitos.
* Limitação de partículas.
* Gerenciamento de conexões.
* Otimização de raycasts.
* StreamingEnabled quando apropriado.
* Redução de cálculos desnecessários.
* Replicação eficiente.

Priorizar estabilidade em servidores multiplayer.

19. ORDEM OBRIGATÓRIA DE DESENVOLVIMENTO

Não tente construir tudo de uma vez sem testar.

Desenvolva em etapas:

ETAPA 1 — COMBATE

* Estrutura de pastas.
* Config.
* Primeira pessoa.
* Viewmodel.
* Raquete clássica.
* Bolinha.
* Disparo.
* Colisões.
* Dano.
* Munição.
* Recarga.

ETAPA 2 — ANIMAÇÕES

* Idle.
* Bobbing.
* Sway.
* Rebatida.
* Recarga.
* Troca de raquete.

ETAPA 3 — HUD

* Placar.
* Timer.
* Slots.
* Munição.
* Vida.
* Crosshair.
* Tarefas.
* Menu de pausa.

ETAPA 4 — MAPAS

* Arena inicial.
* Spawns.
* Colisões.
* Ricochetes.
* Miniaturas.

ETAPA 5 — VOTAÇÃO

* Interface.
* Sistema de votos.
* Carregamento do mapa.

ETAPA 6 — RAQUETES ESPECIAIS

* Sniper.
* Shotgun.
* Rápida.
* Curva.
* Teleguiada.
* Gigante.
* Corpo a corpo.
* Ultimate.

ETAPA 7 — MULTIPLAYER

* 1v1.
* 2v2.
* 3v3.
* FFA.
* Matchmaking.
* ELO.

ETAPA 8 — PROGRESSÃO

* Loja.
* Inventário.
* Moedas.
* Skins.
* Tarefas.
* Passe.

ETAPA 9 — POLIMENTO

* Áudio.
* Efeitos.
* Otimização.
* Testes.
* Compatibilidade mobile e console.

20. REGRAS DE EXECUÇÃO DO CODEX

Antes de começar:

1. Analise todos os arquivos existentes no workspace.
2. Identifique se já existe um projeto Roblox iniciado.
3. Preserve os arquivos que já estiverem funcionando.
4. Organize a estrutura antes de implementar.
5. Crie um planejamento técnico.

Durante o desenvolvimento:

* Crie os arquivos reais no workspace.
* Não responda apenas com blocos de código.
* Implemente os scripts diretamente.
* Não deixe funcionalidades essenciais como pseudocódigo.
* Teste cada sistema antes de avançar.
* Verifique referências entre módulos.
* Verifique RemoteEvents e RemoteFunctions.
* Corrija erros encontrados.
* Documente como importar os assets.
* Mantenha o projeto organizado.

Se uma funcionalidade depender de uma ação manual no Roblox Studio, explique exatamente o que preciso fazer.

Se não houver conexão direta com o Roblox Studio, não alegue que publicou ou executou o jogo. Prepare os arquivos para importação e explique o procedimento.

Ao finalizar cada etapa, apresentar:

* Arquivos criados.
* Sistemas implementados.
* O que já funciona.
* O que ainda falta.
* Como testar no Roblox Studio.

IMPORTANTE: NÃO FINALIZE O PROJETO APENAS COM A CRIAÇÃO DA ESTRUTURA DE PASTAS. IMPLEMENTE OS SISTEMAS DE VERDADE.

Comece agora pela análise do workspace e pela ETAPA 1. Continue desenvolvendo o projeto em etapas, sem substituir funcionalidades existentes por simulações visuais.