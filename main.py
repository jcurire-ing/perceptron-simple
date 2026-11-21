from src.dataset import training_data
from src.perceptron import Perceptron

model = Perceptron()
model.train(training_data)
prediction = model.predict([9, 1])
print(prediction)
