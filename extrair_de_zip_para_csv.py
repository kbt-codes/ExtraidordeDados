import os
import zipfile
import re
import pandas as pd

# === CONFIGURAÇÃO ===
PASTA_ZIPS = 'zips'              # Onde estão os arquivos .zip
PASTA_EXTRACAO = 'extraidos'     # Onde os arquivos serão descompactados
ARQUIVO_SAIDA = 'pacientes.csv'  # Nome do CSV final

# === Função para extrair ZIP ===
def extrair_zip(arquivo_zip, destino):
    with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
        zip_ref.extractall(destino)

# === Função para extrair campos de texto ===
def extrair_dado(texto, campo):
    padrao = fr'\*{campo}:\* ?(.+)'  # ex: *Peso:* 4,1 kg
    resultado = re.search(padrao, texto)
    return resultado.group(1).strip() if resultado else None

# === Começar processamento ===
todos_dados = []

# Criar pasta de extração se não existir
os.makedirs(PASTA_EXTRACAO, exist_ok=True)

# 1. Iterar sobre todos os arquivos .zip
for zip_nome in os.listdir(PASTA_ZIPS):
    if zip_nome.endswith('.zip'):
        caminho_zip = os.path.join(PASTA_ZIPS, zip_nome)
        extrair_zip(caminho_zip, PASTA_EXTRACAO)

# 2. Agora varrer todos os arquivos .txt extraídos
for raiz, dirs, arquivos in os.walk(PASTA_EXTRACAO):
    for nome_arquivo in arquivos:
        if nome_arquivo.endswith('.txt'):
            caminho_txt = os.path.join(raiz, nome_arquivo)
            with open(caminho_txt, 'r', encoding='utf-8') as f:
                texto = f.read()

            dados = {
                'arquivo': nome_arquivo,
                'peso': extrair_dado(texto, 'Peso'),
                'codigo': extrair_dado(texto, 'CÓDIGO'),
                'tutor': extrair_dado(texto, 'TUTOR'),
                'paciente': extrair_dado(texto, 'Paciente'),
                'especie': extrair_dado(texto, 'Espécie'),
                'raca': extrair_dado(texto, 'Raça'),
                'idade': extrair_dado(texto, 'Idade'),
                'sexo': extrair_dado(texto, 'Sexo'),
                'motivo_internacao': extrair_dado(texto, 'Motivo da internação')
            }

            todos_dados.append(dados)

# 3. Criar DataFrame e salvar em CSV
df = pd.DataFrame(todos_dados)
df.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')

print(f"✅ Extração concluída! CSV salvo como: {ARQUIVO_SAIDA}")
