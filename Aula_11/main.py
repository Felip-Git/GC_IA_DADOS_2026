import os
import random

cardapio = {
    "chocolate": 5.00,
    "baunilha": 4.50,
    "morango": 3.00,
    "flocos": 9.00
}

brindes = ["Canudos", "Copo personalizado", "Gelo", "Badge"]

def mostrar_cardapio():
    print("-- CARDAPIO --")
    for sabor, preco in cardapio.items():
        print(f"{sabor}, R${preco}")

def fazer_pedido():
    total = 0
    pedido = []
    while True:
        sabor = input("Escolhe o sabor: (digite 'fechar' para encerrar o pedido) ")
        if sabor == "fechar":
            print("Pedido encerrado.")
            
            break
            
        elif sabor in cardapio:
            total += cardapio[sabor]
            pedido.append(sabor)
            print(f"{sabor.title()} adicionado ao pedido. Total: R${total:.2f}")
        else:
            print("Sabor não disponível.")
    return pedido, total

mostrar_cardapio()
pedido, total = fazer_pedido()

print(f"\nSeu pedido: {pedido}")
print(f"Total a pagar: R${total:.2f}")

if total > 20:
    brinde = random.choice(brindes)
    print(f"Parabéns! Você ganhou um brinde: {brinde}")