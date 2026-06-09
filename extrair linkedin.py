import re
import sys
import time
import random
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from pathlib import Path
from urllib.parse import urlparse

from ddgs import DDGS

# =========================================================
# CONFIG
# =========================================================

if getattr(sys, "frozen", False):
    PASTA = Path(sys.executable).resolve().parent
else:
    PASTA = Path(__file__).resolve().parent

ARQUIVO_SAIDA = "linkedin.txt"

# =========================================================
# CONTROLE - OTIMIZADO PARA VELOCIDADE
# =========================================================

MAX_LINKS = 400
MAX_RESULTADOS = 50  # Aumentado para obter mais resultados por query

PAUSA_MIN = 0.5  # Reduzido drasticamente (era 2.0)
PAUSA_MAX = 1.5  # Reduzido drasticamente (era 5.0)

MAX_RETRY = 2  # Reduzido retries
PAUSA_RETRY = 3  # Espera menor entre retries

# APENAS BING E YANDEX (removido duckduckgo)
BACKENDS = ["bing",] #"yandex"

# =========================================================
# TERMOS (mantido igual)
# =========================================================

TERMOS = [

    # SALVADOR (FOCO PRINCIPAL)
    "engenheiro civil salvador",
    "engenheiro eletricista salvador",
    "engenheiro mecanico salvador",
    "engenheiro seguranca trabalho salvador",
    "arquiteto salvador",
    "gerente obras salvador",
    "coordenador obras salvador",
    "gerente manutencao salvador",
    "coordenador manutencao salvador",
    "facilities salvador",
    "gerente facilities salvador",
    "diretor engenharia salvador",
    "diretor operacional salvador",
    "gerente engenharia salvador",
    "gerente infraestrutura salvador",
    "comprador construtora salvador",
    "gerente compras salvador",
    "rh construtora salvador",
    "gerente projetos salvador",
    "coordenador projetos salvador",
    "responsavel tecnico salvador",
    "sindico profissional salvador",

    # EMPRESAS SALVADOR / BAHIA
    "construtora salvador",
    "empresa engenharia salvador",
    "empresa manutencao predial salvador",
    "empresa climatizacao salvador",
    "empresa eletrica salvador",
    "incorporadora salvador",
    "construtora bahia",
    "empresa facilities bahia",

    # SÃO PAULO
    "engenheiro civil sao paulo",
    "engenheiro eletricista sao paulo",
    "gerente manutencao sao paulo",
    "gerente engenharia sao paulo",
    "gerente facilities sao paulo",
    "diretor engenharia sao paulo",
    "construtora sao paulo",
    "empresa manutencao predial sao paulo",

    # ESPÍRITO SANTO
    "engenheiro civil espirito santo",
    "engenheiro eletricista espirito santo",
    "gerente manutencao espirito santo",
    "gerente engenharia espirito santo",
    "gerente facilities espirito santo",
    "diretor engenharia espirito santo",
    "construtora espirito santo",
    "empresa manutencao predial espirito santo",

    # BUSCA NACIONAL
    "engenharia brasil",
    "construcao civil brasil",
    "construtora brasil",
    "manutencao predial brasil",
    "facilities brasil",
    "climatizacao brasil",
    "hvac brasil",
    "infraestrutura brasil"
]

EXTRAS = [
    "linkedin",
    "perfil",
    "profissional",
    "trabalho",
    "vaga",
    "contratar",
]

# =========================================================
# REGEX (mantido igual)
# =========================================================

LINKEDIN_REGEX = re.compile(
    r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?",
    re.IGNORECASE
)

# =========================================================
# FUNÇÕES (mantidas, apenas buscar() otimizado)
# =========================================================

def limpar_link(url):
    url = str(url or "").strip()
    match = LINKEDIN_REGEX.search(url)
    if not match:
        return None
    url = match.group(0)
    url = url.split("?")[0].split("#")[0].rstrip("/")
    return url


def eh_linkedin(url):
    dominio = urlparse(url).netloc.lower()
    return dominio in ("linkedin.com", "www.linkedin.com")


def linkedin_util(url):
    if not eh_linkedin(url):
        return False
    path = urlparse(url).path.strip("/").lower()
    if not path or not path.startswith("in/"):
        return False
    perfil = path.replace("in/", "").split("/")[0]
    bloqueados = {
        "pub", "in", "post", "feed", "jobs", "messaging", "notifications",
        "learning", "learning/", "business", "advertising", "marketing",
        "help", "about", "legal", "terms", "privacy", "cookie",
        "basket", "fav", "u", "checkpoint", "login", "reg", "pie", "crv",
    }
    if perfil in bloqueados:
        return False
    if len(perfil) < 3:
        return False
    if perfil.count(".") > 2:
        return False
    if perfil.startswith("-") or perfil.endswith("-"):
        return False
    return True


def gerar_consultas():
    consultas = []
    for termo in TERMOS:
        base = [
            f'site:linkedin.com/in/ "{termo}"',
            f'site:linkedin.com/in/ "{termo}" salvador',
            f'site:linkedin.com/in/ "{termo}" bahia',
        ]
        consultas.extend(base)
        for extra in EXTRAS:
            consultas.extend([
                f'site:linkedin.com/in/ "{termo}" "{extra}"',
                f'intitle:"{extra}" site:linkedin.com/in/ "{termo}"',
            ])
    consultas = list(set(consultas))
    random.shuffle(consultas)
    return consultas


def carregar_existentes():
    caminho = PASTA / ARQUIVO_SAIDA
    if not caminho.exists():
        return set()
    with open(caminho, "r", encoding="utf-8") as f:
        return {linha.strip() for linha in f if linha.strip()}


def salvar_incremental(link):
    caminho = PASTA / ARQUIVO_SAIDA
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(link + "\n")


def buscar_uma_consulta(consulta, backend, vistos, MAX_LINKS):
    """Busca individual para paralelização opcional"""
    resultados = []
    sucesso = False
    
    for tentativa in range(MAX_RETRY):
        try:
            with DDGS(timeout=20) as ddgs:
                busca = ddgs.text(
                    consulta,
                    region="br-pt",
                    safesearch="off",
                    max_results=MAX_RESULTADOS,
                    backend=backend,
                )
                resultados = list(busca or [])
            sucesso = True
            break
        except Exception as e:
            if tentativa < MAX_RETRY - 1:
                time.sleep(PAUSA_RETRY)
            continue
    
    if not sucesso:
        return [], vistos
    
    novos_links = []
    for item in resultados:
        href = limpar_link(item.get("href", ""))
        if not href or not linkedin_util(href) or href in vistos:
            continue
        vistos.add(href)
        novos_links.append(href)
    
    return novos_links, vistos


def buscar():
    vistos = carregar_existentes()
    total = len(vistos)
    
    print(f"\nLINKS EXISTENTES: {total}")
    
    consultas = gerar_consultas()
    
    for consulta in consultas:
        if total >= MAX_LINKS:
            break
        
        backend = random.choice(BACKENDS)
        
        print(f"\nCONSULTA: {consulta[:60]}... | BACKEND: {backend} | TOTAL: {total}/{MAX_LINKS}")
        
        time.sleep(random.uniform(PAUSA_MIN, PAUSA_MAX))
        
        novos_links, vistos = buscar_uma_consulta(consulta, backend, vistos, MAX_LINKS)
        
        for href in novos_links:
            if total >= MAX_LINKS:
                break
            salvar_incremental(href)
            total += 1
            print(f"[{total}] {href}")
    
    return total


# =========================================================
# MAIN
# =========================================================

def main():
    print("\n========================================")
    print("EXTRATOR LINKEDIN TURBO - BING+YANDEX")
    print("========================================")
    print(f"\nMETA: {MAX_LINKS} PERFIS")
    print(f"BACKENDS: {BACKENDS}")
    print(f"Pausa: {PAUSA_MIN}-{PAUSA_MAX}s")
    
    try:
        inicio = time.time()
        total = buscar()
        fim = time.time()
        
        print("\n========================================")
        print("FINALIZADO")
        print("========================================")
        print(f"TOTAL: {total}")
        print(f"TEMPO: {round(fim - inicio, 2)}s")
        print(f"MÉDIA: {round((fim-inicio)/max(total,1), 2)}s/link")
        print(f"ARQUIVO: {PASTA / ARQUIVO_SAIDA}")
        
    except KeyboardInterrupt:
        print("\nENCERRADO MANUALMENTE")
    except Exception:
        print("\nERRO GERAL")
        traceback.print_exc()


if __name__ == "__main__":
    main()
