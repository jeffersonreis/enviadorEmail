import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class SimpleEmail():

  def __init__(self, email, senha):
    self.__email_enviador = email
    self.__senha_enviador = senha
    self.__message = None
    self.__title = None
    self.__file_name = None
    self.__lista_dados = None
    self.__type_message = None

  @property
  def title(self):
    return self.__title

  @title.setter
  def title(self, title):
    self.__title = title

  def tratarLista(self, arquivo):
    lista = []
    arq = open(arquivo, "r", encoding='utf8')

    for linha in arq.readlines():
      dados = linha.split(",")
      lista.append([dados[0].strip(), dados[1].strip()])

    self.__lista_dados = lista

  def tratarPreMessage(self, arquivo):
    arq = open(arquivo, "r", encoding='utf8')
    msg = ""

    for linha in arq.readlines():
      msg += linha

    self.__pre_message = msg

    if ".html" in arquivo:
      # especial para html
      self.__type_message = "html"

    else: 
      # conversao para .txt etc, string.
      self.__type_message = "plain"
    
  def upFile(self, arq):
    # teste se existe
    test = open(arq, "r")
    test.close
    
    self.__file_name = arq

  def createMessage(self, nome = None):
    self.__message = self.__pre_message.format(nome)

  def sendEmail(self, email_recebedor):
    try: 
      print("Enviando email para:", email_recebedor)

      msg = MIMEMultipart()
      msg['From'] = email_recebedor 
      msg['To'] = self.__email_enviador
      msg['Subject'] = self.__title
      msg.attach(MIMEText(self.__message, self.__type_message))

      if self.__file_name != None:
        attachment = open(self.__file_name,'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        
        part.add_header('Content-Disposition', "attachment; filename=" + self.__file_name)
        
        msg.attach(part)
        attachment.close()

      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(self.__email_enviador, self.__senha_enviador)
      text = msg.as_string()
      server.sendmail(self.__email_enviador, email_recebedor, text)
      server.quit()
      print("Email enviado com sucesso!")

    except:
      print("Houve um erro ao email", email_recebedor)

  def testLogin(self):
    try:
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(self.__email_enviador, self.__senha_enviador)
      server.quit()
      return True

    except:
      return False

  def allSend(self):
    index = 0
    max_index = len(self.__lista_dados)

    for dado in self.__lista_dados:
      index += 1
      print("\n Email nº", index, "/", max_index)
      self.createMessage(dado[0])
      self.sendEmail(dado[1])

def run():
  print("\nEnviador de email! By Jefferson Reis")
  print("ATENÇÃO: Todos os arquivos devem estar na mesma pasta que esse executador")
  email = input("\nEntre com o seu email: ")
  senha = input("Entre com a senha do seu email: ")

  enviador = SimpleEmail(email, senha)
  if enviador.testLogin():
    print("Logado com sucesso")
  else:
    print("Usuário e senha inválidas OU problema com conexão ao servidor (Verificar segurança no Gmail)")
    exit()

  # Carregar Lista de Nomes e Emails 
  # print("\nArquivo de nome e emails")
  # print("Nome + extensao. Ex.: dados.txt")

  while True:
    try:
      # arq = input("\nEntre: ")
      arq = 'dados.txt'
      enviador.tratarLista(arq)
      break

    except:
      print("Erro na lista de contatos")
      entrada = input("Tentar novamente? s/Sim n/Nao ")
      if entrada.lower() == "n" or entrada.lower() == "na" or entrada.lower() == "nao" or entrada.lower() == "no":
        exit()

  # Carregar Texto Mensagem Email
  # print("\nArquivo da mensagem. Ex.: mensagem.txt ou .html")
  while True:
    try:
      # arq = input("Entre: ")
      arq = 'mensagem.html'
      enviador.tratarPreMessage(arq)
      break

    except:
      print("Erro na Mensagem")
      entrada = input("Tentar novamente? s/Sim n/Nao ")
      if entrada.lower() == "n" or entrada.lower() == "na" or entrada.lower() == "nao" or entrada.lower() == "no":
        exit()
      

  # Anexo
  print("\nAdicionar anexo? S/sim - N/nao")
  entrada = input("")
  if entrada.lower() == "sim" or entrada.lower() == "s" or entrada.lower() == "si" or entrada.lower() == "sin":
    while True:
      try:
        print("Arquivo Anexo. Ex.: anexo.pdf")
        arq = input("Entre: ")
        enviador.upFile(arq)
        break

      except:
        print("Erro no arquivo")
        entrada = input("Tentar novamente? s/Sim n/Nao ")
        if entrada.lower() == "n" or entrada.lower() == "na" or entrada.lower() == "nao" or entrada.lower() == "no":
          break


  # Definindo titulo
  titulo = input("\nEntre com o titulo do email: ")
  enviador.title = titulo

  print("\nEnviando os emails!")
  enviador.allSend()
  print("\nTerminamos, obrigado!")
run()