LinkedIn Conector Automatizado
Scripts automatizado em Python usando Selenium para conectar e enviar mensagens corporativas no LinkedIn de forma semi-automática.

📋 Funcionalidades
✅ Login automático no LinkedIn com anti-detecção

🤝 Conectar/Seguir em perfis de pessoas e empresas

📧 Enviar mensagem personalizada junto com o convite

🔄 Continua de onde parou (salva progresso automaticamente)

📝 Log detalhado em arquivo com timestamp

🚫 Limite diário configurável para evitar bloqueios

🎭 Anti-detecção avançada (User-Agent aleatório, remover webdriver)

🚯 Remove duplicatas da lista de perfis automaticamente

📊 Estatísticas finais (sucessos, falhas, já conectados)

🖼️ Screenshots em erros para debug

⚠️ Aviso Importante
Este script viola os Termos de Serviço do LinkedIn. O uso pode resultar em:

Bloqueio temporário ou permanente da conta

Restrições de acesso

Suspensão da conta

Use por sua própria conta e risco. Recomenda-se:

Manter limites diários baixos (30-50 conexões)

Usar pausas longas entre ações

Não usar para spam ou massa

🛠️ Instalação
1. Pré-requisitos
Python 3.8 ou superior

Chrome ou Chromium instalado

Conta no LinkedIn

2. Instalar dependências
bash
pip install selenium webdriver-manager
🚀 Como Usar
1. Configurar credenciais
No início do script, edite:

python
login = "seu-email@gmail.com"
senha = "sua-senha"
LIMITE_DIARIO = 50  # Número máximo de perfis por execução (0 = sem limite)
2. Adicionar perfis
Na variável perfis_texto, cole os links do LinkedIn (1 por linha):

python
perfis_texto = """
https://br.linkedin.com/in/exemplo1
https://br.linkedin.com/company/exemplo2
https://br.linkedin.com/in/exemplo3
"""
3. Personalizar mensagem
Edite a variável mensagem com sua mensagem corporativa:

python
mensagem = """
Prezados,

Gostaria de apresentar sua empresa...

Atenciosamente,
Seu Nome
"""
4. Executar
bash
python script_linkedin.py
📁 Arquivos Gerados
Arquivo	Descrição
progresso_linkedin.json	Progresso salvo (perfis processados)
log_linkedin.txt	Log completo com timestamp de todas as ações
erro_login.png	Screenshot se falhar no login
erro_perfil_X.png	Screenshot se falhar em perfil específico
erro_crítico.png	Screenshot de erro crítico
⚙️ Configurações
Variável	Descrição	Valor Padrão
LIMITE_DIARIO	Máximo de perfis por execução	50
ARQUIVO_PROGRESSO	Arquivo de progresso	"progresso_linkedin.json"
ARQUIVO_LOG	Arquivo de log	"log_linkedin.txt"
📊 Exemplo de Log
text
[2026-05-28 15:03:45] [INFO] ============================================================
[2026-05-28 15:03:45] [INFO] INICIANDO SCRIPT LINKEDIN - CONECTAR + MENSAGEM
[2026-05-28 15:03:45] [INFO] ============================================================
[2026-05-28 15:03:47] [INFO] Total de perfis únicos: 100
[2026-05-28 15:03:47] [INFO] Perfis já processados: 0
[2026-05-28 15:03:47] [INFO] Perfis pendentes: 100
[2026-05-28 15:03:50] [INFO] Abrindo página de login...
[2026-05-28 15:04:02] [SUCESSO] LOGIN EFETUADO COM SUCESSO
[2026-05-28 15:04:10] [INFO] ==================================================
[2026-05-28 15:04:10] [INFO] PERFIL 1/100
[2026-05-28 15:04:10] [INFO] https://br.linkedin.com/in/exemplo1
[2026-05-28 15:04:10] [INFO] ==================================================
[2026-05-28 15:04:18] [SUCESSO] Botão CONECTAR clicado
[2026-05-28 15:04:25] [INFO] Abrindo campo de mensagem
[2026-05-28 15:04:30] [SUCESSO] Mensagem enviada com sucesso
[2026-05-28 15:04:30] [SUCESSO] SUCESSO: 1 conectados, 1 mensagens
[2026-05-28 15:04:30] [INFO] Pausa operacional: 35s
🔧 Troubleshooting
Login falha / CAPTCHA aparece
LinkedIn detectou comportamento automatizado

Aguarde 24h antes de tentar novamente

Reduza o LIMITE_DIARIO para 20-30

Use pausas mais longas

Não encontra botão "Conectar"
O perfil já pode estar conectado

O perfil pode não permitir conexões

Verifique se o link está correto

Chrome não abre
bash
# Atualize o webdriver
pip install --upgrade webdriver-manager
Erro de Selenium
bash
# Reinstale as dependências
pip install --upgrade selenium webdriver-manager
🔄 Reiniciar do Zero
Para limpar tutto e começar de novo:

bash
# Apague os arquivos de progresso
rm progresso_linkedin.json
rm log_linkedin.txt
📝 Dicas de Uso Seguro
Comece com limite baixo: LIMITE_DIARIO = 20

Aumente gradualmente: Se não houver problemas, aumente para 30, 40, 50

Use em horários comerciais: Maior chance de parecer comportamento humano

Monitore o log: Verifique se não está sendo detectado

Não repita mensagem exatamente: Considere personalizar por perfil

Pare se ver CAPTCHA: Não force, aguarde 24h

📄 Estrutura do Código
text
├── Configurações (login, senha, limites)
├── Lista de perfis
├── Mensagem corporativa
├── Funções de log e progresso
├── Configuração do Chrome (anti-detecção)
├── Função de login
├── Função de processar perfil
└── Main loop
⚖️ Licença
Uso pessoal e educacional. O autor não se responsabiliza por:

Bloqueio de contas

Violação de termos de serviço

Qualquer dano decorrente do uso deste script

🤝 Contribuição
Para melhorar o script:

Adicionar mais opções anti-detecção

Implementar proxy rotativo

Criar painel de controle

Adicionar suporte a múltiplas contas

Implementar reconhecimento de CAPTCHA