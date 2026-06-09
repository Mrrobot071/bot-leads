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

login = " @gmail.com"
senha = " "

# Limite de perfis por execução (0 = sem limite) - ALTERADO PARA 100
LIMITE_DIARIO = 300

# Arquivo de progresso
ARQUIVO_PROGRESSO = "progresso_linkedin.json"
ARQUIVO_LOG = "log_linkedin.txt"

# =========================================================
# LISTA DE PERFIS
# =========================================================

perfis_texto = """
 
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
