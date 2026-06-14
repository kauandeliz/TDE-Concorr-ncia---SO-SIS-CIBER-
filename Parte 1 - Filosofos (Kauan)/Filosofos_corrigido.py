# Jantar dos Filosofos Versao Corrigida (sem deadlock)
#
# A ideia pra resolver o deadlock e usar uma "hierarquia" nos garfos:
# cada garfo tem um numero (0 a 4), e todo filosofo pega primeiro o
# garfo de NUMERO MENOR e depois o de numero maior, nao importa se
# esse e o garfo da esquerda ou da direita dele.
#
# Isso quebra a condicao de "espera circular" do Coffman, porque agora
# nao tem como formar um ciclo: todo mundo respeita a mesma ordem
# (0 antes de 1, 1 antes de 2, etc), entao nunca vai ter um filosofo
# esperando algo que depende dele mesmo de volta.
#
# Sobre nao deixar ninguem passar fome: como o Lock do python libera
# pra quem ta esperando ha mais tempo (mais ou menos isso), e cada
# filosofo "pensa" um tempinho aleatorio, ninguem fica travado sempre
# por tras dos outros. No teste, todos os 5 filosofos conseguiram comer
# 5 vezes cada.

import random
import threading
import time

N = 5
REFEICOES = 5  # quantas vezes cada filosofo vai comer

garfos = [threading.Lock() for _ in range(N)]
vezes_que_comeu = [0] * N


def filosofo(i):
    garfo_esq = i
    garfo_dir = (i + 1) % N

    # pega primeiro o de menor numero, depois o maior
    primeiro = min(garfo_esq, garfo_dir)
    segundo = max(garfo_esq, garfo_dir)

    for vez in range(REFEICOES):
        print(f"Filosofo {i}: pensando ({vez+1}/{REFEICOES})")
        time.sleep(random.uniform(0.05, 0.2))

        print(f"Filosofo {i}: com fome, vou pegar garfo {primeiro} primeiro")
        garfos[primeiro].acquire()

        print(f"Filosofo {i}: peguei garfo {primeiro}, agora vou pegar {segundo}")
        garfos[segundo].acquire()

        print(f"Filosofo {i}: comendo ({vez+1}/{REFEICOES})")
        vezes_que_comeu[i] += 1
        time.sleep(random.uniform(0.05, 0.15))

        garfos[segundo].release()
        garfos[primeiro].release()
        print(f"Filosofo {i}: terminei e devolvi os garfos")

    print(f"Filosofo {i}: acabei minhas {REFEICOES} refeicoes!")


def main():
    print("=== Jantar dos Filosofos - versao corrigida (sem deadlock) ===\n")

    threads = []
    for i in range(N):
        t = threading.Thread(target=filosofo, args=(i,))
        threads.append(t)

    inicio = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.time()

    print("\n=== Resultado final ===")
    print(f"Demorou {fim - inicio:.2f} segundos")
    for i in range(N):
        print(f"Filosofo {i} comeu {vezes_que_comeu[i]} vezes")
    print("\nNinguem travou, todo mundo conseguiu comer.")


if __name__ == "__main__":
    main()
