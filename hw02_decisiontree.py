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
delta = dict()

def sum_of_class_given_split_on_feature(z, split, feature, comp, this_dataset):
    this_dataset_size = len(this_dataset[0])
    return sum(1 if this_dataset[3][j] == z and comp(this_dataset[feature][j], split) else 0 for j in range(this_dataset_size))


def lte(a, b):
    return a <= b


def gt(a, b):
    return a > b


def chose_split_by_deltas(deltas_dict):
    curr_max = 0
    chosen_split = -1
    for d_entry in deltas_dict:
        print(str(deltas_dict[d_entry]) + ": " + str(d_entry))
        if math.fabs(d_entry) >= curr_max:
            chosen_split = deltas_dict[d_entry]
            curr_max = math.fabs(d_entry)
    return [chosen_split, curr_max]


def test_split_for_feature(feature, dataset, gini):
    dataset_size = len(dataset[0])
    for i in np.arange(-0.6, 10, 0.1):
        sum_z1_i_l = sum_of_class_given_split_on_feature(z1, i, feature, lte, dataset)
        sum_z2_i_l = sum_of_class_given_split_on_feature(z2, i, feature, lte, dataset)
        sum_z3_i_l = sum_of_class_given_split_on_feature(z3, i, feature, lte, dataset)
        sum_z1_i_r = sum_of_class_given_split_on_feature(z1, i, feature, gt, dataset)
        sum_z2_i_r = sum_of_class_given_split_on_feature(z2, i, feature, gt, dataset)
        sum_z3_i_r = sum_of_class_given_split_on_feature(z3, i, feature, gt, dataset)
        dataset_sizel = sum_z1_i_l + sum_z2_i_l + sum_z3_i_l
        dataset_sizer = sum_z1_i_r + sum_z2_i_r + sum_z3_i_r
        if dataset_sizel == 0 or dataset_sizer == 0:
            continue
        gini_l = 1 \
                  - math.pow(sum_z1_i_l / dataset_sizel, 2) \
                  - math.pow(sum_z2_i_l / dataset_sizel, 2) \
                  - math.pow(sum_z3_i_l / dataset_sizel, 2)
        gini_r = 1 \
                  - math.pow(sum_z1_i_r / dataset_sizer, 2) \
                  - math.pow(sum_z2_i_r / dataset_sizer, 2) \
                  - math.pow(sum_z3_i_r / dataset_sizer, 2)

        d = gini - ((sum_z1_i_l + sum_z2_i_l + sum_z3_i_l) / dataset_size) * gini_l \
            - ((sum_z1_i_r + sum_z2_i_r + sum_z3_i_r) / dataset_size) * gini_r
        delta[d] = i
        print("split=" + str(i) + " gini0_l=" + str(gini_l) + " gini0_r=" + str(gini_r) + " delta0=" + str(d)
              + " [" + str(z1) + "'s (l): " + str(sum_z1_i_l) + " ; " + str(z2) + "'s (l): " + str(sum_z2_i_l) + " ; " + str(z3) + "'s (l): " + str(sum_z3_i_l)
              + " | " + str(z1) + "'s (r): " + str(sum_z1_i_r) + " ; " + str(z2) + "'s (r): " + str(sum_z2_i_r) + " ; " + str(z3) + "'s (r): " + str(sum_z3_i_r) + "]")
    return delta

gini0 = 1 - math.pow(dataset[3].count(z1) / dataset_size, 2) - math.pow(dataset[3].count(z2) / dataset_size, 2) \
        - math.pow(dataset[3].count(z3) / dataset_size, 2)
print("gini 0: " + str(gini0))

feature_to_split_on = -1
split_and_max_delta = [-1, 0]
chosen_feature = -1
# depth 0 -> 1 
for f in range(0,3):
    delta.clear()
    d_dict = test_split_for_feature(f, dataset, gini0)
    split_and_max = chose_split_by_deltas(d_dict)
    if split_and_max[1] > split_and_max_delta[1]:
        split_and_max_delta = split_and_max
        chosen_feature = f

print("split_and_max_delta=" + str(split_and_max_delta))
print("chosen_feature=" + str(chosen_feature))

dataset1l = [[],[],[],[]]
dataset1r = [[],[],[],[]]
for i in range(dataset_size):
    if dataset[0][i] <= split_and_max_delta[0]:
        for j in range(0,4):
            dataset1l[j].append(dataset[j][i])
    else:
        for j in range(0,4):
            dataset1r[j].append(dataset[j][i])

print("l tree lvl 1: " + str(dataset1l)) # -> pure node, no split needed for l2!
print("r tree lvl 1: " + str(dataset1r))

dataset_size1l = len(dataset1l[0])
gini1l = 1 - math.pow(dataset1l[3].count(z1) / dataset_size1l, 2) - math.pow(dataset1l[3].count(z2) / dataset_size1l, 2) \
          - math.pow(dataset1l[3].count(z3) / dataset_size1l, 2)
print("gini 1l: " + str(gini1l))

dataset_size1r = len(dataset1r[0])
gini1r = 1 - math.pow(dataset1r[3].count(z1) / dataset_size1r, 2) - math.pow(dataset1r[3].count(z2) / dataset_size1r, 2) \
          - math.pow(dataset1r[3].count(z3) / dataset_size1r, 2)
print("gini 1r: " + str(gini1r))

dataset = dataset1r
dataset_size = len(dataset[0])
split_and_max_delta = [-1, 0]
chosen_feature = -1
# depth 1 -> 2
for f in range(0,3):
    delta.clear()
    d_dict = test_split_for_feature(f, dataset, gini1r)
    split_and_max = chose_split_by_deltas(d_dict)
    if split_and_max[1] > split_and_max_delta[1]:
        split_and_max_delta = split_and_max
        chosen_feature = f

print("split_and_max_delta=" + str(split_and_max_delta))
print("chosen_feature=" + str(chosen_feature))

dataset2rl = [[],[],[],[]]
dataset2rr = [[],[],[],[]]
for i in range(dataset_size):
    if dataset[0][i] <= split_and_max_delta[0]:
        for j in range(0,4):
            dataset2rl[j].append(dataset[j][i])
    else:
        for j in range(0,4):
            dataset2rr[j].append(dataset[j][i])

print("rl tree lvl 2: " + str(dataset2rl))
print("rr tree lvl 2: " + str(dataset2rr)) # pure node -> no split needed!

dataset_size2rl = len(dataset2rl[0])
gini2ll = 1 - math.pow(dataset2rl[3].count(z1) / dataset_size2rl, 2) - math.pow(dataset2rl[3].count(z2) / dataset_size2rl, 2) \
         - math.pow(dataset2rl[3].count(z3) / dataset_size2rl, 2)
print("gini 2rl: " + str(gini2ll))

dataset_size2rr = len(dataset2rr[0])
gini2lr = 1 - math.pow(dataset2rr[3].count(z1) / dataset_size2rr, 2) - math.pow(dataset2rr[3].count(z2) / dataset_size2rr, 2) \
          - math.pow(dataset2rr[3].count(z3) / dataset_size2rr, 2)
print("gini 2rr: " + str(gini2lr))