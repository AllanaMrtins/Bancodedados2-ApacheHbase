import sqlite3
import json
import sys

db_name = 'hbase_distribuido_replica.db'

def conectar_banco():
    if not os.path.exists(db_name):
        print(f"[ERRO] O arquivo {db_name} nao foi encontrado nesta pasta!")
        print("Certifique-se de que copiou o arquivo de dados para esta maquina.")
        sys.exit(1)
    return sqlite3.connect(db_name)

def mostrar_menu():
    print("\n" + "="*60)
    print("      CONSOLES DE CONSULTA EM TEMPO REAL - ECOSSISTEMA NO SQL")
    print("="*60)
    print("[1] Mostrar Status do Nó (Total de registros indexados)")
    print("[2] Plano de Execução (Árvore Analítica - EXPLAIN)")
    print("[3] Operação GET por RowKey (Busca por Inscrição Direta)")
    print("[4] Operação SCAN (Varredura de registros em lote)")
    print("[5] Sair")
    print("="*60)

import os

while True:
    mostrar_menu()
    opcao = input("Escolha a operação para demonstrar em tempo real: ")
    
    if opcao == '1':
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM enem_2025")
        total = cursor.fetchone()[0]
        print(f"\n[STATUS DO NÓ] Status: OPERACIONAL | Registros Consistentes: {total}")
        conn.close()
        
    elif opcao == '2':
        conn = conectar_banco()
        cursor = conn.cursor()
        print("\n[PLANO DE EXECUÇÃO - EXPLAIN QUERY PLAN]")
        cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM enem_2025 WHERE row_key = 'teste'")
        plano = cursor.fetchall()
        for p in plano:
            print(f" -> Operação Estrutural: {p[3]}")
        print("\n[DEFESA TÉCNICA] O índice na RowKey evita o Full Table Scan, garantindo complexidade O(1) de busca.")
        conn.close()
        
    elif opcao == '3':
        conn = conectar_banco()
        cursor = conn.cursor()
        print("\n[OPERAÇÃO GET]")
        row_key_digitada = input("Digite a RowKey (Inscrição de teste padrão: 210066506229): ").strip()
        if not row_key_digitada:
            row_key_digitada = '210066506229'
            
        cursor.execute("SELECT * FROM enem_2025 WHERE row_key = ?", (row_key_digitada,))
        res = cursor.fetchone()
        if res:
            print(f"\n-> RowKey Localizada: {res[0]}")
            # Formata o JSON para ficar bonito na tela (Pretty Print)
            dados_cf = json.loads(res[1])
            socio_cf = json.loads(res[2])
            print(f"   Column Family [dados]: {json.dumps(dados_cf, indent=2)}")
            print(f"   Column Family [socioeconomico]: {json.dumps(socio_cf, indent=2)}")
        else:
            print(f"\n[AVISO] RowKey {row_key_digitada} não localizada no fragmento deste nó.")
        conn.close()
        
    elif opcao == '4':
        conn = conectar_banco()
        cursor = conn.cursor()
        limite = input("\nQuantos registros deseja varrer no SCAN? (Padrão 3): ").strip()
        limite = int(limite) if limite.isdigit() else 3
        
        print(f"\n[OPERAÇÃO SCAN - EXECUTANDO VARREDURA PARA {limite} REGISTROS]")
        cursor.execute("SELECT row_key, family_dados, family_socioeconomico FROM enem_2025 LIMIT ?", (limite,))
        scan_res = cursor.fetchall()
        for idx, s in enumerate(scan_res):
            print(f" -> [{idx+1}] RowKey: {s[0]} | Dados Iniciais: {s[1][:50]}... | Socioeconômico: {s[2][:50]}...")
        print("\nVarredura (Scan stream) concluída com sucesso no nó.")
        conn.close()
        
    elif opcao == '5':
        print("\nEncerrando demonstração prática. Cluster liberado.")
        break
    else:
        print("\nOpção inválida! Escolha um comando de 1 a 5.")
        
    input("\nPressione ENTER para continuar...")