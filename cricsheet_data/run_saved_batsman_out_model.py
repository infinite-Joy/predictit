
from keras.models import model_from_json

model = model_from_json(open('my_model_architecture.json').read())
model.load_weights('my_model_weights.h5')

# Finally, before it can be used, the model shall be compiled.
model.compile(optimizer='adagrad', loss='mse')
