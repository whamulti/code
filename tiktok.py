#!/usr/bin/env python3
"""
TikTok Video Downloader
Lê URLs de um arquivo .txt e baixa os vídeos um por um.

Dependências:
    pip install yt-dlp

Uso:
    1. Crie um arquivo link_tiktok.txt com uma URL do TikTok por linha
    2. Execute: python tiktok.py
    3. Ou especifique outro arquivo: python tiktok.py meus_link_tiktok.txt
"""

import sys
import os
import time

try:
    import yt_dlp
except ImportError:
    print("❌ Biblioteca 'yt-dlp' não encontrada.")
    print("   Instale com: pip install yt-dlp")
    sys.exit(1)


# ── Configurações ────────────────────────────────────────────────────────────

ARQUIVO_LINKS   = "link_tiktok.txt"             # arquivo padrão com as URLs
PASTA_SAIDA     = r"C:\Users\Ricardo\Videos"    # pasta onde os vídeos serão salvos
FORMATO         = "best"            # melhor qualidade disponível

# ── Helpers ──────────────────────────────────────────────────────────────────

def ler_links(caminho: str) -> list[str]:
    """Lê o arquivo de links e retorna uma lista de URLs válidas."""
    if not os.path.exists(caminho):
        print(f"❌ Arquivo '{caminho}' não encontrado.")
        print(f"   Crie o arquivo e adicione uma URL do TikTok por linha.")
        sys.exit(1)

    links = []
    with open(caminho, "r", encoding="utf-8") as f:
        for num, linha in enumerate(f, start=1):
            url = linha.strip()
            if not url or url.startswith("#"):   # ignora vazias e comentários
                continue
            if "tiktok.com" not in url:
                print(f"⚠️  Linha {num}: URL ignorada (não parece ser do TikTok): {url}")
                continue
            links.append(url)

    return links


def progresso(d: dict) -> None:
    """Callback para exibir o progresso do download."""
    if d["status"] == "downloading":
        pct        = d.get("_percent_str", "?%").strip()
        velocidade = d.get("_speed_str", "?").strip()
        eta        = d.get("_eta_str", "?").strip()
        print(f"\r   ⬇  {pct}  |  {velocidade}  |  ETA {eta}   ", end="", flush=True)
    elif d["status"] == "finished":
        print()   # quebra a linha após o download


def baixar(url: str, indice: int, total: int) -> bool:
    """Faz o download de uma única URL. Retorna True se bem-sucedido."""
    print(f"\n[{indice}/{total}] {url}")

    opcoes = {
        "format":           FORMATO,
        "outtmpl":          os.path.join(PASTA_SAIDA, "%(title)s.%(ext)s"),
        "progress_hooks":   [progresso],
        "quiet":            True,
        "no_warnings":      True,
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get("title", "sem título")
            print(f"   ✅ Baixado: {titulo}")
            return True
    except yt_dlp.utils.DownloadError as e:
        print(f"\n   ❌ Erro ao baixar: {e}")
        return False


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    arquivo = sys.argv[1] if len(sys.argv) > 1 else ARQUIVO_LINKS

    print("=" * 55)
    print("       TikTok Downloader — powered by yt-dlp")
    print("=" * 55)
    print(f"📄 Arquivo de links : {arquivo}")
    print(f"📁 Pasta de saída   : {PASTA_SAIDA}/")

    links = ler_links(arquivo)
    if not links:
        print("\n⚠️  Nenhuma URL válida encontrada no arquivo.")
        sys.exit(0)

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    total    = len(links)
    ok       = 0
    falhas   = []

    print(f"\n🎬 {total} vídeo(s) na fila...\n")
    inicio = time.time()

    for i, url in enumerate(links, start=1):
        sucesso = baixar(url, i, total)
        if sucesso:
            ok += 1
        else:
            falhas.append(url)
        time.sleep(1)   # pequena pausa entre downloads

    # ── Resumo ───────────────────────────────────────────────────────────────
    duracao = time.time() - inicio
    minutos, segundos = divmod(int(duracao), 60)

    print("\n" + "=" * 55)
    print(f"✅ Concluídos : {ok}/{total}")
    if falhas:
        print(f"❌ Falhas     : {len(falhas)}")
        for url in falhas:
            print(f"   • {url}")
    print(f"⏱  Tempo total: {minutos}m {segundos}s")
    print(f"📁 Vídeos salvos em: {os.path.abspath(PASTA_SAIDA)}/")
    print("=" * 55)


if __name__ == "__main__":
    main()
