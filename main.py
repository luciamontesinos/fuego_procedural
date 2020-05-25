# import threading
#
# from fire import generate_fire, generate_gif
# thread_list = []
#
# for n in range(16):
#    thread = threading.Thread(target=generate_fire, args=[n, 100, 10])
#    thread_list.append(thread)
#    thread.start()
#
# for thread in thread_list:
#    thread.join()
#
# generate_gif(16)
from multiprocessing.pool import Pool
from fire import generate_fire, generate_gif

if __name__ == '__main__':
    pool = Pool(processes=32)
    [pool.apply(generate_fire, args=[n, 512, 50]) for n in range(8)]
    generate_gif(8)
