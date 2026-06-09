from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random
import time
import os
import json
from datetime import datetime
import re

# =========================================================
# CONFIGURAÇÕES
# =========================================================

login = "lucasdsantoss2003@gmail.com"
senha = "33832216"

# Limite de perfis por execução (0 = sem limite) - ALTERADO PARA 100
LIMITE_DIARIO = 300

# Arquivo de progresso
ARQUIVO_PROGRESSO = "progresso_linkedin.json"
ARQUIVO_LOG = "log_linkedin.txt"

# =========================================================
# LISTA DE PERFIS
# =========================================================

perfis_texto = """
https://www.linkedin.com/in/caique-prado-17261022
https://www.linkedin.com/in/eduardo-krueger-2a159047
https://www.linkedin.com/in/miguel-serra-68ba2a46
https://www.linkedin.com/in/airton-ferreira-humber-b9582b93
https://www.linkedin.com/in/jvazevedo
https://www.linkedin.com/in/gustavo-marco-8b2b50138
https://www.linkedin.com/in/thiago-andress-054a17108
https://www.linkedin.com/in/versonimowes
https://www.linkedin.com/in/andr
https://www.linkedin.com/in/engetask-engenharia-engetask-b7a320291
https://www.linkedin.com/in/luiza-sousa
https://www.linkedin.com/in/erico-evaristo-de-oliveira-7ba8b922
https://www.linkedin.com/in/engemat-engenharia-651a6ba5
https://www.linkedin.com/in/eguinaldo-marques-3aa38463
https://www.linkedin.com/in/3ca-imobili
https://www.linkedin.com/in/gilmara-lima-120434146
https://www.linkedin.com/in/victoria-chong-643563163
https://www.linkedin.com/in/ivanluz
https://www.linkedin.com/in/luciene-ribeiro-de-sousa-20779414b
https://www.linkedin.com/in/edilson-engelux-muniz-de-oliveira-b8763347
https://www.linkedin.com/in/sarah-dourado-06b07a145
https://www.linkedin.com/in/mutti-santana-3b742418a
https://www.linkedin.com/in/marcelo-araujo-577201117
https://www.linkedin.com/in/stephanie-brasil-jones-b35418151
https://www.linkedin.com/in/paulo-vaz-8b106392
https://www.linkedin.com/in/pedro-magalh
https://www.linkedin.com/in/jose-luiz-goes-98012659
https://www.linkedin.com/in/orlando-lemos-71bbbba1
https://www.linkedin.com/in/rm-construtora-173876a9
https://www.linkedin.com/in/construtora-jl
https://www.linkedin.com/in/realiza-construtora-campos-dos-goytacazes-596a64208
https://www.linkedin.com/in/construtora-construtec-84bb10138
https://www.linkedin.com/in/zelina-e-silva-b00b4672
https://www.linkedin.com/in/guiberto-vital-59255743
https://www.linkedin.com/in/israel-barros-308b161b0
https://www.linkedin.com/in/renata-nascimento-caetano-416073223
https://www.linkedin.com/in/luciano-duarte-a65062166
https://www.linkedin.com/in/jos
https://www.linkedin.com/in/viviane-oliveira-444463181
https://www.linkedin.com/in/valentina-lopes-b32424252
https://www.linkedin.com/in/vanize-oliveira-117454204
https://www.linkedin.com/in/claudio-leite
https://www.linkedin.com/in/geisa-siqueira-76a2bb11a
https://www.linkedin.com/in/nicolas-vanelli-costa-6b36865a
https://www.linkedin.com/in/leandro-ferreira-67720496
https://www.linkedin.com/in/arivaldo-ramos-998a3910a
https://www.linkedin.com/in/bruno-silva-corvo-15325457
https://www.linkedin.com/in/daniela-de-almeida-malaquias-915574b7
https://www.linkedin.com/in/laurindo-vilas-boas-3211166a
https://www.linkedin.com/in/isabelle-paim-b266a32a9
https://www.linkedin.com/in/gustavoamoedoestevez987876669
https://www.linkedin.com/in/pedro-miguel-messeder-machado-036483127
https://www.linkedin.com/in/marcos-vinicius-21095b71
https://www.linkedin.com/in/jose-augusto-tiuba-1b921a1ba
https://www.linkedin.com/in/ananda-oliveira-432789b3
https://www.linkedin.com/in/henrique-henrique-97aa824b
https://www.linkedin.com/in/priscila-valente
https://www.linkedin.com/in/marc-waxman-braga-0681691b4
https://www.linkedin.com/in/kelvynlucas
https://www.linkedin.com/in/luiz-bahiana-23a5b2289
https://www.linkedin.com/in/alessandra-candida-de-almeida-pereira-549745230
https://www.linkedin.com/in/leticia-martimiano
https://www.linkedin.com/in/salvador-garc
https://www.linkedin.com/in/dom-gob-sv
https://www.linkedin.com/in/prubiosalvador
https://www.linkedin.com/in/salvador-trejo-b567059a
https://www.linkedin.com/in/salvadordiazperez
https://www.linkedin.com/in/douglas-salvador-853b2878
https://www.linkedin.com/in/salvador-carrillo-miani-a00585125
https://www.linkedin.com/in/salvador-zald
https://www.linkedin.com/in/salvadorbicudo
https://www.linkedin.com/in/alejandra-rios-21b7b556
https://www.linkedin.com/in/salvadorpascualbarranquero
https://www.linkedin.com/in/salvador-montes-de-oca-pua-129a6718a
https://www.linkedin.com/in/salvador-guerrero-garcia-55520549
https://www.linkedin.com/in/salvador-tom
https://www.linkedin.com/in/salvador-burelo-032810235
https://www.linkedin.com/in/echauvin
https://www.linkedin.com/in/thomas-seck-0a2a68a
https://www.linkedin.com/in/benjamin-freeman-3112a520
https://www.linkedin.com/in/natalia-wenger-mba-pmp-ccp-98bab961
https://www.linkedin.com/in/larisaescalle
https://www.linkedin.com/in/aparnaramani
https://www.linkedin.com/in/sssvasan
https://www.linkedin.com/in/alessandro-moreira-nunes-00948276
https://www.linkedin.com/in/allen-liao
https://www.linkedin.com/in/nicholasathomas
https://www.linkedin.com/in/paulbahlstrom
https://www.linkedin.com/in/kenneth-kasuba
https://www.linkedin.com/in/nicholas-obuekwe
https://www.linkedin.com/in/dennismlaw
https://www.linkedin.com/in/jamille-santos
https://www.linkedin.com/in/sandeepa
https://www.linkedin.com/in/christophermartinez22
https://www.linkedin.com/in/ojsanchez
https://www.linkedin.com/in/sarachristensen
https://www.linkedin.com/in/charles-webb-b7202a2a
https://www.linkedin.com/in/mike-yee-716168200
https://www.linkedin.com/in/corina-salvador
https://www.linkedin.com/in/rajesh-jha-90010b4
https://www.linkedin.com/in/cassidy-mccahill-31b988411
https://www.linkedin.com/in/rodrigodutragarcia
https://www.linkedin.com/in/philip-rackliffe-8426762
https://www.linkedin.com/in/nadine-lee-64b210157
https://www.linkedin.com/in/higor-corr
https://www.linkedin.com/in/isabela-cristina-25a52b54
https://www.linkedin.com/in/lorenzzo-bafile-32a8382
https://www.linkedin.com/in/kenmatharu
https://www.linkedin.com/in/julio-da-silva-3b7467
https://www.linkedin.com/in/farquharsona
https://www.linkedin.com/in/safian-alam
https://www.linkedin.com/in/ryan-lindner-4b22a83b
https://www.linkedin.com/in/mason-clarke-186ba01bb
https://www.linkedin.com/in/iharnoor
https://www.linkedin.com/in/salframondi
https://www.linkedin.com/in/craig-stephen-slavtcheff-7115455
https://www.linkedin.com/in/barqub
https://www.linkedin.com/in/maria-rodriguez-66466852
https://www.linkedin.com/in/euclides-dos-santos-2a1b72295
https://www.linkedin.com/in/pbailis
https://www.linkedin.com/in/natalie-torres-04a491230
https://www.linkedin.com/in/amarinder-grewal
https://www.linkedin.com/in/behnam-zamanzad-ghavidel-9b5750121
https://www.linkedin.com/in/amanda-maria-b49115232
https://www.linkedin.com/in/lucasevangelistacarvalho
https://www.linkedin.com/in/salvador-landeros
https://www.linkedin.com/in/emmanuel-sanchez-0406aa408
https://www.linkedin.com/in/gmelotechsales
https://www.linkedin.com/in/robson-gomes-dias-9235ab212
https://www.linkedin.com/in/wfsolu
https://www.linkedin.com/in/jpauloabp
https://www.linkedin.com/in/rafael-rosa-sanches-a09383123
https://www.linkedin.com/in/tarcisio-pereira-58a63115
https://www.linkedin.com/in/glauco-p-762100169
https://www.linkedin.com/in/vinicius-pereira-silva-531a58108
https://www.linkedin.com/in/ricardo-machado-a7529080
https://www.linkedin.com/in/geson-nascimento-862b369b
https://www.linkedin.com/in/amanda-araujo-a1039214b
https://www.linkedin.com/in/pedro-milani-mattos-188494182
https://www.linkedin.com/in/prof-rodolfo-souza-9456bb2a2
https://www.linkedin.com/in/group-balladares-464692150
https://www.linkedin.com/in/ricardo-da-silva-ribeiro-34074514a
https://www.linkedin.com/in/patrim
https://www.linkedin.com/in/geraldo-rodrigues-a92b5290
https://www.linkedin.com/in/gelfran-santos-02a5a4191
https://www.linkedin.com/in/ana-carolina-rocha-2021a
https://www.linkedin.com/in/paulo-filadelfo-913a3886
https://www.linkedin.com/in/glaysson-cotta-334253186
https://www.linkedin.com/in/rodrigo-messias-oliveira-b8104689
https://www.linkedin.com/in/jefersonsouzasantos
https://www.linkedin.com/in/peres-engenheiro-de-seguran
https://www.linkedin.com/in/edvaldo-dos-santos-sabino-07794036
https://www.linkedin.com/in/douglas-barros-peritojudicial
https://www.linkedin.com/in/fernando-ara
https://www.linkedin.com/in/gustavo-gomes-de-lima-37a636135
https://www.linkedin.com/in/felipe-cotrim-169187b0
https://www.linkedin.com/in/arqmigueldefreitas
https://www.linkedin.com/in/gilmar-freire-375206116
https://www.linkedin.com/in/brenda-brito-08a525104
https://www.linkedin.com/in/samanta-ribeiro-27450248
https://www.linkedin.com/in/lorenzohpacussich
https://www.linkedin.com/in/lorena-valverde-95027189
https://www.linkedin.com/in/gabriel-victor-nunes-968037289
https://www.linkedin.com/in/arquitetoalexg
https://www.linkedin.com/in/rodrigo-sampaio-22ba33197
https://www.linkedin.com/in/isa-maciel-6a33a4a0
https://www.linkedin.com/in/dener-martins-b897131bb
https://www.linkedin.com/in/hugo-ribeiro-aa7246114
https://www.linkedin.com/in/milena-dygas-03407020b
https://www.linkedin.com/in/rodolfo-esteves-21989531
https://www.linkedin.com/in/tiago-dallegrave-23b28194
https://www.linkedin.com/in/danilo-silva-330402102
https://www.linkedin.com/in/rivasc
https://www.linkedin.com/in/luis-orellana-39180826
https://www.linkedin.com/in/ernesto-paramo
https://www.linkedin.com/in/anthonyrossopspro
https://www.linkedin.com/in/jason-clement-7595974
https://www.linkedin.com/in/michael-cheney-86031112
https://www.linkedin.com/in/jordan-s-3696b0184
https://www.linkedin.com/in/brianpoveromo
https://www.linkedin.com/in/charlie-spencer-b4987875
https://www.linkedin.com/in/heath-pramberger-28007a209
https://www.linkedin.com/in/jameshfitzgerald
https://www.linkedin.com/in/daniel-morais-350442124
https://www.linkedin.com/in/almir-almeida-alencar-0115a225b
https://www.linkedin.com/in/joaomdmoura
https://www.linkedin.com/in/jim-hurtado-7a8a372a
https://www.linkedin.com/in/omarossama22
https://www.linkedin.com/in/roberto-salvi
https://www.linkedin.com/in/jose-salvador-bb9925191
https://www.linkedin.com/in/brenno-bezerra-78129932
https://www.linkedin.com/in/alessandro-salvador-47324824
https://www.linkedin.com/in/alexandre-de-angelis-8996b262
https://www.linkedin.com/in/vitoria-araujocampos
https://www.linkedin.com/in/patricia-salvador-5aa281115
https://www.linkedin.com/in/tekes
https://www.linkedin.com/in/jose-nilson-14b2071b
https://www.linkedin.com/in/priscila-coutinho-s-fonseca-0263a731
https://www.linkedin.com/in/carlos-henrique-santana-lima-a42347147
https://www.linkedin.com/in/alissandro-santos-47a0a8210
https://www.linkedin.com/in/monica-oliveira-compras
https://www.linkedin.com/in/jacquelineundadelgado
https://www.linkedin.com/in/gabriel-hadi-ba31a7221
https://www.linkedin.com/in/man-lun-aa3070161
https://www.linkedin.com/in/janice-almeida-2846b3347
https://www.linkedin.com/in/ingoelfering
https://www.linkedin.com/in/martinstumpe
https://www.linkedin.com/in/vaibhav-taneja-7297003
https://www.linkedin.com/in/tunaungmyint
https://www.linkedin.com/in/judith-ibarra-bianchetta-pe-cfm-env-sp-2396718
https://www.linkedin.com/in/sharpourreza
https://www.linkedin.com/in/emily-mango-22941611
https://www.linkedin.com/in/farhanilhamdi1
https://www.linkedin.com/in/akhmad-mega-saputra-2a6463296
https://www.linkedin.com/in/lixy-alzamora-54331159
https://www.linkedin.com/in/berglindbaldursdottir
https://www.linkedin.com/in/aline-borba-07b96529
https://www.linkedin.com/in/aptojal
https://www.linkedin.com/in/sandy-n-a-154896b7
https://www.linkedin.com/in/matthew-j-gay
https://www.linkedin.com/in/crystaldthom
https://www.linkedin.com/in/leon-threets-jr-aba193b
https://www.linkedin.com/in/conrado-zapanta
https://www.linkedin.com/in/mw-engenharia-e-constru
https://www.linkedin.com/in/edy-silva-939b4ba3
https://www.linkedin.com/in/daniel-gomes-a4854699
https://www.linkedin.com/in/ismael-rego-31970b205
https://www.linkedin.com/in/silvio-arruda-592a1375
https://www.linkedin.com/in/almeida-sapata-engenharia-20917819b
https://www.linkedin.com/in/leonardo-sampaio-7202871a5
https://www.linkedin.com/in/alan1985
https://www.linkedin.com/in/leonardo-mariano-0a5b861a5
https://www.linkedin.com/in/samuel-dos-santos-silva-014211156
https://www.linkedin.com/in/ana-maria-barbosa-93a008180
https://www.linkedin.com/in/samuel-pereira-9971b74b
https://www.linkedin.com/in/joelmos-pereira-da-silva-27ba5963
https://www.linkedin.com/in/gabriel-carvalho-57198131
https://www.linkedin.com/in/saviolimaesilva
https://www.linkedin.com/in/juan-salvador-88389a202
https://www.linkedin.com/in/adamharrisonguild
https://www.linkedin.com/in/andrewdfeldman
https://www.linkedin.com/in/mattgray1
https://www.linkedin.com/in/sundarpichai
https://www.linkedin.com/in/jenhsunhuang
https://www.linkedin.com/in/satyanadella
https://www.linkedin.com/in/bersin
https://www.linkedin.com/in/marciosalvador2016
https://www.linkedin.com/in/frank-paolino
https://www.linkedin.com/in/hasan-mohamed-abdul-wahab
https://www.linkedin.com/in/tony-mormino
https://www.linkedin.com/in/mohammedrehansyed
https://www.linkedin.com/in/pedro-de-la-paz-71a3ab236
https://www.linkedin.com/in/davidcwilkins
https://www.linkedin.com/in/hunter-m-64296a33
https://www.linkedin.com/in/kylebudde
https://www.linkedin.com/in/merrittscott
https://www.linkedin.com/in/daveiba
https://www.linkedin.com/in/molson1
https://www.linkedin.com/in/tregovich
https://www.linkedin.com/in/stacy-gualandi-1050516
https://www.linkedin.com/in/ivan-leon-hernandez-nieves-01832131

"""

# =========================================================
# MENSAGEM CORPORATIVA
# =========================================================

mensagem = """
Prezados,

Gostaria de apresentar a Construtec Engenharia, empresa especializada em serviços de instalações técnicas e serviços civis, oferecendo soluções completas com qualidade, segurança e responsabilidade técnica.

 
"""

# =========================================================
# FUNÇÕES DE LOG E PROGRESSO
# =========================================================

def log(msg, nivel="INFO"):
    """Escreve log no arquivo e no console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] [{nivel}] {msg}\n"
    print(linha.strip())
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linha)

def carregar_progresso():
    """Carrega progresso salvo"""
    if os.path.exists(ARQUIVO_PROGRESSO):
        try:
            with open(ARQUIVO_PROGRESSO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"processados": [], "erros": [], "total_processados": 0}
    return {"processados": [], "erros": [], "total_processados": 0}

def salvar_progresso(progresso):
    """Salva progresso"""
    with open(ARQUIVO_PROGRESSO, "w", encoding="utf-8") as f:
        json.dump(progresso, f, indent=2, ensure_ascii=False)

def limpar_perfis_duplicados(perfis):
    """Remove duplicatas mantendo ordem"""
    vistos = set()
    unico = []
    for p in perfis:
        limpo = p.strip().strip("[]()")
        if limpo and limpo not in vistos:
            vistos.add(limpo)
            unico.append(limpo)
    return unico

# =========================================================
# CONFIGURAÇÃO DO CHROME (ANTI-DETECÇÃO AVANÇADA)
# =========================================================

def criar_driver():
    """Cria o driver com opções anti-detecção"""
    options = webdriver.ChromeOptions()
    
    # Anti-detecção básica
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # User-Agent aleatório
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    # Outras opções
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    # Remove webdriver
    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        })
        Object.defineProperty(navigator, 'languages', {
            get: () => ['pt-BR', 'pt', 'en']
        })
    """)
    
    driver.maximize_window()
    return driver

# =========================================================
# LOGIN NO LINKEDIN
# =========================================================

def fazer_login(driver, login, senha):
    """Realiza login no LinkedIn"""
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 30)
    
    try:
        log("Abrindo página de login...")
        
        email_input = wait.until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        email_input.clear()
        time.sleep(random.uniform(0.5, 1.5))
        email_input.send_keys(login)
        
        senha_input = wait.until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        senha_input.clear()
        time.sleep(random.uniform(0.5, 1.5))
        senha_input.send_keys(senha)
        
        time.sleep(random.uniform(1, 2))
        
        botao_login = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        botao_login.click()
        
        log("Login enviado, aguardando...")
        time.sleep(random.uniform(8, 12))
        
        if "feed" in driver.current_url or "linkedin.com/in/" in driver.current_url:
            log("LOGIN EFETUADO COM SUCESSO", "SUCESSO")
            return True
        else:
            log("LinkedIn pode ter pedido validação (CAPTCHA/2FA)", "AVISO")
            log(f"URL atual: {driver.current_url}")
            input("Após validar, pressione ENTER para continuar...")
            return True
            
    except TimeoutException:
        log("Não encontrou tela de login - screenshot salvo", "ERRO")
        driver.save_screenshot("erro_login.png")
        return False
    except Exception as e:
        log(f"Erro no login: {e}", "ERRO")
        return False

# =========================================================
# PROCESSAR PERFIL
# =========================================================

def processar_perfil(driver, wait, perfil, mensagem, progresso):
    """Processa um único perfil"""
    
    driver.get(perfil)
    time.sleep(random.uniform(5, 9))
    
    resultado = {
        "perfil": perfil,
        "conectado": False,
        "mensagem_enviada": False,
        "erro": None
    }
    
    # Verificar se já está conectado/seguindo
    ja_conectado = False
    try:
        botoes = driver.find_elements(By.TAG_NAME, "button")
        for botao in botoes:
            texto = botao.text.strip().lower()
            if "já conectado" in texto or "conexão" in texto or "seguindo" in texto:
                log("Já conectado/seguindo este perfil - apenas enviando mensagem", "AVISO")
                ja_conectado = True
                break
    except:
        pass
    
    # Se já está conectado, pular para enviar mensagem diretamente
    conectado = False
    if not ja_conectado:
        try:
            botoes = driver.find_elements(By.TAG_NAME, "button")
            for botao in botoes:
                try:
                    texto = botao.text.strip().lower()
                    
                    if "conectar" in texto:
                        driver.execute_script("arguments[0].click();", botao)
                        log("Botão CONECTAR clicado", "SUCESSO")
                        conectado = True
                        time.sleep(random.uniform(2, 4))
                        break
                        
                    elif "seguir" in texto:
                        driver.execute_script("arguments[0].click();", botao)
                        log("Botão SEGUIR clicado", "SUCESSO")
                        conectado = True
                        time.sleep(random.uniform(2, 4))
                        break
                        
                except:
                    continue
            
            if not conectado:
                log("Nenhum botão conectar/seguir encontrado", "AVISO")
                
        except Exception as e:
            log(f"Erro ao localizar botões: {e}", "ERRO")
            resultado["erro"] = str(e)
    else:
        # Já está conectado, considerar como conectado para enviar mensagem
        conectado = True
        resultado["ja_conectado"] = True
    
    # Adicionar nota (seja para novos ou já conectados)
    if conectado:
        try:
            time.sleep(random.uniform(2, 5))
            
            adicionar_nota = driver.find_elements(
                By.XPATH, "//button[contains(., 'Adicionar nota')]"
            )
            
            if adicionar_nota:
                adicionar_nota[0].click()
                log("Abrindo campo de mensagem", "INFO")
                time.sleep(3)
                
                textarea = wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "textarea"))
                )
                textarea.clear()
                textarea.send_keys(mensagem)
                time.sleep(2)
                
                enviar = driver.find_element(
                    By.XPATH, "//button[contains(., 'Enviar')]"
                )
                enviar.click()
                
                log("Mensagem enviada com sucesso", "SUCESSO")
                resultado["mensagem_enviada"] = True
                resultado["conectado"] = True
                
            else:
                log("Perfil não permite adicionar nota", "AVISO")
                
        except Exception as e:
            log(f"Erro ao enviar mensagem: {e}", "ERRO")
            resultado["erro"] = str(e)
    
    return resultado

# =========================================================
# MAIN
# =========================================================

def main():
    log("=" * 60)
    log("INICIANDO SCRIPT LINKEDIN - CONECTAR + MENSAGEM")
    log("=" * 60)
    
    # Carregar perfis
    perfis = limpar_perfis_duplicados([
        linha.strip() 
        for linha in perfis_texto.splitlines() 
        if linha.strip()
    ])
    
    log(f"Total de perfis únicos: {len(perfis)}")
    
    # Carregar progresso
    progresso = carregar_progresso()
    processados = set(progresso["processados"])
    erros = progresso.get("erros", [])
    
    perfis_pendentes = [p for p in perfis if p not in processados]
    log(f"Perfis já processados: {len(processados)}")
    log(f"Perfis pendentes: {len(perfis_pendentes)}")
    
    if not perfis_pendentes:
        log("Todos os perfis já foram processados!", "SUCESSO")
        input("Pressione ENTER para fechar...")
        return
    
    # Criar driver
    driver = criar_driver()
    wait = WebDriverWait(driver, 30)
    
    try:
        # Login
        if not fazer_login(driver, login, senha):
            log("Falha no login. Encerrando.", "ERRO")
            return
        
        # Contadores
        contador = 0
        sucesso = 0
        falha = 0
        ja_conectado = 0
        
        # Loop perfis
        for i, perfil in enumerate(perfis_pendentes):
            contador += 1
            
            # Verificar limite diário
            if LIMITE_DIARIO > 0 and (progresso["total_processados"] + contador) > LIMITE_DIARIO:
                log(f"Limite diário de {LIMITE_DIARIO} alcançado. Parando.", "AVISO")
                break
            
            log(f"\n{'='*70}")
            log(f"PERFIL {progresso['total_processados'] + contador}/{len(perfis)}", "INFO")
            log(f"{perfil}")
            log(f"{'='*50}")
            
            try:
                resultado = processar_perfil(driver, wait, perfil, mensagem, progresso)
                
                if resultado.get("ja_conectado"):
                    ja_conectado += 1
                    processados.add(perfil)
                    # Ainda conta como sucesso se mensagem foi enviada
                    if resultado["mensagem_enviada"]:
                        sucesso += 1
                
                elif resultado["conectado"] and resultado["mensagem_enviada"]:
                    sucesso += 1
                    processados.add(perfil)
                
                else:
                    falha += 1
                    if not resultado.get("ja_conectado"):
                        erros.append({"perfil": perfil, "erro": resultado.get("erro", "desconhecido")})
                
                # Salvar progresso a cada 5 perfis
                if contador % 5 == 0:
                    progresso["processados"] = list(processados)
                    progresso["erros"] = erros
                    progresso["total_processados"] = progresso["total_processados"] + contador
                    salvar_progresso(progresso)
                
                # Delay humano
                pausa = random.randint(20, 45)
                log(f"Pausa operacional: {pausa}s")
                time.sleep(pausa)
                
            except Exception as e:
                falha += 1
                erros.append({"perfil": perfil, "erro": str(e)})
                log(f"Erro geral no perfil: {e}", "ERRO")
                driver.save_screenshot(f"erro_perfil_{contador}.png")
                
                # Pausa maior em caso de erro
                time.sleep(random.randint(10, 20))
        
        # Finalização
        log("\n" + "=" * 60)
        log("PROCESSO FINALIZADO", "SUCESSO")
        log("=" * 60)
        log(f"Total processados nesta execução: {contador}")
        log(f"Sucesso: {sucesso}")
        log(f"Já conectado (mensagem enviada): {ja_conectado}")
        log(f"Falhas: {falha}")
        log(f"Total acumulado: {progresso['total_processados'] + contador}")
        
        # Salvar progresso final
        progresso["processados"] = list(processados)
        progresso["erros"] = erros
        progresso["total_processados"] = progresso["total_processados"] + contador
        salvar_progresso(progresso)
        
    except KeyboardInterrupt:
        log("Interrupção pelo usuário", "AVISO")
    except Exception as e:
        log(f"Erro crítico: {e}", "ERRO")
        driver.save_screenshot("erro_crítico.png")
    finally:
        input("\nPressione ENTER para fechar...")
        driver.quit()
        log("Driver fechado. Script encerrado.")

if __name__ == "__main__":
    main()
