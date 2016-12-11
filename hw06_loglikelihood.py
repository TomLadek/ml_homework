import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt


def plot_decision_boundary(X, Z, W=None, b=None):
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.scatter(X[:,0], X[:,1], c=Z, cmap=plt.cm.cool)
    ax.set_autoscale_on(False)

    a = - W[0, 0] / W[0, 1]
    xx = np.linspace(-30, 30)
    yy = a * xx - (b[0]) / W[0, 1]

    ax.plot(xx, yy, 'k-', c=plt.cm.cool(1.0/3.0))


def loadDataset(split, X=[] , XT=[], Z = [], ZT = []):
    dataset = datasets.load_iris()
    c = list(zip(dataset['data'], dataset['target']))
    np.random.seed(224)
    np.random.shuffle(c)
    x, t = zip(*c)
    sp = int(split*len(c))
    X = x[:sp]
    XT = x[sp:]
    Z = t[:sp]
    ZT = t[sp:]
    names = ['Sepal. length', 'Sepal. width', 'Petal. length', 'Petal. width']
    return np.array(X), np.array(XT), np.array(Z), np.array(ZT), names

# prepare data
split = 0.67
X, XT, Z, ZT, names = loadDataset(split)

# combine two of the 3 classes for a 2 class problem
Z[Z==2] = 1
ZT[ZT==2] = 1

# only look at 2 dimensions of the input data for easy visualisation
X = X[:,:2]
XT = XT[:,:2]


def pred(X, W, b):
    c = np.add(b, np.dot(X, W.transpose()))    # X is already transposed but W isn't

    if np.isscalar(c):
        c = np.array([c])

    for x in np.nditer(c, op_flags=['readwrite']):
        x[...] = 1 / (1 + np.exp(-1 * x))    # transform each position with 1 / (1 + exp(-a))

    return np.reshape(c, (X.shape[0],1))

print(pred(X, np.ones(2), -10))


def loglikelihood(X, Z, W, b):
    #product = 1
    #for i in range(X.shape[0]):
    #    product = product * np.power(pred(np.array([X[i]]), W, b), Z[i]) * np.power(pred(np.array([X[i]]), W, b), 1 - Z[i])
    #neglog = -1 * np.log(product)
    #return neglog

    error = 0
    for i in range(X.shape[0]):
        error += Z[i] * np.log(pred(np.array([X[i]]), W, b)) + (1 - Z[i]) * np.log(1 - pred(np.array([X[i]]), W, b))
    return error

#loglikelihood(X, Z, np.ones(2), -10)


def grad(X, Z, W, b):
    return np.empty_like(W), np.empty_like(b)


W = np.random.randn(1,2) * 0.01
b = np.random.randn(1) * 0.01

learning_rate = 0.001
train_loss = []
validation_loss = []

for i in range(10000):
    dLdW, dLdb = grad(X, Z, W, b)

    W -= learning_rate * dLdW
    b -= learning_rate * dLdb
    train_loss.append( - loglikelihood(X, Z, W, b).mean())

_ = plt.plot(train_loss)