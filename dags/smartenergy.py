import fitz  # PyMuPDF
import os
import shutil

def extrair_dados_copel(pdf_path):
    # Abrir o arquivo PDF
    with fitz.open(pdf_path) as pdf:
        texto = ""
        for pagina in pdf:
            texto += pagina.get_text()
    
    # Dicionário para armazenar dados extraídos
    dados_fatura = {
        "cliente": {},
        "fatura": {},
        "consumo": {},
        "tarifas": {},
        "historico_consumo": {},
        "itens_fatura": []
    }
    
    print(texto)
    # Extração de Dados do Cliente
    dados_fatura["cliente"]["nome"] = texto.split("Nome: ")[1].split("\n")[0]
    dados_fatura["cliente"]["endereco"] = texto.split("Endereço: ")[1].split("\n")[0]
    dados_fatura["cliente"]["cpf"] = texto.split("CPF: ")[1].split("\n")[0]
    
    # Extração de Dados da Fatura
    dados_fatura["fatura"]["numero"] = texto.split("Nùmero da fatura: ")[1].split("\n")[0]
    dados_fatura["fatura"]["data_emissao"] = texto.split("DATA DE EMISSÃO: ")[1].split("\n")[0]
    #dados_fatura["fatura"]["vencimento"] = texto.split("Vencimento: ")[1].split("\n")[0]
    #dados_fatura["fatura"]["total"] = texto.split("TOTAL ")[1].split("\n")[0]
    
    # Extração de Dados de Consumo
  #  periodo_consumo = texto.split("B1 Residencial / Residencial Bifasico /50A\n")[1].split("\n")[0]
   # dados_fatura["consumo"]["periodo"] = periodo_consumo
   # dados_fatura["consumo"]["dias"] = int(texto.split("Nº DIAS FAT.")[1].split("\n")[0].strip())
   # dados_fatura["consumo"]["consumo_kwh"] = int(texto.split("CONSUMO FATURADO")[1].split("\n")[0].strip())
    
    # Extração de Tarifas (ICMS, COFINS, PIS)
    dados_fatura["tarifas"]["icms"] = texto.split("ICMS\n")[1].split("\n")[1].strip()
    dados_fatura["tarifas"]["cofins"] = texto.split("COFINS\n")[1].split("\n")[1].strip()
    dados_fatura["tarifas"]["pis"] = texto.split("PIS\n")[1].split("\n")[1].strip()
    
    # Extração do Histórico de Consumo
    historico = {}
    historico_secao = texto.split("HISTÓRICO DE CONSUMO / kWh\n")[1].split("RESÍDUO DE CONSUMO MEDIDOR ANTERIOR")[0]
    for linha in historico_secao.split("\n"):
        if " " in linha:
            mes, consumo = linha.split()[:2]
            historico[mes] = consumo
    dados_fatura["historico_consumo"] = historico
    
    # Extração de Itens da Fatura
    itens_fatura_secao = texto.split("ENERGIA ELET CONSUMO\n")[1].split("ICMS\n")[0]  # Delimitando a seção
    linhas = itens_fatura_secao.split("\n")
    for i in range(0, len(linhas), 4):  # Cada item tem 4 linhas
        if i + 3 < len(linhas):
            descricao = linhas[i].strip()
            unidade = linhas[i + 1].strip()
            quantidade = linhas[i + 2].strip()
            valor_unitario = linhas[i + 3].split()[0].strip()
            valor_total = linhas[i + 3].split()[-1].strip()
            dados_fatura["itens_fatura"].append({
                "descricao": descricao,
                "unidade": unidade,
                "quantidade": quantidade,
                "valor_unitario": valor_unitario,
                "valor_total": valor_total
            })
    
    return dados_fatura

def mover_arquivo_para_pasta_read(pdf_path):
    # Caminho da pasta "read"
    pasta_read = os.path.join(os.path.dirname(pdf_path), "read")
    # Criar a pasta "read" se ela não existir
    os.makedirs(pasta_read, exist_ok=True)
    # Caminho de destino para o arquivo
    destino = os.path.join(pasta_read, os.path.basename(pdf_path))
    # Mover o arquivo para a pasta "read"
    shutil.move(pdf_path, destino)
    print(f"Arquivo movido para {destino}")

# Exemplo de uso
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the PDF file
caminho_pdf = os.path.join(script_dir, "load", "copel.pdf")

#caminho_pdf = "./load/Copel.pdf"
dados = extrair_dados_copel(caminho_pdf)
print(dados)
mover_arquivo_para_pasta_read(caminho_pdf)
