import threading
import time

NumeroDeThreads = 8     
IncrementosPorThread = 200000  


def incrementa_sem_protecao(dados):
    for i in range(IncrementosPorThread):
        valor = dados["contador"]
        if i % 100 == 0:
            time.sleep(0) 
        dados["contador"] = valor + 1


def incrementa_com_semaforo(dados, sem):
    for i in range(IncrementosPorThread):
        sem.acquire()
        try:
            valor = dados["contador"]
            if i % 100 == 0:
                time.sleep(0)
            dados["contador"] = valor + 1
        finally:
            sem.release()


def roda_sem_protecao():
    dados = {"contador": 0}
    threads = [threading.Thread(target=incrementa_sem_protecao, args=(dados,)) for _ in range(NumeroDeThreads)]

    inicio = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.time()

    return dados["contador"], fim - inicio


def roda_com_semaforo():
    dados = {"contador": 0}
    sem = threading.Semaphore(1)  

    threads = [threading.Thread(target=incrementa_com_semaforo, args=(dados, sem)) for _ in range(NumeroDeThreads)]

    inicio = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.time()

    return dados["contador"], fim - inicio

def main():
    esperado = NumeroDeThreads * IncrementosPorThread
    print(f"Threads: {NumeroDeThreads}, incrementos por thread: {IncrementosPorThread}")
    print(f"Valor esperado = {NumeroDeThreads} x {IncrementosPorThread} = {esperado}\n")

    print("--- Sem semaforo (com erro) ---")
    for i in range(1, 4):
        resultado, tempo = roda_sem_protecao()
        print(f"Tentativa {i}: deu {resultado} (perdeu {esperado - resultado}) - {tempo:.3f}s")

    print("\n--- Com semaforo (corrigido) ---")
    for i in range(1, 4):
        resultado, tempo = roda_com_semaforo()
        certo = "certo!" if resultado == esperado else "ERRADO"
        print(f"Tentativa {i}: deu {resultado} - {certo} - {tempo:.3f}s")


if __name__ == "__main__":
    main()