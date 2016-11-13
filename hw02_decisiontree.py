import csv, math, numpy as np

fname = "E:\\Users\\Tom\\Google Drive\\Studium - Informatik\\Machine Learning\\Übung\\02_homework_dataset.csv"
dataset = [[], [], [], []]
with(open(fname)) as f:
    content = csv.reader(f)

    for line in content:
        print(line)
        if line[0] == "x1":
            continue
        for i in range(0, 4):
            dataset[i].append(float(line[i]))

# for i in dataset[0]:
print()
print("x1:", dataset[0])
print("x2:", dataset[1])
print("x3:", dataset[2])
print("z:", dataset[3])

dataset_size = len(dataset[3])
z1 = 0
z2 = 1
z3 = 2

gini0 = 1 - math.pow(dataset[3].count(z1) / dataset_size, 2) - math.pow(dataset[3].count(z2) / dataset_size, 2) \
        - math.pow(dataset[3].count(z3) / dataset_size, 2)
print(gini0)


def sum_of_class_given_split_on_feature(z, split, feature, comp):
    return sum(1 if dataset[3][j] == z and comp(dataset[feature][j], split) else 0 for j in range(dataset_size))


def lte(a, b):
    return a <= b


def gt(a, b):
    return a > b

delta = dict()
for i in np.arange(0, 10, 0.1):
    sum_z1_i_x1_l = sum_of_class_given_split_on_feature(z1, i, 0, lte)
    sum_z2_i_x1_l = sum_of_class_given_split_on_feature(z2, i, 0, lte)
    sum_z3_i_x1_l = sum_of_class_given_split_on_feature(z3, i, 0, lte)
    sum_z1_i_x1_r = sum_of_class_given_split_on_feature(z1, i, 0, gt)
    sum_z2_i_x1_r = sum_of_class_given_split_on_feature(z2, i, 0, gt)
    sum_z3_i_x1_r = sum_of_class_given_split_on_feature(z3, i, 0, gt)
    gini0_l = 1 \
              - math.pow(sum_z1_i_x1_l / dataset_size, 2) \
              - math.pow(sum_z2_i_x1_l / dataset_size, 2) \
              - math.pow(sum_z3_i_x1_l / dataset_size, 2)
    gini0_r = 1 \
              - math.pow(sum_z1_i_x1_r / dataset_size, 2) \
              - math.pow(sum_z2_i_x1_r / dataset_size, 2) \
              - math.pow(sum_z3_i_x1_r / dataset_size, 2)

    d = gini0 - ((sum_z1_i_x1_l + sum_z2_i_x1_l + sum_z3_i_x1_l) / dataset_size) * gini0_l \
        - ((sum_z1_i_x1_r + sum_z2_i_x1_r + sum_z3_i_x1_r) / dataset_size) * gini0_r
    delta[d] = i
    print("split=" + str(i) + " gini0_l=" + str(gini0_l) + " gini0_r=" + str(gini0_r) + " delta=" + str(d)
          + " [" + str(z1) + "'s (l): " + str(sum_z1_i_x1_l) + " ; " + str(z2) + "'s (l): " + str(sum_z2_i_x1_l) + " ; " + str(z3) + "'s (l): " + str(sum_z3_i_x1_l)
          + " | " + str(z1) + "'s (r): " + str(sum_z1_i_x1_r) + " ; " + str(z2) + "'s (r): " + str(sum_z2_i_x1_r) + " ; " + str(z3) + "'s (r): " + str(sum_z3_i_x1_r) + "]")


for d_entry in delta:
    print(str(delta[d_entry]) + ": " + str(d_entry))
