# Jantar dos Filosofos Versao Ingenua (com deadlock)
#
# Cada filosofo tenta pegar o garfo da esquerda e depois o da direita.
# Se todo mundo pegar o garfo da esquerda ao mesmo tempo, ninguem
# consegue pegar o da direita (esta na mao do vizinho) e o programa
# trava. Isso e o famoso DEADLOCK.
#
# As 4 condicoes do Coffman que aparecem aqui:
# 1) Exclusao mutua -> cada garfo (Lock) so pode ser usado por 1 filosofo
# 2) Manter e esperar -> filosofo fica com o garfo esquerdo esperando o direito
# 3) Sem preempcao -> nao tem como tirar o garfo de outro na forca
# 4) Espera circular -> filosofo 0 espera o 1, o 1 espera o 2... e o ultimo espera o 0
#
# Para o deadlock acontecer de forma garantida, usamos uma Barrier pra
# fazer todo mundo pegar o garfo esquerdo "no mesmo instante", e um
# sleep antes de tentar o garfo direito.

import threading
import time

N = 5

garfos = [threading.Lock() for _ in range(N)]

# todo mundo so pega o garfo esquerdo depois que TODOS chegarem aqui
barreira = threading.Barrier(N)


def filosofo(i):
    esquerda = garfos[i]
    direita = garfos[(i + 1) % N]

    print(f"Filosofo {i}: pensando...")
    time.sleep(0.2)

    print(f"Filosofo {i}: ta com fome, vou tentar pegar o garfo {i} (esquerda)")

    barreira.wait()  # espera todo mundo chegar aqui

    esquerda.acquire()
    print(f"Filosofo {i}: peguei o garfo {i}")

    time.sleep(0.3)  # da tempo de todo mundo pegar o garfo esquerdo

    print(f"Filosofo {i}: agora vou tentar o garfo {(i+1)%N} (direita)... vai travar")
    direita.acquire()  # AQUI TRAVA - todo mundo fica esperando o vizinho

    # daqui pra baixo nunca executa nessa versao
    print(f"Filosofo {i}: comendo!")
    time.sleep(0.2)
    direita.release()
    esquerda.release()
    print(f"Filosofo {i}: terminei de comer")


def main():
    print("=== Jantar dos Filosofos - versao com deadlock ===\n")

    threads = []
    for i in range(N):
        t = threading.Thread(target=filosofo, args=(i,))
        threads.append(t)
        t.start()

    # espera 5 segundos. se ainda tiver thread viva, e deadlock
    time.sleep(5)

    travadas = [t for t in threads if t.is_alive()]
    if travadas:
        print("\n!!! DEADLOCK !!!")
        print(f"{len(travadas)} filosofos travados, ninguem consegue comer.")
        print("Cada um esta com o garfo da esquerda e esperando o da direita,")
        print("que ta na mao do vizinho. Isso e espera circular -> deadlock.")
        print("\nO programa nao vai terminar sozinho, encerrando agora.")
        import os
        os._exit(0)
    else:
        print("\nTodos terminaram (estranho, nao deveria acontecer aqui).")


if __name__ == "__main__":
    main()
