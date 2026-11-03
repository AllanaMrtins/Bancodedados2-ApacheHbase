import pandas as pd
import happybase
import sys

print("Conectando ao HBase via porta Thrift (9090)...")

try:
    # Conecta usando o localhost mapeado no Docker
    connection = happybase.Connection('localhost', port=9090)
    tables = connection.tables()
except Exception as e:
    print(f"\nErro de Conexão: Não foi possível acessar a porta 9090 local.")
    print(f"Detalhe do erro: {e}")
    print("Verifique se a linha - \"9090:9090\" está no seu compose-node1.yaml e se reiniciou o container.")
    sys.exit(1)

table_name = 'enem_2025'

# Cria a tabela de dados automaticamente com as duas famílias combinadas
if table_name.encode() not in tables:
    print(f"Criando tabela {table_name} de forma distribuída...")
    connection.create_table(
        table_name,
        {'dados': dict(), 'socioeconomico': dict()}
    )

table = connection.table(table_name)
print("Tabela pronta. Carregando dados do arquivo CSV...")

# Lê a amostra de 70 mil dados gerada
df = pd.read_csv('enem_70k.csv', sep=';', dtype=str, encoding='utf-8')

print("Iniciando a inserção dos 70 mil registros em lotes rápidos...")
with table.batch(batch_size=1000) as b:
    for index, row in df.iterrows():
        row_key = row['NU_INSCRICAO']

        # Mapeamento do cabeçalho exato fornecido (Alinhado dentro do for)
        payload = {
            b'dados:NU_ANO': str(row['NU_ANO']).encode(),
            b'dados:TP_FAIXA_ETARIA': str(row['TP_FAIXA_ETARIA']).encode(),
            b'dados:TP_SEXO': str(row['TP_SEXO']).encode(),
            b'dados:NO_MUNICIPIO_PROVA': str(row['NO_MUNICIPIO_PROVA']).encode(),
            b'dados:SG_UF_PROVA': str(row['SG_UF_PROVA']).encode(),
            b'socioeconomico:Q001': str(row['Q001']).encode(),
            b'socioeconomico:Q002': str(row['Q002']).encode(),
            b'socioeconomico:Q005': str(row['Q005']).encode(),
            b'socioeconomico:Q006': str(row['Q006']).encode(),
        }
        b.put(row_key.encode(), payload)

print("\nSucesso absoluto! 70 mil dados populados e distribuídos no Apache HBase.")
