import numpy as np
import pandas as pd


def softmax(x):
    exps = np.exp(x - np.max(x, axis=0, keepdims=True))
    return exps / np.sum(exps, axis=0, keepdims=True)


def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return x > 0


def initialize_weights(shape):
    return np.random.randn(*shape) * 0.01


def dense_forward(A_prev, W, b):
    Z = np.dot(W, A_prev) + b
    return Z


def initialize_model(input_dim, hidden_dim, output_dim):
    parameters = {}

    parameters['W1'] = initialize_weights((hidden_dim, input_dim))
    parameters['b1'] = np.zeros((hidden_dim, 1))

    parameters['W2'] = initialize_weights((output_dim, hidden_dim))
    parameters['b2'] = np.zeros((output_dim, 1))

    return parameters


def forward_propagation(X, parameters):
    W1, b1 = parameters['W1'], parameters['b1']
    W2, b2 = parameters['W2'], parameters['b2']

    Z1 = dense_forward(X, W1, b1)
    A1 = relu(Z1)

    Z2 = dense_forward(A1, W2, b2)
    A2 = softmax(Z2)

    cache = (Z1, A1, Z2, A2)
    return A2, cache


def compute_loss(A2, Y):
    m = Y.shape[1]
    loss = -np.sum(Y * np.log(A2)) / m
    return loss


def backward_propagation(X, Y, cache, parameters):
    Z1, A1, Z2, A2 = cache
    W2 = parameters['W2']

    m = Y.shape[1]

    dZ2 = A2 - Y
    dW2 = np.dot(dZ2, A1.T) / m
    db2 = np.sum(dZ2, axis=1, keepdims=True) / m

    dA1 = np.dot(W2.T, dZ2)
    dZ1 = dA1 * relu_derivative(Z1)
    dW1 = np.dot(dZ1, X.T) / m
    db1 = np.sum(dZ1, axis=1, keepdims=True) / m

    grads = {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}

    return grads


def update_parameters(parameters, grads, learning_rate):
    parameters['W1'] -= learning_rate * grads['dW1']
    parameters['b1'] -= learning_rate * grads['db1']
    parameters['W2'] -= learning_rate * grads['dW2']
    parameters['b2'] -= learning_rate * grads['db2']

    return parameters


def train_model(X_train, Y_train, parameters, epochs, learning_rate):
    for epoch in range(epochs):
        epoch_loss = 0
        for i in range(X_train.shape[0]):
            X = X_train[i].reshape(-1, 1)
            Y = Y_train[i].reshape(-1, 1)

            A2, cache = forward_propagation(X, parameters)
            loss = compute_loss(A2, Y)
            epoch_loss += loss

            grads = backward_propagation(X, Y, cache, parameters)
            parameters = update_parameters(parameters, grads, learning_rate)

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss / X_train.shape[0]}\n")

    return parameters


file_path = "../raw_data.csv"
data = pd.read_csv(file_path)

X_data = data.iloc[:, :-1].values
Y_data = data.iloc[:, -1].values

X_data = X_data / np.max(np.abs(X_data), axis=0)

num_classes = len(np.unique(Y_data))
Y_data_one_hot = np.zeros((Y_data.size, num_classes))
Y_data_one_hot[np.arange(Y_data.size), Y_data] = 1

X_train = X_data
Y_train = Y_data_one_hot

input_dim = X_train.shape[1]
hidden_dim = 50
output_dim = num_classes
parameters = initialize_model(input_dim, hidden_dim, output_dim)

epochs = 2000
learning_rate = 0.01
parameters = train_model(X_train, Y_train, parameters, epochs, learning_rate)

print("Final Weights and Biases:")
print("W1:", parameters['W1'])
print("b1:", parameters['b1'])
print("W2:", parameters['W2'])
print("b2:", parameters['b2'])

