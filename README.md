# code

Pequenos scripts Python para download de vídeos.

## youtube.py

Baixa vídeos do YouTube em lote a partir de uma lista de URLs, usando [yt-dlp](https://github.com/yt-dlp/yt-dlp).

**Instalação:**

```bash
pip install yt-dlp
```

**Uso:**

1. Crie um arquivo de texto com uma URL do YouTube por linha (linhas vazias ou iniciadas com `#` são ignoradas). Por padrão o script usa `link_youtube.txt`.
2. Execute:

   ```bash
   python youtube.py
   ```

   Ou, para usar outro arquivo de links:

   ```bash
   python youtube.py meus_links.txt
   ```

3. Os vídeos são baixados (áudio + vídeo mesclados em `.mp4`, melhor qualidade disponível) para a pasta `downloads/`. Ao final é exibido um resumo com sucessos, falhas e tempo total.

## drive.py

Baixa vídeos do Google Drive em lote a partir de uma lista de URLs, usando [yt-dlp](https://github.com/yt-dlp/yt-dlp). Igual ao `youtube.py`, mas separado para não misturar os dois tipos de link.

**Instalação:**

```bash
pip install yt-dlp
```

**Uso:**

1. Crie um arquivo de texto com uma URL do Google Drive por linha (formato `https://drive.google.com/file/d/.../view`; linhas vazias ou iniciadas com `#` são ignoradas). Por padrão o script usa `link_drive.txt`.
2. Execute:

   ```bash
   python drive.py
   ```

   Ou, para usar outro arquivo de links:

   ```bash
   python drive.py meus_links.txt
   ```

3. Os vídeos são baixados para a pasta `downloads/`. Ao final é exibido um resumo com sucessos, falhas e tempo total.

> Só funciona para arquivos aos quais você já tem permissão de visualização (link "qualquer pessoa com o link pode visualizar" ou compartilhado diretamente com sua conta).

## video.py

Script simples que baixa um único arquivo `.mp4` a partir de uma URL fixa (usa a biblioteca `requests`) e salva como `video.mp4`. Serve como exemplo/protótipo pontual, sem relação com `youtube.py`.

**Instalação:**

```bash
pip install requests
```

## link_youtube.txt

Arquivo de exemplo com links de entrada usado por `youtube.py`.

