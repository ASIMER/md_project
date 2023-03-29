from multiprocessing import Pool
from langdetect import detect


def f(comments):
    d = detect('test')
    for com in comments:
        print(com*5)
    return d

if __name__ == '__main__':
    comms = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    processes = 8
    i_in_part = len(comms) // processes
    print("item_in_part:", i_in_part)
    comms = [
            comms[i * i_in_part
                  : i * i_in_part + i_in_part if i != processes - 1 else None]
            for i in range(processes)
            ]
    with Pool(5) as p:
        print(p.map(f,
                    comms)
              )
