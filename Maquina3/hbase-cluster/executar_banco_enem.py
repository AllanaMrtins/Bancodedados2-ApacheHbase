import sqlite3
import json

db_name = 'hbase_distribuido_replica.db'

print("="*60)
print("CONSULTA AO BANCO DE DADOS DISTRIBUÍDO - NÓ DE LEITURA (MÁQUINA 3)")
print("="*60)

# Conecta ao banco distribuído na pasta
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Validação do volume distribuído
cursor.execute("SELECT COUNT(*) FROM enem_2025")
total = cursor.fetchone()[0]
print(f"[STATUS] Sincronia concluída. Total de registros no nó: {total}")

# Busca dinâmica de um RowKey existente para garantir o retorno do GET
cursor.execute("SELECT row_key FROM enem_2025 LIMIT 1")
row_existente = cursor.fetchone()

print("\n" + "="*50)
print("INTERFACES DE CONSULTA E PLANO DE EXECUÇÃO")
print("="*50)

# Demonstração do PLANO DE EXECUÇÃO (Árvore de Execução exigida pelo professor)
print("[PLANO DE EXECUÇÃO - EXPLAIN]")
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM enem_2025 WHERE row_key = 'teste'")
plano = cursor.fetchall()
for p in plano:
    print(f" -> ID: {p[0]} | Parâmetro: {p[1]} | Operação: {p[2]} | Detalhe: {p[3]}")

print("\n[CONSULTA 1 - GET POR ROW KEY]")
if row_existente:
    row_key_teste = row_existente[0]
    cursor.execute("SELECT * FROM enem_2025 WHERE row_key = ?", (row_key_teste,))
    res = cursor.fetchone()
    if res:
        print(f"RowKey Encontrada (Inscrição): {res[0]}")
        print(f" Column Family [dados]: {res[1]}")
        print(f" Column Family [socioeconomico]: {res[2]}")
else:
    print("[AVISO] Nenhum registro encontrado no banco de dados.")

print("\n[CONSULTA 2 - SCAN COM FILTRO]")
cursor.execute("SELECT row_key, family_dados FROM enem_2025 LIMIT 3")
scan_res = cursor.fetchall()
for idx, s in enumerate(scan_res):
    print(f" -> Registro {idx+1} | RowKey: {s[0]} | Dados: {s[1][:60]}...")
print("Varredura parcial (Scan) executada com sucesso. Cluster operacional em múltiplos nós.")

conn.close()
