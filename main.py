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

# Limite de perfis por execução (0 = sem limite)
LIMITE_DIARIO = 50

# Arquivo de progresso
ARQUIVO_PROGRESSO = "progresso_linkedin.json"
ARQUIVO_LOG = "log_linkedin.txt"

# =========================================================
# LISTA DE PERFIS
# =========================================================

perfis_texto = """
https://br.linkedin.com/company/terral-construtora-ltda
https://br.linkedin.com/in/emisaelbraulio
https://br.linkedin.com/in/edilton-queiroz-souza-54625781
https://br.linkedin.com/in/izabelamauricio
https://br.linkedin.com/in/marcelo-bertolucio-barreto
https://br.linkedin.com/in/felipe-guanabara-12ba72b0
https://br.linkedin.com/in/anne-nascimento-40b58743
https://br.linkedin.com/company/g-oca-engenharia
https://br.linkedin.com/in/luan-ferrari-71b38416
https://br.linkedin.com/in/joaovictorbricidioarariba
https://br.linkedin.com/in/agois
https://www.linkedin.com/company/facilitasengenharia
https://br.linkedin.com/in/jessica-bailhao-0574a32b9
https://br.linkedin.com/in/costa-espana-condominio-9a5a64185
https://br.linkedin.com/in/alvaro-guibson-eng
https://br.linkedin.com/company/bilight-energy
https://br.linkedin.com/company/3s-engenharia-e-inspeção
https://br.linkedin.com/company/pactoengenhariaconsultiva
https://www.linkedin.com/company/grifoengenharia
https://tr.linkedin.com/company/4i-engenharia
https://br.linkedin.com/in/aline-hora-094856250
https://br.linkedin.com/in/raymundo-rocha-00518a58
https://br.linkedin.com/in/flor-anjos-a56696158
https://br.linkedin.com/in/andressa-figueredo-a09692158
https://br.linkedin.com/in/cristiane-luchese-b4835694
https://br.linkedin.com/in/cristiano-farias-b5561155
https://br.linkedin.com/in/stela-mattos-06663816a
https://br.linkedin.com/in/axys
https://br.linkedin.com/in/augusto-cesar-garcia-81628129
https://br.linkedin.com/in/hamiltonlimaa
https://br.linkedin.com/in/leonardo-matos-827320181
https://br.linkedin.com/in/marricatia
https://br.linkedin.com/in/dielma-reis-85b8b567
https://br.linkedin.com/in/dayane-xavier
https://br.linkedin.com/in/daniela-barros-07491137
https://br.linkedin.com/in/rosângela-paixão-263b9794
https://br.linkedin.com/in/valquíria-rosário-54338339
https://br.linkedin.com/in/stephanie-brasil-jones-b35418151
https://br.linkedin.com/in/allure-residências-condomínio-95300b144
https://br.linkedin.com/in/jair-lopes-dos-santos-91133741
https://br.linkedin.com/in/encarregada-condominio-a17a39137
https://br.linkedin.com/in/morada-do-condominio-2a468411a
https://br.linkedin.com/in/joçanã-bispo-22a00791
https://br.linkedin.com/company/ap-consultoria-e-projetos-ltda
https://br.linkedin.com/company/aguilarengenharia
https://br.linkedin.com/company/jequitibaengenharia
https://br.linkedin.com/in/rio-joanes-condomínio-b11b53365
https://br.linkedin.com/in/hartmann-clinica-434876a8
https://br.linkedin.com/in/jovial-clinica-2b712765
https://br.linkedin.com/in/ricardo-pereira-oliveira-4a7576165
https://br.linkedin.com/in/amad-clinica-96b058283
https://br.linkedin.com/in/tamisia-queiroz-a087571a8
https://br.linkedin.com/in/andre-guanaes-md-msc-phd-3b390ab
https://br.linkedin.com/in/jailton-goncalves
https://br.linkedin.com/in/taisdamião
https://br.linkedin.com/in/mariluce-hospital-92b54071
https://br.linkedin.com/in/caio-bernardes-14582822a
https://br.linkedin.com/in/alan-cunha
https://br.linkedin.com/in/claudioviniciusvidal
https://br.linkedin.com/in/jakson-ramos-4b355336
https://br.linkedin.com/in/marcelo-rios-9981104
https://br.linkedin.com/in/maria-beatriz-peixoto-bulgarelli-lopes-072a441b1
https://br.linkedin.com/in/darllan-santiago-3761a8212
https://br.linkedin.com/in/roselia-cristo-63724a205
https://br.linkedin.com/in/daniel-leão-12b377b4
https://br.linkedin.com/in/indalécio-ribeiro-62559322b
https://br.linkedin.com/in/lucas-guanabara-83447744
https://br.linkedin.com/in/eduardo-suarez-sampaio-1412b8172
https://br.linkedin.com/in/marilia-alves-683343231
https://br.linkedin.com/in/israel-dá-conceição-silva-068014245
https://br.linkedin.com/in/luiza-pelizzari-manenti-369250202
https://br.linkedin.com/in/rodrigo-franca-61b33051
https://br.linkedin.com/in/lithocenter-hospital-51b76a188
https://br.linkedin.com/in/gleison-bezerra-7a25b71bb
https://br.linkedin.com/in/claudio-freitas-pmp-836a03149
https://br.linkedin.com/in/andressaleonerh
https://br.linkedin.com/in/flávia-sá-03b9403a
https://br.linkedin.com/in/leandro-nunes-0b6a5817a
https://br.linkedin.com/in/fernando-azevedo-52009460
https://br.linkedin.com/in/maurício-angelo-5401764a
https://br.linkedin.com/in/samuel-sena-46504747
https://br.linkedin.com/in/engbonifacioneves
https://br.linkedin.com/company/pampulha-engenharia
https://br.linkedin.com/company/vivaengenharia
https://br.linkedin.com/company/otm-engenharia
https://br.linkedin.com/company/genese-engenharia
https://br.linkedin.com/company/dna7engenharia
https://br.linkedin.com/in/gustavo-gomes-barcelos-4257b6317
https://br.linkedin.com/company/bnsengenharia
https://br.linkedin.com/in/jeffersonbcruz/en
https://br.linkedin.com/in/lf-construtora-522195110
https://br.linkedin.com/in/celso-castro-244a9a169
https://www.linkedin.com/in/analuisafarah
https://br.linkedin.com/in/adelmo-silva-7694b4173
https://br.linkedin.com/in/andreza-nunes-154589279
https://br.linkedin.com/in/admpauloramos
https://br.linkedin.com/in/ed-pandini
https://br.linkedin.com/in/diego-barral-306b43162
https://br.linkedin.com/in/bernard-pimentel
https://br.linkedin.com/in/eduardafalcao
https://br.linkedin.com/in/joseluciomachado
https://br.linkedin.com/in/wanewman-andrade-15583156
https://br.linkedin.com/in/lazaro-gantois-6428aa72
https://br.linkedin.com/in/mauricio-cardoso-79a95a4b
https://br.linkedin.com/in/natália-de-andrade
https://br.linkedin.com/in/hugo-santos-b86520124
https://br.linkedin.com/in/tarcisioschettini
https://br.linkedin.com/in/rogeriomatos-eng
https://br.linkedin.com/in/amanddasantos
https://br.linkedin.com/in/francisco-costa-neto-03ab0519
https://br.linkedin.com/in/carla-vogelsanger-490759133
https://br.linkedin.com/in/tiago-bonfim-41530010a
https://br.linkedin.com/in/rafael-santos-cruz
"""

# =========================================================
# MENSAGEM CORPORATIVA
# =========================================================

mensagem = """
Prezados,

Gostaria de apresentar a Construtec Engenharia, empresa especializada em serviços de instalações técnicas e serviços civis, oferecendo soluções completas com qualidade, segurança e responsabilidade técnica.

Atuamos nas seguintes áreas:

• Instalações elétricas prediais e industriais
• Instalações de infraestrutura
• Serviços de manutenção preventiva e corretiva
• Obras e reformas civis em geral
• Execução de pisos industriais e concretagem
• Serviços de alvenaria, reboco e acabamentos
• Adequações técnicas conforme necessidade do cliente

Nosso objetivo é oferecer serviços com organização, cumprimento de prazos e custo competitivo, sempre buscando a melhor solução técnica para cada cliente.

Ficamos à disposição para uma visita técnica ou elaboração de orçamento sem compromisso.

Atenciosamente,

Construtec Engenharia
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
    
    # Verificar se já está conectado
    try:
        botoes = driver.find_elements(By.TAG_NAME, "button")
        for botao in botoes:
            texto = botao.text.strip().lower()
            if "já conectado" in texto or "conexão" in texto:
                log("Já conectado com este perfil - pulando", "AVISO")
                resultado["ja_conectado"] = True
                return resultado
    except:
        pass
    
    # Clicar em Conectar/Seguir
    conectado = False
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
    
    # Adicionar nota
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
            
            log(f"\n{'='*50}")
            log(f"PERFIL {progresso['total_processados'] + contador}/{len(perfis)}", "INFO")
            log(f"{perfil}")
            log(f"{'='*50}")
            
            try:
                resultado = processar_perfil(driver, wait, perfil, mensagem, progresso)
                
                if resultado.get("ja_conectado"):
                    ja_conectado += 1
                    processados.add(perfil)
                
                elif resultado["conectado"] and resultado["mensagem_enviada"]:
                    sucesso += 1
                    processados.add(perfil)
                    log(f"SUCESSO: {sucesso} conectados, {mensagem_enviada} mensagens", "SUCESSO")
                
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
        log(f"Já conectado: {ja_conectado}")
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
