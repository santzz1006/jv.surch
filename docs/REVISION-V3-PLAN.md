# PADDLE BRAWL — revisão pelas referências de 18:05

Pedido atual: seguir BRIEF-V3.md e as duas imagens WhatsApp; preservar sistemas funcionais. Confirmação posterior do usuário: times continuam AZUL / VERMELHO, substituindo roxo / amarelo do texto de referência.

## Base existente e problemas confirmados

- Combate autoritativo, sete primárias, melee, parry, super saque, munição e recarga; 13 verificações isoladas passaram após reduzir a curva da Spin Master.
- Filas locais 1v1/2v2/3v3/FFA, rounds, treino com sparring opcional, economia, inventário e tarefas implementados. Multiplayer com clientes reais ainda precisa ser verificado.
- HUD v2 já usa 16 PNGs individuais, mas o desenho e a composição estão abaixo das referências fornecidas.
- Animações R6 foram extraídas do pacote Tomiasz. O movimento das juntas foi medido durante deslocamento, mas a aprovação visual continua pendente: o usuário ainda percebe bugs.
- Raquete atual tem cabo comprido, pegada desalinhada e animação baseada em deslocar o modelo inteiro; precisa ser substituída por um viewmodel com ponto de pegada explícito.
- Lobby Blender v2 tinha deslocamento vertical de 14,75 studs devido ao centro do mesh combinado. Corrigido em ServerStorage ao posicionar CADA BasePart pelo centro mundial de seu accessor GLB. Não usar FindFirstChild(name,true) sem filtrar BasePart: o importador cria Model e MeshPart com o mesmo nome.
- DataStore ainda retorna StudioAccessToApisNotAllowed, mesmo após o usuário informar que ativou o acesso. Não declarar persistência testada.

## Etapas, em ordem

1. Consolidar combate existente; remodelar a raquete clássica e corrigir a pegada/viewmodel. Testar saque, colisões, dano, munição e recarga.
2. Separar AnimationController e ViewmodelController; curvas de antecipação/contato/recuperação, recarga real, inspeção, troca, corrida, pulo e slide. Validar visualmente em sequência.
3. Refazer HUD conforme imagem da partida: placar compacto, avatares/vida, timer com ampulheta, slots, tarefas com progresso, vida verde, menu de pausa 3×2. PNGs separados, fonte FredokaOne, sem números fictícios.
4. Refazer lobby Blender com portal central, palco circular, arquibancadas, árvores blocadas, refletores e painéis de modos/loja/passe; preservar dez arenas e campo de treino. Verificar escala, orientação e alinhamento arte/colisão.
5. Melhorar votação com miniaturas, avatares e seleção aleatória; verificar início de round.
6. Modelos/ícones/animações próprios das oito categorias, pooling, VFX e áudio originais; super saque.
7. Dividir serviços de partida/time/round/ranking e testar ciclo de modos, desconexões, placar e resultados.
8. Níveis, histórico, ranking, cosméticos/trails/emotes/passe e persistência com validação; informar bloqueios externos reais.
9. Layouts específicos para toque/controle, otimização, teste final, documentação/importador, salvar no Studio e pacote de fontes/assets.

## Restrições

- Exclusivamente R6 e rostos clássicos Roblox.
- Não regredir testes de servidor nem substituir sistemas por simulações visuais.
- Assets novos via Blender MCP e PNGs separados; cliente apenas apresenta resultados validados pelo servidor.
- Experiência permanece privada; salvamento em Roblox não equivale a publicação.
- Nenhum subagente autorizado nesta conversa.
