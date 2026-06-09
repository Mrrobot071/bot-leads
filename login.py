from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep

login = " "
senha = " "

options = webdriver.ChromeOptions()

# anti-detecção
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# remove webdriver
driver.execute_script("""
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
""")

driver.maximize_window()

driver.get("https://www.linkedin.com/login")

print(driver.title)

try:

    wait = WebDriverWait(driver, 30)

    # campo email
    email_input = wait.until(
        EC.element_to_be_clickable((By.ID, "username"))
    )

    email_input.clear()
    sleep(1)

    email_input.send_keys(login)

    # campo senha
    senha_input = wait.until(
        EC.element_to_be_clickable((By.ID, "password"))
    )

    senha_input.clear()
    sleep(1)

    senha_input.send_keys(senha)

    sleep(2)

    # botão entrar
    botao = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )

    botao.click()

    print("Login enviado!")

    # espera carregar
    sleep(10)

    print("URL atual:", driver.current_url)

    # verifica se logou
    if "feed" in driver.current_url:
        print("LOGIN FEITO COM SUCESSO")
    else:
        print("LinkedIn pode ter pedido verificação.")

except TimeoutException:

    print("Não encontrou campo de login.")
    print("URL atual:", driver.current_url)

    driver.save_screenshot("erro_login.png")

except Exception as e:
    print("ERRO:", e)

input("Pressione ENTER para fechar...")

driver.quit()
