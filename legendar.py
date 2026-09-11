#!/usr/bin/env python3
"""
Gerador de Legendas Traduzidas
Baixa um vídeo (link) ou usa um arquivo local, transcreve o áudio e gera
um arquivo .srt traduzido para o idioma escolhido (padrão: português).

Dependências:
    pip install yt-dlp faster-whisper deep-translator imageio_ffmpeg

Uso:
    python legendar.py <link_ou_caminho_do_video> [idioma_destino]

Exemplos:
    python legendar.py https://www.facebook.com/share/v/xxxxx/
    python legendar.py C:\\Users\\Ricardo\\Videos\\meuvideo.mp4
    python legendar.py https://www.tiktok.com/@user/video/123 en
"""

import sys
import os

# Garante suporte a UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import yt_dlp
    import imageio_ffmpeg
    from faster_whisper import WhisperModel
    from deep_translator import MyMemoryTranslator
except ImportError as e:
    print(f"❌ Dependência faltando: {e}")
    print("   Instale com: pip install yt-dlp faster-whisper deep-translator imageio_ffmpeg")
    sys.exit(1)


# ── Configurações ────────────────────────────────────────────────────────────

PASTA_SAIDA   = "downloads"   # pasta onde vídeo e legenda são salvos
MODELO_WHISPER = "small"      # tiny, base, small, medium, large (maior = mais preciso e mais lento)
IDIOMA_PADRAO  = "pt"         # idioma de destino da tradução

# MyMemory exige códigos completos (idioma-REGIÃO). Mapeia os códigos curtos
# que o faster-whisper detecta/recebe para o formato que o MyMemory entende.
MAPA_IDIOMAS = {
    "pt": "pt-BR", "en": "en-GB", "es": "es-ES", "fr": "fr-FR", "de": "de-DE",
    "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "zh": "zh-CN", "ru": "ru-RU",
    "ar": "ar-SA", "hi": "hi-IN", "nl": "nl-NL", "pl": "pl-PL", "tr": "tr-TR",
    "sv": "sv-SE", "id": "id-ID", "vi": "vi-VN", "th": "th-TH", "uk": "uk-UA",
}


def codigo_mymemory(codigo: str) -> str:
    """Converte um código curto de idioma (ex: 'en') para o formato do MyMemory."""
    return MAPA_IDIOMAS.get(codigo, codigo)


# ── Helpers ──────────────────────────────────────────────────────────────────

def baixar_video(url: str) -> str:
    """Baixa o vídeo de qualquer site suportado pelo yt-dlp e retorna o caminho do arquivo."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    opcoes = {
        "outtmpl":        os.path.join(PASTA_SAIDA, "%(id)s.%(ext)s"),
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "format":         "best",
        "quiet":          True,
        "no_warnings":    True,
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def formatar_srt_timestamp(segundos: float) -> str:
    """Converte segundos (float) para o formato HH:MM:SS,mmm do .srt"""
    ms_totais = round(segundos * 1000)
    horas, resto = divmod(ms_totais, 3_600_000)
    minutos, resto = divmod(resto, 60_000)
    segs, ms = divmod(resto, 1000)
    return f"{horas:02d}:{minutos:02d}:{segs:02d},{ms:03d}"


def transcrever(caminho_video: str, modelo: str):
    """Transcreve o áudio do vídeo e retorna a lista de segmentos com timestamps."""
    print(f"🎙️  Transcrevendo áudio (modelo '{modelo}')...")
    model = WhisperModel(modelo, device="cpu", compute_type="int8")
    segmentos, info = model.transcribe(caminho_video, beam_size=5)
    print(f"🌐 Idioma detectado: {info.language} ({info.language_probability:.0%} de confiança)")
    return list(segmentos), info.language


def traduzir_segmentos(segmentos, idioma_origem: str, idioma_destino: str):
    """Traduz o texto de cada segmento para o idioma de destino."""
    if idioma_origem == idioma_destino:
        print("ℹ️  Idioma de origem igual ao de destino — pulando tradução.")
        return [(s.start, s.end, s.text.strip()) for s in segmentos]

    print(f"🌍 Traduzindo {len(segmentos)} trecho(s) para '{idioma_destino}'...")
    tradutor = MyMemoryTranslator(
        source=codigo_mymemory(idioma_origem),
        target=codigo_mymemory(idioma_destino),
    )
    resultado = []
    for i, s in enumerate(segmentos, start=1):
        texto = s.text.strip()
        try:
            traduzido = tradutor.translate(texto) if texto else ""
        except Exception as e:
            print(f"   ⚠️  Falha ao traduzir trecho {i}: {e}")
            traduzido = texto
        resultado.append((s.start, s.end, traduzido))
        print(f"\r   {i}/{len(segmentos)}", end="", flush=True)
    print()
    return resultado


def gerar_srt(caminho_saida: str, segmentos_traduzidos) -> None:
    """Escreve os segmentos traduzidos em um arquivo .srt."""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        for i, (inicio, fim, texto) in enumerate(segmentos_traduzidos, start=1):
            f.write(f"{i}\n")
            f.write(f"{formatar_srt_timestamp(inicio)} --> {formatar_srt_timestamp(fim)}\n")
            f.write(f"{texto}\n\n")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python legendar.py <link_ou_caminho_do_video> [idioma_destino]")
        print("Exemplo: python legendar.py https://www.tiktok.com/@user/video/123 pt")
        sys.exit(1)

    entrada        = sys.argv[1]
    idioma_destino = sys.argv[2] if len(sys.argv) > 2 else IDIOMA_PADRAO

    print("=" * 55)
    print("       Gerador de Legendas Traduzidas")
    print("=" * 55)

    if entrada.startswith("http://") or entrada.startswith("https://"):
        print(f"⬇️  Baixando vídeo: {entrada}")
        caminho_video = baixar_video(entrada)
        print(f"✅ Vídeo salvo em: {caminho_video}")
    else:
        caminho_video = entrada
        if not os.path.exists(caminho_video):
            print(f"❌ Arquivo não encontrado: {caminho_video}")
            sys.exit(1)

    segmentos, idioma_origem = transcrever(caminho_video, MODELO_WHISPER)
    if not segmentos:
        print("⚠️  Nenhuma fala detectada no vídeo.")
        sys.exit(0)

    traduzidos = traduzir_segmentos(segmentos, idioma_origem, idioma_destino)

    base, _ = os.path.splitext(caminho_video)
    caminho_srt = f"{base}.{idioma_destino}.srt"
    gerar_srt(caminho_srt, traduzidos)

    print("\n" + "=" * 55)
    print(f"✅ Legenda gerada: {caminho_srt}")
    print("=" * 55)


if __name__ == "__main__":
    main()
