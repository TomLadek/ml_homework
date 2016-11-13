import csv, math, numpy as np

fname = "..\\..\\Google Drive\\Studium - Informatik\\Machine Learning\\Übung\\02_homework_dataset.csv"
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


def sum_of_class_given_split_on_feature(z, split, feature, comp, this_dataset):
    this_dataset_size = len(this_dataset[0])
    return sum(1 if this_dataset[3][j] == z and comp(this_dataset[feature][j], split) else 0 for j in range(this_dataset_size))


def lte(a, b):
    return a <= b


def gt(a, b):
    return a > b

delta0 = dict()
for i in np.arange(0, 10, 0.1):
    sum_z1_i_x1_l = sum_of_class_given_split_on_feature(z1, i, 0, lte, dataset)
    sum_z2_i_x1_l = sum_of_class_given_split_on_feature(z2, i, 0, lte, dataset)
    sum_z3_i_x1_l = sum_of_class_given_split_on_feature(z3, i, 0, lte, dataset)
    sum_z1_i_x1_r = sum_of_class_given_split_on_feature(z1, i, 0, gt, dataset)
    sum_z2_i_x1_r = sum_of_class_given_split_on_feature(z2, i, 0, gt, dataset)
    sum_z3_i_x1_r = sum_of_class_given_split_on_feature(z3, i, 0, gt, dataset)
    gini1_l = 1 \
              - math.pow(sum_z1_i_x1_l / dataset_size, 2) \
              - math.pow(sum_z2_i_x1_l / dataset_size, 2) \
              - math.pow(sum_z3_i_x1_l / dataset_size, 2)
    gini1_r = 1 \
              - math.pow(sum_z1_i_x1_r / dataset_size, 2) \
              - math.pow(sum_z2_i_x1_r / dataset_size, 2) \
              - math.pow(sum_z3_i_x1_r / dataset_size, 2)

    d = gini0 - ((sum_z1_i_x1_l + sum_z2_i_x1_l + sum_z3_i_x1_l) / dataset_size) * gini1_l \
        - ((sum_z1_i_x1_r + sum_z2_i_x1_r + sum_z3_i_x1_r) / dataset_size) * gini1_r
    delta0[d] = i
    print("split=" + str(i) + " gini0_l=" + str(gini1_l) + " gini0_r=" + str(gini1_r) + " delta0=" + str(d)
          + " [" + str(z1) + "'s (l): " + str(sum_z1_i_x1_l) + " ; " + str(z2) + "'s (l): " + str(sum_z2_i_x1_l) + " ; " + str(z3) + "'s (l): " + str(sum_z3_i_x1_l)
          + " | " + str(z1) + "'s (r): " + str(sum_z1_i_x1_r) + " ; " + str(z2) + "'s (r): " + str(sum_z2_i_x1_r) + " ; " + str(z3) + "'s (r): " + str(sum_z3_i_x1_r) + "]")

curr_max = 0
chosen_split0 = 0
for d_entry in delta0:
    print(str(delta0[d_entry]) + ": " + str(d_entry))
    if math.fabs(d_entry) >= curr_max:
        chosen_split0 = delta0[d_entry]
        curr_max = math.fabs(d_entry)

print("chosen split on lvl 0: " + str(chosen_split0))

dataset1l = [[],[],[],[]]
dataset1r = [[],[],[],[]]
for i in range(dataset_size):
    if dataset[0][i] <= chosen_split0:
        for j in range(0,4):
            dataset1l[j].append(dataset[j][i])
    else:
        for j in range(0,4):
            dataset1r[j].append(dataset[j][i])

print("l tree lvl 1: " + str(dataset1l))
print("r tree lvl 1: " + str(dataset1r))

dataset_size1l = len(dataset1l[0])
delta1l = dict()
gini1l = 1 - math.pow(dataset1l[3].count(z1) / dataset_size1l, 2) - math.pow(dataset1l[3].count(z2) / dataset_size1l, 2) \
        - math.pow(dataset1l[3].count(z3) / dataset_size1l, 2)
for i in np.arange(0, 5.2, 0.1):
    sum_z1_i_x2_l = sum_of_class_given_split_on_feature(z1, i, 2, lte, dataset1l)
    sum_z2_i_x2_l = sum_of_class_given_split_on_feature(z2, i, 2, lte, dataset1l)
    sum_z3_i_x2_l = sum_of_class_given_split_on_feature(z3, i, 2, lte, dataset1l)
    sum_z1_i_x2_r = sum_of_class_given_split_on_feature(z1, i, 2, gt, dataset1l)
    sum_z2_i_x2_r = sum_of_class_given_split_on_feature(z2, i, 2, gt, dataset1l)
    sum_z3_i_x2_r = sum_of_class_given_split_on_feature(z3, i, 2, gt, dataset1l)
    gini2_l = 1 \
              - math.pow(sum_z1_i_x2_l / dataset_size1l, 2) \
              - math.pow(sum_z2_i_x2_l / dataset_size1l, 2) \
              - math.pow(sum_z3_i_x2_l / dataset_size1l, 2)
    gini2_r = 1 \
              - math.pow(sum_z1_i_x2_r / dataset_size1l, 2) \
              - math.pow(sum_z2_i_x2_r / dataset_size1l, 2) \
              - math.pow(sum_z3_i_x2_r / dataset_size1l, 2)

    d = gini1l - ((sum_z1_i_x2_l + sum_z2_i_x2_l + sum_z3_i_x2_l) / dataset_size1l) * gini2_l \
        - ((sum_z1_i_x2_r + sum_z2_i_x2_r + sum_z3_i_x2_r) / dataset_size1l) * gini2_r
    delta1l[d] = i
    print("split=" + str(i) + " gini2_l=" + str(gini2_l) + " gini2_r=" + str(gini2_r) + " delta1l=" + str(d)
          + " [" + str(z1) + "'s (l): " + str(sum_z1_i_x2_l) + " ; " + str(z2) + "'s (l): " + str(sum_z2_i_x2_l) + " ; " + str(z3) + "'s (l): " + str(sum_z3_i_x2_l)
          + " | " + str(z1) + "'s (r): " + str(sum_z1_i_x2_r) + " ; " + str(z2) + "'s (r): " + str(sum_z2_i_x2_r) + " ; " + str(z3) + "'s (r): " + str(sum_z3_i_x2_r) + "]")

curr_max = 0
chosen_split1 = 0
for d_entry in delta1l:
    print(str(delta1l[d_entry]) + ": " + str(d_entry))
    if math.fabs(d_entry) >= curr_max:
        chosen_split1 = delta1l[d_entry]
        curr_max = math.fabs(d_entry)

print("chosen split on lvl 1l: " + str(chosen_split1))

dataset2ll = [[],[],[],[]]
dataset2lr = [[],[],[],[]]
for i in range(dataset_size1l):
    if dataset1l[2][i] <= chosen_split1:
        for j in range(0,4):
            dataset2ll[j].append(dataset1l[j][i])
    else:
        for j in range(0,4):
            dataset2lr[j].append(dataset1l[j][i])

print("ll tree lvl 2: " + str(dataset2ll))
print("lr tree lvl 2: " + str(dataset2lr))

dataset_size2ll = len(dataset2ll[0])
gini2ll = 1 - math.pow(dataset2ll[3].count(z1) / dataset_size2ll, 2) - math.pow(dataset2ll[3].count(z2) / dataset_size2ll, 2) \
         - math.pow(dataset2ll[3].count(z3) / dataset_size2ll, 2)
print("gini 2ll: " + str(gini2ll))

dataset_size2lr = len(dataset2lr[0])
gini2lr = 1 - math.pow(dataset2lr[3].count(z1) / dataset_size2lr, 2) - math.pow(dataset2lr[3].count(z2) / dataset_size2lr, 2) \
          - math.pow(dataset2lr[3].count(z3) / dataset_size2lr, 2)
print("gini 2lr: " + str(gini2lr))