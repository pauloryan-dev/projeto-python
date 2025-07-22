"""
Estudo de Caso — Lógica Computacional com Python
Aluno: Paulo Ryan Ferreira da Silva
Curso: Análise e Desenvolvimento de Sistemas
Projeto: Sistema de Controle de Estoque e Vendas para Loja de Eletrônicos

1. Cenário:
Uma loja de eletrônicos precisa de um sistema simples para gerenciar seu estoque. Fui contratado como desenvolvedor para resolver esse problema.

2. Desafio:
Desenvolver um sistema que permita adicionar, atualizar, excluir e visualizar produtos em estoque, utilizando estruturas condicionais, laços e dicionários em Python.

3. Teoria na prática:
Usei estruturas condicionais (if, else), laços (while e for) e dicionários para armazenar os produtos. Também implementei persistência com arquivos JSON e exportação para CSV. Cada função do sistema representa uma aplicação prática do conteúdo teórico estudado em aula.

4. Levantamento de soluções:
- Utilização de dicionários para modelar os produtos
- Arquivos JSON para salvar os dados entre execuções
- Interface via terminal com menu textual
- Funções separadas para modularizar o código

5. Melhor solução adotada:
Escolhi um sistema modular, simples de executar em qualquer computador com Python instalado, e com funcionalidades extras como registro de vendas, exportação CSV e backup automático — recursos que agregam valor para o cliente.

6. Plano de ação:
- Construir o menu com controle de fluxo
- Implementar funções para cada operação
- Adicionar salvamento em JSON
- Criar backup automático e exportação CSV
- Testar todas as opções para garantir funcionamento

7. Autoavaliação:
Aprendi a importância da organização do código, modularização e controle de fluxo. O projeto me ajudou a aplicar a teoria de forma concreta e funcional. Para versões futuras, posso melhorar o design e até criar uma interface gráfica.

Sistema funcional e pronto para uso via terminal.
"""
import json
import os
import csv
import shutil
from datetime import datetime

ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_VENDAS = "vendas.json"
PASTA_BACKUP = "backup"

def criar_backup_arquivo(arquivo_original):
    if not os.path.exists(PASTA_BACKUP):
        os.makedirs(PASTA_BACKUP)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.basename(arquivo_original)
    backup_nome = f"{nome_arquivo.split('.')[0]}backup{timestamp}.json"
    caminho_backup = os.path.join(PASTA_BACKUP, backup_nome)
    shutil.copy2(arquivo_original, caminho_backup)
    print(f"Backup criado: {caminho_backup}")

def salvar_estoque(estoque):
    with open(ARQUIVO_ESTOQUE, "w") as f:
        json.dump(estoque, f, indent=4)
    criar_backup_arquivo(ARQUIVO_ESTOQUE)

def carregar_estoque():
    if not os.path.exists(ARQUIVO_ESTOQUE):
        return {}
    with open(ARQUIVO_ESTOQUE, "r") as f:
        return json.load(f)

def salvar_vendas(vendas):
    with open(ARQUIVO_VENDAS, "w") as f:
        json.dump(vendas, f, indent=4)
    criar_backup_arquivo(ARQUIVO_VENDAS)

def carregar_vendas():
    if not os.path.exists(ARQUIVO_VENDAS):
        return []
    with open(ARQUIVO_VENDAS, "r") as f:
        return json.load(f)

def exportar_estoque_csv(estoque, nome_arquivo="estoque.csv"):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Nome do Produto", "Preço", "Quantidade"])
        for nome, info in estoque.items():
            escritor.writerow([nome, info['preco'], info['quantidade']])
    print(f"Estoque exportado para {nome_arquivo} com sucesso.")

def exportar_vendas_csv(vendas, nome_arquivo="vendas.csv"):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Cliente", "Produto", "Quantidade"])
        for venda in vendas:
            cliente = venda['cliente']
            for produto, quantidade in venda['itens'].items():
                escritor.writerow([cliente, produto, quantidade])
    print(f"Vendas exportadas para {nome_arquivo} com sucesso.")

def relatorio_produtos_mais_vendidos(vendas):
    contagem_produtos = {}
    for venda in vendas:
        for produto, qtd in venda['itens'].items():
            contagem_produtos[produto] = contagem_produtos.get(produto, 0) + qtd
    if not contagem_produtos:
        print("Nenhuma venda registrada para gerar relatório.")
        return
    print("\n=== Produtos Mais Vendidos ===")
    for produto, total in sorted(contagem_produtos.items(), key=lambda x: x[1], reverse=True):
        print(f"{produto}: {total} unidades vendidas")

def mostrar_menu():
    print("\n=== Sistema de Controle de Estoque e Vendas ===")
    print("1. Adicionar produto")
    print("2. Atualizar produto")
    print("3. Excluir produto")
    print("4. Visualizar estoque")
    print("5. Registrar venda")
    print("6. Visualizar histórico de vendas")
    print("7. Exportar estoque para CSV")
    print("8. Exportar vendas para CSV")
    print("9. Relatório produtos mais vendidos")
    print("10. Sair")

def adicionar_produto(estoque):
    nome = input("Nome do produto: ").strip()
    if nome in estoque:
        print("Produto já existe no estoque!")
        return
    try:
        preco = float(input("Preço do produto: "))
        quantidade = int(input("Quantidade em estoque: "))
    except ValueError:
        print("Preço ou quantidade inválidos.")
        return
    estoque[nome] = {"preco": preco, "quantidade": quantidade}
    print(f"Produto '{nome}' adicionado com sucesso.")

def atualizar_produto(estoque):
    nome = input("Nome do produto para atualizar: ").strip()
    if nome not in estoque:
        print("Produto não encontrado.")
        return
    try:
        preco = input("Novo preço do produto (deixe vazio para manter): ").strip()
        if preco:
            estoque[nome]["preco"] = float(preco)
        qtd = input("Nova quantidade em estoque (deixe vazio para manter): ").strip()
        if qtd:
            estoque[nome]["quantidade"] = int(qtd)
        print(f"Produto '{nome}' atualizado com sucesso.")
    except ValueError:
        print("Preço ou quantidade inválidos.")

def excluir_produto(estoque):
    nome = input("Nome do produto para excluir: ").strip()
    if nome in estoque:
        del estoque[nome]
        print(f"Produto '{nome}' excluído do estoque.")
    else:
        print("Produto não encontrado.")

def visualizar_estoque(estoque):
    if not estoque:
        print("Estoque vazio.")
        return
    print("\n=== Estoque Atual ===")
    for nome, info in estoque.items():
        print(f"Nome: {nome} | Preço: R$ {info['preco']:.2f} | Quantidade: {info['quantidade']}")

def registrar_venda(estoque, vendas):
    cliente = input("Nome do cliente: ").strip()
    carrinho = {}
    while True:
        produto = input("Nome do produto para vender (ou 'fim' para encerrar): ").strip()
        if produto.lower() == "fim":
            break
        if produto not in estoque:
            print("Produto não encontrado no estoque.")
            continue
        try:
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("Quantidade inválida.")
            continue
        if quantidade > estoque[produto]["quantidade"]:
            print(f"Estoque insuficiente. Disponível: {estoque[produto]['quantidade']}")
            continue
        if produto in carrinho:
            carrinho[produto] += quantidade
        else:
            carrinho[produto] = quantidade
    if not carrinho:
        print("Nenhum produto adicionado à venda.")
        return
    for produto, qtd in carrinho.items():
        estoque[produto]["quantidade"] -= qtd
    venda = {"cliente": cliente, "itens": carrinho}
    vendas.append(venda)
    print(f"Venda para '{cliente}' registrada com sucesso.")

def visualizar_vendas(vendas):
    if not vendas:
        print("Nenhuma venda registrada.")
        return
    print("\n=== Histórico de Vendas ===")
    for i, venda in enumerate(vendas, start=1):
        print(f"\nVenda {i}: Cliente: {venda['cliente']}")
        for produto, qtd in venda["itens"].items():
            print(f" - {produto}: {qtd}")

def main():
    estoque = carregar_estoque()
    vendas = carregar_vendas()
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            adicionar_produto(estoque)
            salvar_estoque(estoque)
        elif opcao == "2":
            atualizar_produto(estoque)
            salvar_estoque(estoque)
        elif opcao == "3":
            excluir_produto(estoque)
            salvar_estoque(estoque)
        elif opcao == "4":
            visualizar_estoque(estoque)
        elif opcao == "5":
            registrar_venda(estoque, vendas)
            salvar_estoque(estoque)
            salvar_vendas(vendas)
        elif opcao == "6":
            visualizar_vendas(vendas)
        elif opcao == "7":
            exportar_estoque_csv(estoque)
        elif opcao == "8":
            exportar_vendas_csv(vendas)
        elif opcao == "9":
            relatorio_produtos_mais_vendidos(vendas)
        elif opcao == "10":
            salvar_estoque(estoque)
            salvar_vendas(vendas)
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
