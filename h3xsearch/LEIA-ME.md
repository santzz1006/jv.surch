# Cópia dos arquivos públicos de H3X Search

Origem: https://h3xsearch.com/ — captura em 13/11/2026.

## Conteúdo

- `site/`: arquivos originais recebidos por HTTP, com caminhos preservados. Inclui HTML, CSS, JavaScript compilado, fontes, imagens, manifesto e a resposta JSON de `/api/config`.
- `json-ld/`: dados estruturados extraídos dos HTMLs. São metadados de páginas, perguntas frequentes e organização, não um catálogo de produtos.
- `json/config.json`: cópia formatada da configuração pública.
- `manifest-download.json`: URLs, status HTTP, tamanhos e SHA-256 de cada arquivo recebido.
- `COMO-FUNCIONA-A-BUSCA.md`: análise do JavaScript público.
- `download.py`: script para repetir o download dos recursos públicos referenciados, limitado ao domínio e a 250 URLs. Não autentica nem contorna verificações.

## Visualizar no computador

Nesta pasta, execute:

```powershell
python -m http.server 8080 --bind 127.0.0.1 --directory site
```

Abra http://127.0.0.1:8080/ ou execute `visualizar.ps1`. Para encerrar, pressione Ctrl+C no terminal.

É necessário servir por HTTP porque os caminhos dos arquivos começam com `/` e o aplicativo usa módulos JavaScript. Abrir o HTML com duplo clique não reproduz corretamente o site.

## Limites da cópia

O layout e as páginas informativas estão disponíveis localmente. A busca real NÃO funciona apenas com um servidor estático: exige os endpoints de backend, uma sessão válida e a verificação Turnstile do domínio original. A cópia preserva o JavaScript original, inclusive essas dependências; por isso, a interface pode apresentar erro de sessão ou de verificação localmente.

Não foi obtido o código privado do servidor, um banco completo de anúncios ou respostas JSON de produtos. O fluxo protegido não foi contornado. O script baixa recursos públicos descobertos por referências; não enumera arquivos ocultos nem garante uma cópia de tudo que exista no servidor. Serviços externos, como Cloudflare, Discord, Hubbuy e imagens de anúncios não carregados, não fazem parte do espelho.

Os arquivos JavaScript são o build distribuído ao navegador, não o projeto fonte original com seus componentes e configuração de build.
