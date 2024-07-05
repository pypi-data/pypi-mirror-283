import numpy as np
import json

class no:
    def __init__(self, refd):
        self.data_processor = nopro(refd)
        input_size = self.data_processor.max_length * len(self.data_processor.vocab)
        hidden_size = 50
        output_size = len(self.data_processor.label_to_index)
        hidden_layers = 1
        self.model = noNN(input_size, hidden_size, output_size, hidden_layers)

    def train(self, epochs, ilr, decay):
        X = self.data_processor.X
        y = self.data_processor.y
        self.model.train(X, y, epochs, ilr, decay)

    def predict(self, tref):
        vocab = self.data_processor.vocab
        word_to_index = self.data_processor.word_to_index
        index_to_label = self.data_processor.index_to_label
        max_length = self.data_processor.max_length

        X = np.zeros((len(tref), max_length, len(vocab)))
        for i, sentence in enumerate(tref):
            for j, word in enumerate(sentence.replace("_____", "BLANK").split()):
                if word in word_to_index:
                    X[i, j, word_to_index[word]] = 1
        X = X.reshape(len(X), -1)
        predicted_output = self.model.forward(X)
        predicted_indices = np.argmax(predicted_output, axis=1)
        predicted_words = [index_to_label[idx] for idx in predicted_indices]
        return predicted_words

    def save(self, filepath):
        self.model.save_model(filepath)

    def load(self, filepath):
        self.model.load_model(filepath)

class noNN:
    def __init__(self, input_size, hidden_size, output_size, hidden_layers=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.hidden_layers = hidden_layers

        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2. / self.input_size)
        self.bias_input_hidden = np.zeros((1, self.hidden_size))

        self.weights_hidden_hidden = [
            np.random.randn(self.hidden_size, self.hidden_size) * np.sqrt(2. / self.hidden_size)
            for _ in range(hidden_layers - 1)
        ]
        self.bias_hidden_hidden = [np.zeros((1, self.hidden_size)) for _ in range(hidden_layers - 1)]

        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2. / self.hidden_size)
        self.bias_hidden_output = np.zeros((1, self.output_size))

    def elu(self, x, alpha=1.0):
        return np.where(x > 0, x, alpha * (np.exp(x) - 1))

    def elu_derivative(self, x, alpha=1.0):
        return np.where(x > 0, 1, alpha * np.exp(x))

    def forward(self, X):
        self.hidden_outputs = []
        hidden_output = self.elu(np.dot(X, self.weights_input_hidden) + self.bias_input_hidden)
        self.hidden_outputs.append(hidden_output)

        for i in range(self.hidden_layers - 1):
            hidden_output = self.elu(np.dot(hidden_output, self.weights_hidden_hidden[i]) + self.bias_hidden_hidden[i])
            self.hidden_outputs.append(hidden_output)

        self.predicted_output = np.dot(hidden_output, self.weights_hidden_output) + self.bias_hidden_output
        return self.predicted_output

    def backward(self, X, y, output, learning_rate):
        error = y - output
        output_delta = error
        hidden_deltas = [output_delta]

        for i in reversed(range(self.hidden_layers)):
            hidden_output = self.hidden_outputs[i]
            hidden_error = np.dot(hidden_deltas[0], self.weights_hidden_output.T if i == self.hidden_layers - 1 else self.weights_hidden_hidden[i].T)
            hidden_delta = hidden_error * self.elu_derivative(hidden_output)
            hidden_deltas.insert(0, hidden_delta)

        max_grad = 1.0
        hidden_deltas = [np.clip(delta, -max_grad, max_grad) for delta in hidden_deltas]

        self.weights_hidden_output += np.dot(self.hidden_outputs[-1].T, hidden_deltas[-1]) * learning_rate
        self.bias_hidden_output += np.sum(hidden_deltas[-1], axis=0, keepdims=True) * learning_rate

        for i in range(self.hidden_layers - 1, 0, -1):
            self.weights_hidden_hidden[i-1] += np.dot(self.hidden_outputs[i-1].T, hidden_deltas[i]) * learning_rate
            self.bias_hidden_hidden[i-1] += np.sum(hidden_deltas[i], axis=0, keepdims=True) * learning_rate

        self.weights_input_hidden += np.dot(X.T, hidden_deltas[0]) * learning_rate
        self.bias_input_hidden += np.sum(hidden_deltas[0], axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate, decay_rate):
        y_one_hot = np.zeros((y.size, self.output_size))
        y_one_hot[np.arange(y.size), y] = 1

        for epoch in range(epochs):
            learning_rate = learning_rate / (1 + decay_rate * epoch)
            output = self.forward(X)

            if np.isnan(output).any():
                print(f"NaN detected at epoch {epoch}")
                break

            self.backward(X, y_one_hot, output, learning_rate)
            if epoch % 1000 == 0:
                loss = np.mean(np.square(y_one_hot - output))
                print(f"Epoch: {epoch}, Loss: {loss}")

    def save_model(self, filepath):
        model_data = {
            "weights_input_hidden": self.weights_input_hidden.tolist(),
            "bias_input_hidden": self.bias_input_hidden.tolist(),
            "weights_hidden_hidden": [w.tolist() for w in self.weights_hidden_hidden],
            "bias_hidden_hidden": [b.tolist() for b in self.bias_hidden_hidden],
            "weights_hidden_output": self.weights_hidden_output.tolist(),
            "bias_hidden_output": self.bias_hidden_output.tolist()
        }
        with open(filepath, "w") as f:
            json.dump(model_data, f)

    def load_model(self, filepath):
        with open(filepath, "r") as f:
            model_data = json.load(f)
        self.weights_input_hidden = np.array(model_data["weights_input_hidden"])
        self.bias_input_hidden = np.array(model_data["bias_input_hidden"])
        self.weights_hidden_hidden = [np.array(w) for w in model_data["weights_hidden_hidden"]]
        self.bias_hidden_hidden = [np.array(b) for b in model_data["bias_hidden_hidden"]]
        self.weights_hidden_output = np.array(model_data["weights_hidden_output"])
        self.bias_hidden_output = np.array(model_data["bias_hidden_output"])

class nopro:
    def __init__(self, refd):
        self.refd = refd
        self.X_raw = [sentence[1].replace("_____", "BLANK") for sentence in refd]
        self.y_raw = [sentence[0] for sentence in refd]
        self.build_vocabulary()
        self.encode_labels()
        self.encode_sentences()

    def build_vocabulary(self):
        self.vocab = set(word for sentence in self.X_raw for word in sentence.split())
        self.vocab.add("BLANK")
        self.vocab = sorted(self.vocab)
        self.word_to_index = {word: i for i, word in enumerate(self.vocab)}
        self.index_to_word = {i: word for i, word in enumerate(self.vocab)}

    def encode_labels(self):
        unique_labels = list(set(self.y_raw))
        self.label_to_index = {label: i for i, label in enumerate(unique_labels)}
        self.index_to_label = {i: label for i, label in enumerate(unique_labels)}
        self.y = np.array([self.label_to_index[label] for label in self.y_raw])

    def encode_sentences(self):
        self.max_length = max(len(sentence.split()) for sentence in self.X_raw)
        self.X = np.zeros((len(self.X_raw), self.max_length, len(self.vocab)))
        for i, sentence in enumerate(self.X_raw):
            for j, word in enumerate(sentence.split()):
                self.X[i, j, self.word_to_index[word]] = 1
        self.X = self.X.reshape(len(self.X), -1)

# Example usage in a Jupyter notebook
refd = [
    ("running", "I am _____ fast"),
    ("running", "He is _____ fast"),
    ("running", "She is _____ a computer"),
    ("coding", "We are _____ a new project"),
    ("coding", "They are _____ a game"),
    ("coding", "The boys are _____"),
    ("eating", "I am _____ dinner"),
    ("eating", "The baby is _____"),
    ("eating", "She is _____ a burger")
]

# Initialize the model
model = no(refd)

# Training parameters
ilr = 0.01
decay = 1e-6
epochs = 50000

# Train the model
model.train(epochs, ilr, decay)

# Test data
tref = [
    "She is _____ fast",
    "They are _____ the project",
    "I am _____ a book",
    "The cat is _____ the food"
]

# Predict
res = model.predict(tref)
for i, sentence in enumerate(tref):
    print(f"Input: {sentence}, Predicted: {res[i]}")

# Save the model
model.save("model.json")

# Load the model and predict again
model.load("model.json")
res = model.predict(tref)
for i, sentence in enumerate(tref):
    print(f"After loading: Input: {sentence}, Predicted: {res[i]}")
