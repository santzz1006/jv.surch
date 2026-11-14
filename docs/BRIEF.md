Crie um jogo Roblox chamado "PADDLE BRAWL": FPS competitivo de ping-pong, com a MESMA estrutura, HUD e fluxo do jogo Rivals (Nosniy Games), mas em vez de armas de fogo a arma é a RAQUETE e a munição é a BOLINHA DE PING-PONG. Cartoon, rápido, com poderes e super arremessos. Funcionar em PC, mobile e console.

## REGRAS GERAIS
- Somente R6. Nada de R15. Rostos, cabelos e acessórios no estilo clássico dos itens do Roblox. Nunca gerar olhos ou rostos 3D customizados.
- Visual cartoon, cores saturadas, formas arredondadas, materiais chapados.
- Arquitetura: ServerScriptService (lógica), ReplicatedStorage (módulos e remotes), StarterPlayerScripts (cliente). O servidor valida hits, dano e cooldowns.
- Tudo configurável em um módulo Config (dano, cadência, velocidade, cooldown, recarga, tempo de round).

## GAMEPLAY (estilo Rivals)
- Primeira pessoa, mira central pequena (crosshair em cruz fina), mouse travado.
- Viewmodel: raquete + braço R6 cartoon no canto inferior direito, com bobbing ao andar, sway ao virar a câmera, animações de rebatida, recarga, inspect e troca.
- Movimento rápido: correr, pular, agachar, slide, bunny hop suave.
- Clique esquerdo rebate e dispara a bolinha (projétil muito rápido, quase hitscan) com rastro visível. Clique direito: mira com zoom leve ou parry (rebater a bolinha inimiga).
- A bolinha quica nas paredes e ganha velocidade a cada quique. Headshot = dano maior.
- Vida padrão 150. Tempo de abate curto. Granadas viram utilitários (bolinha explosiva, bolinha congelante).
- Slots de equipamento como no Rivals: 1) Primária, 2) Secundária, 3) Corpo a corpo (ex.: raquete de golpe curto), 4) Utilitário. Cada slot mostra ícone, munição atual e reserva.
- Nome da raquete equipada aparece no canto inferior direito (ex.: "Raquete Clássica").

## MODOS
- Duelos 1v1 (principal, ranqueado), 2v2, 3v3 e free-for-all.
- Duelo: melhor de rounds, primeiro a pontuar vence. Placar dos dois times no topo.
- Matchmaking, lobby, fila, rank/ELO simples.
- Tarefas diárias (ex.: "Jogar duelos 4/5", "Eliminações 9/15", "Vença duelos") com barra de progresso e recompensa (chaves/moedas).

## RAQUETES (armas) E PODERES
1. Clássica: equilibrada, rápida.
2. Sniper (Long Smash): carrega, bolinha perfurante de longo alcance.
3. Shotgun (Triple Serve): 3 bolinhas em leque, curta distância.
4. Rápida (Rally Rapid): cadência altíssima, dano baixo.
5. Curva (Spin Master): trajetória curva controlada.
6. Teleguiada (Homing): persegue o inimigo por 2s.
7. Gigante (Mega Smash): bolinha enorme, explosão em área, recarga lenta.
8. Corpo a corpo: raquete de golpe curto com knockback.
Ultimate: SUPER SAQUE (carrega com abates e acertos): câmera dinâmica curta, slow-motion, raquete brilhando, bolinha de fogo atravessando inimigos.
Skins de raquete e bolinha com raridades, efeitos de abate e trails.

## ANIMAÇÕES (prioridade máxima: fluidez como no vídeo de referência anexado)
- R6 e viewmodel com keyframes e easing suaves: idle, corrida, pulo, slide, rebatida, recarga, inspect, troca de raquete, super saque, dano, eliminação, vitória.
- Anticipation, follow-through e squash/stretch exagerados (cartoon). Transições sem cortes.
- Gerar via Blender (rig R6) ou keyframes em código, o que ficar mais fiel ao vídeo.

## HUD (estilo Rivals — NÃO desenhar em código)
Gerar PNGs com transparência de cada moldura e usar ImageLabel; o código só posiciona e preenche os dados com tween.
- Topo central: barra de placar em 3 partes: time da esquerda (moldura ROXA) com avatares, nível e ícone de plataforma + pontuação; no meio um timer escuro com ícone de ampulheta (ex.: 7.8); time da direita (moldura AMARELA) com avatares, nível, ícone de plataforma + pontuação. Barras de vida pequenas verdes sobre cada avatar.
- Topo esquerdo: botão do Roblox, menu, chat, microfone, configurações em botões redondos escuros.
- Abaixo deles: três botões redondos (ver jogadores, buscar, ranking).
- Topo direito: 4 slots de equipamento circulares (primária, secundária, corpo a corpo, utilitário), o ativo destacado em azul com munição "20 / 100"; ping e fps com a região do servidor.
- Esquerda: painel "Tarefas Diárias" com ícone, barras de progresso (azul em andamento, verde concluída com check) e ícone de recompensa.
- Inferior esquerdo: barra de vida verde com valor e coração (150).
- Inferior direito: nome da raquete atual.
- Mobile: botões translúcidos grandes: agachar/slide, mirar, atirar, recarregar, pular, inspecionar, joystick.
- Killfeed no canto, tela de eliminação, tela de vitória e derrota, loja, inventário e menu principal, todos em PNG no mesmo estilo cartoon com contorno grosso.

## VOTAÇÃO DE MAPA (estilo Rivals)
- Tela com fundo verde escuro e grade de cards de mapa (imagem do mapa + nome embaixo em faixa listrada, borda verde).
- Cards grandes em destaque no topo mostram os mapas mais votados com porcentagem (ex.: "Ponte [50%]", "Westown [50%]") com avatar de quem votou.
- Cards menores embaixo: "Aleatório" (ícone de shuffle), "Arena", "Backrooms", "Campo de Batalha", "Xadrez", "Portão" (etiqueta "Experimental"), "Parquinho", "Área de Experimentação".
- Timer de votação no topo (ex.: 5.3s). O mapa vencedor é carregado.
- Gerar um PNG de miniatura para cada mapa.

## MAPAS (modelar no Blender via MCP)
- Arenas compactas e simétricas: blocos, paredes altas, corredores, cantos, rampas, plataformas, cobertura baixa.
- Mapas: Ponte, Westown, Cemitério, Arena (blocos brancos), Backrooms, Campo de Batalha, Xadrez, Portão, Parquinho, Área de Experimentação (nomes de referência, versões cartoon com tema de ping-pong, mesas gigantes e bolinhas como cenário).
- Superfícies lisas para ricochete, quinas bem definidas, low-poly estilizado, FBX com escala correta, colisões simples, spawns por time.
- Gerar também: raquetes, bolinhas, trails, props.

## SISTEMAS EXTRAS
- Loja, caixas, moeda do jogo, passe de temporada (base), cosméticos, emotes.
- Performance: pooling de bolinhas e efeitos, poucas partes, FX leves.

## ENTREGA (em etapas)
1. Estrutura de pastas e scripts completos e comentados.
2. Lista de assets para o Blender (mapas, raquetes, animações, PNGs do HUD e das miniaturas) com especificações.
3. Passo a passo de importação no Roblox Studio.
4. Ordem: viewmodel + raquete + bolinha + rebatida, depois HUD base, depois mapa e votação, depois raquetes especiais, depois modos e matchmaking, depois polimento.