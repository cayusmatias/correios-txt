import csv
import datetime
import re

date = datetime.date.today()

# dados fixos da postagem
tipo_registro = '9'
codigo_cliente = '11111'
ident_cliente = 'KD'
codigo_operacao = '1101'
conteudo = ''.ljust(16)
filler = '00000000'
nm_sequencial_arq = '00001'
nome_do_cliente = 'XXXX YYYY'.ljust(40)
datageracao = str(date.year) + str(date.month) + str(date.day)
datapostagem = str(date.day) + str(date.month) + str(date.year)

arquivo_saida = f"{ident_cliente}1{datapostagem}0.txt"

linhas = []


def trata_endereco(end, num, comp, bairro):
    end = re.sub('^RUA ', 'R ', end)
    end = re.sub('^ |^ {2}', '', end)
    end = re.sub(' {2}| {3}', ' ', end)
    end = re.sub('[.]', '', end)
    if num in ['0', 'CASA', 'A']:
        num = ''
    end = f"{end} {num}"
    if len(end) < 40:
        end = f"{end} {comp}"
    if len(end) < 40:
        end = f"{end} {bairro}"

    return end


with open('arquivos-src/destinatarios.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for count, row in enumerate(spamreader, start=2):
        nome = row[0].ljust(40)[:40]
        rua = trata_endereco(row[1], row[2], row[3], row[4])
        endereco = f"{rua}".ljust(40)[:40]
        cidade = row[6].ljust(30)
        etiqueta = row[9]
        uf = row[7]
        cep = row[5].zfill(8)[:8]
        finaldalinha = f"{uf}{cep}{filler}{nm_sequencial_arq}{str(count).zfill(7)}"
        # print(count, row)
        linha = f"""{tipo_registro}{codigo_cliente}{ident_cliente}{etiqueta}
                    {codigo_operacao}{conteudo}{nome}{endereco}{cidade}{finaldalinha}"""
        linhas.append(linha)

header = f"""85081000000000000000{nome_do_cliente}{datageracao}
        {str(count).zfill(6)}{''.zfill(94)}{nm_sequencial_arq}0000001"""
print(header)

with open(f'arquivos-gerados/{arquivo_saida}', 'a', newline='') as f:
    f.write(header)
    f.write("\n")

for row in linhas:
    print(row)
    with open(f'arquivos-gerados/{arquivo_saida}', 'a', newline='') as f:
        f.write(row)
        f.write("\n")
