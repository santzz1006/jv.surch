# PADDLE BRAWL

Novo projeto R6. Referência funcional: duelos rápidos em primeira pessoa, raquetes e bolinhas; identidade visual PADDLE BRAWL.

## Ordem de implementação
1. Viewmodel, rebatida e projétil validados no servidor.
2. HUD com PNGs e controles PC/toque/gamepad.
3. Arenas Blender, lobby e votação.
4. Raquetes especiais, parry e super saque.
5. Modos, filas, ranking e progressão.
6. Testes de gameplay, importação e apresentação.

## Dependências externas
- Upload de meshes e PNGs requer asset:read, asset:write e diretório autorizado no MCP do Studio.
- Publicação e matchmaking entre servidores precisam de uma experiência publicada. A fase local deve oferecer fila no próprio servidor e treino solo para testes.
- Raiz dos executáveis auxiliares do Blender: C:/Users/neila/.codex/tools/blender-mcp (fora da pasta do jogo).

## Assets de origem
- Tomiasz, asset 11989848355: 2 cópias já presentes no Studio na inspeção inicial; usar apenas os KeyframeSequences R6 selecionados. Não havia scripts nas cópias inspecionadas.
- HUD gerado pela ferramenta nativa image_gen; assets/ui/hud-atlas-transparent.png contém alpha 0–255 e 16 regiões.
