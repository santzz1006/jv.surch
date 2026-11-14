# PADDLE BRAWL — revisão V3

## Implementado nesta revisão

- 27 PNGs independentes, renderizados no Blender: componentes do HUD, ícones coloridos e menu. Os ícones preservam suas cores; as molduras identificam azul/vermelho.
- Oito modelos de raquetes em Blender/FBX/GLB, oito ícones e modelos importados no Studio.
- Lobby reconstruído com portal, plataforma octogonal, arquibancadas, refletores, árvores, quiosques de modos/loja, treino e temporada.
- Dez arenas receberam detalhes temáticos, marcações dos times e miniaturas novas. Arte importada e escala normalizada; colisões usam a mesma especificação geométrica.
- Viewmodel com pegada comum entre braço e raquete, transições, antecipação, rebatidas distintas por equipamento, recarga, inspeção, troca, corrida, pulo, parry e Super Saque.
- Corrigidos acesso prematuro à cabeça e interrupção da troca de equipamento. Raquetes de terceira pessoa agora usam os novos modelos via WeaponService.
- HUD com placar/avatar/vida, slots, munição, barra de vida animada, dano, tarefas, menu 3×2, configurações locais e botões de lobby.
- Pooling limitado de bolinhas e impactos. Quatro efeitos sonoros procedurais originais, publicados como assets; reprodução ainda não confirmada.
- Controles de toque em camada própria, botões IAS de troca e ultimate; controles nativos de movimento/pulo preservados.
- Votação com substituição de voto, aleatório, desempate aleatório e avatares; cards não são recriados a cada segundo.
- Histórico das últimas 20 partidas, ranking do servidor com ELO real, posições simétricas de equipes e quatro spawns distintos de FFA.
- Validação de deslocamento no servidor e medição de ping por ida/volta.

## Evidências de teste

- 13/13 testes isolados de combate passaram: headshot, cooldown, rejeição de NaN, fogo amigo, recarga, seis armas especiais, parry e ultimate.
- 16/16 verificações de votação e distribuição de spawns passaram.
- Lobby V3, campo de treino, HUD e menu 3×2 foram observados no Studio. Troca para Rally Rapid mostrou o modelo correto e atualização de munição.
- Inicialização dos scripts revisados sem erro de Luau no último teste. Posteriormente, o Studio registrou timeout de CorePackages/Scheduler e a ferramenta deixou de responder normalmente.
- Capturas do cenário ficam brancas quando o Studio está minimizado. Restaurar a janela permitiu observar o jogo.

## Não considerar o projeto concluído

- Persistência NÃO validada: Roblox continua retornando StudioAccessToApisNotAllowed (403), apesar da confirmação do usuário sobre a configuração. A progressão fica na sessão; não se tentou contornar a restrição.
- Não houve uma partida completa com múltiplos clientes reais. Fluxos de 1v1/2v2/3v3/FFA, abandono/reconexão e final de partida ainda exigem teste integrado.
- Mobile/console foram implementados, mas não validados em dispositivos reais. A navegação e os limites de layout precisam de auditoria nessas plataformas.
- Reprodução/permissões dos quatro sons ainda precisam ser confirmadas; primeiro probe retornou IsLoaded=false e TimeLength=0.
- O ranking mostrado é do servidor. Ranking global, catálogo completo de trails/efeitos de eliminação, animação dedicada de vitória, identificação confiável de região e a divisão completa da arquitetura pedida no brief ainda não estão concluídos.
- Super Saque tem efeito/gesto/projétil autoritativo; slow-motion visual controlado e sincronismo fino do contato ainda precisam de polimento.
- Aprovação visual final das animações e desempenho em multiplayer continuam pendentes.

## Testar

1. Abrir o projeto placeId 107266350772804, deixar Studio visível e iniciar Play.
2. No lobby: JOGAR abre modos; TREINAR entra no campo; MENU abre a grade.
3. No treino: WASD, Shift, C; clique esquerdo saca; direito defende; R recarrega; F inspeciona; 1–4 trocam; Q usa Super Saque carregado; M abre menu.
4. SPARRING: OFF/ON controla se o adversário do treino atira. Acertar os alvos carrega o ultimate.
5. Comparar todas as armas pelo equipamento no lobby, verificar munição e observar se a mão permanece presa ao cabo durante a rebatida.
6. Testar dois clientes reais antes de publicar. A experiência permanece privada; salvar não publica.

## Fontes e assets

`src/` contém os módulos. `assets/ui/v3`, `assets/weapon-icons`, `assets/models/v3`, `assets/models`, `assets/maps` e `assets/audio` contêm os arquivos reais e manifests com IDs. Os arquivos Blender, GLB e FBX são editáveis; PNGs têm alpha.

`tools/InstallSources.luau` é um restaurador dos scripts para o projeto existente, não um instalador autossuficiente de todos os assets. Não usar scripts antigos de geração V2 para sobrescrever a revisão V3.
