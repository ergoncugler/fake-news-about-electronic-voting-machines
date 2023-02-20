# bibliotecas
import time
import requests
from bs4 import BeautifulSoup

# bibliotecas google
from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

# criar nova planilha
sh = gc.create("extraindo_fato_ou_boato")
worksheet = gc.open("extraindo_fato_ou_boato").sheet1
titulos = ["ID","Título","Data","Link","Texto","Detalhe"]
campos = worksheet.range('A1:F1')
for i in range(0, len(campos)):
  campos[i].value = titulos[i]
worksheet.update_cells(campos)

# início do loop
paginas = 33 # máximo 33
fatos = 12 # padrão 12

index = 1

p = 1
for i in range(paginas):
  site = "https://www.justicaeleitoral.jus.br/fato-ou-boato/checagens/"
  url = f"{site}?b_start:int={(p-1)*12}"
  bs = BeautifulSoup(requests.get(url).text,'html.parser')

  f = 0
  for i in range(fatos):

    # título
    titulo = bs.find_all(class_="check-title")
    titulo = titulo[f].get_text()

    # data
    data = bs.find_all(class_="check-time")
    data = data[f].get_text()

    # link
    link = bs.findAll("div", attrs={"class":"check-body"})
    link = link[f].find("a")["href"]

    # texto
    texto = bs.find_all(class_="check-text")
    texto = texto[f].get_text()
    
    # detalhe
    bs_interno = BeautifulSoup(requests.get(link).text,'html.parser')
    detalhe = bs_interno.find_all(class_="interna-content")
    detalhe = detalhe[1].get_text()

    # planilhando
    conteudo = [index, titulo, data, link, texto, detalhe]
    registros = worksheet.range(f"A{index+1}:F{index+1}")
    for i in range(0,len(registros)):
      registros[i].value = conteudo[i]
    worksheet.update_cells(registros)

    f=f+1
    index=index+1

  p=p+1
  print(f"Página {p-1} obteve {f} citações com sucesso: {((p-1)/paginas)*100:.2f}% realizado. Total de {index-1} citações.")
  time.sleep(2)

print("\nConcluído!\n\n\n\n\n")
