from multiprocessing.pool import Pool

import numpy as np

from fire import generate_fire, generate_gif

seed = np.random.randint(0, 100)
frames = 13
if __name__ == '__main__':
    pool = Pool(processes=frames)
    [pool.apply(generate_fire, args=(n, 512, 50, seed)) for n in range(frames)]
    generate_gif(frames)
