import numpy as np

a = np.genfromtxt('../bitmap_sample.csv', delimiter=',', skip_header=1 ,dtype=int)
a = np.pad(a, ( (0, 0), (0,(256-a.shape[1]))), 'constant', constant_values=0)
c = np.packbits(a, axis=-1).view(np.uint32)

bit_array_1 = np.zeros(256, dtype=int)
bit_array_1[2] = 1
select_array_1 = np.packbits(bit_array_1).view(np.uint32)

bit_array_2 = np.zeros(256, dtype=int)
bit_array_2[3] = 1
select_array_2 = np.packbits(bit_array_2).view(np.uint32)

select_array_total = np.array([select_array_1, select_array_2])

res = np.bitwise_and(c, select_array_total[:, None])
sup = np.sum(np.transpose(res.any(axis=2)).all(1))

np.save("./bitmap_sample_result.npy", c)
