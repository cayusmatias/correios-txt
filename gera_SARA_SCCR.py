import datetime
import csv

date = datetime.datetime.today()
datapostagem = str(date.day) + str(date.month) + str(date.year)
datageracao = str(date.year) + str(date.month) + str(date.day)

contrato = '0000000000'
codigo_adm = '11111111'
codigo_serv = '222222'
cartao_postagem = '33333333333'

arquivo_saida = f"INSSCDIP{datapostagem}{str(date.hour).zfill(2)}{str(date.minute).zfill(2)}{str(date.second).zfill(2)}.txt"

inicio_linha = f'30100000000{datapostagem}0000{contrato}{codigo_adm}'

with open('arquivos-src/destinatarios.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for count, row in enumerate(spamreader, start=1):
        nome = row[0].rjust(40)[:40]
        endereco = f"{row[1]} {row[2]}".ljust(40)[:40]
        cidade = row[6].ljust(30)
        etiqueta = row[9][2:11]
        uf = row[7]
        cep = row[5].zfill(8)[:8]
        contador = count
        linha = f"{inicio_linha}{cep}{codigo_serv}1000000000000,0000000000000{etiqueta}00005{''.zfill(43)}{cartao_postagem}0000000JC00000000000000000000,00{nome}00100000"
        print(linha)

        with open(f'arquivos-gerados/{arquivo_saida}', 'a', newline='') as f:
            f.write(linha)
            f.write("\n")

trailer = f"9{str(contador + 1).zfill(8)}"
with open(f'arquivos-gerados/{arquivo_saida}', 'a', newline='') as f:
    f.write(trailer)
    f.write("\n")
print(trailer)
print(arquivo_saida)