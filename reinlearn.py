from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from keras import Sequential
from keras.layers import Dense

import json

# create X and y

with open('boards.json', 'r') as f:
    data = json.load(f)
    
x = []
y = []

for board in data['board']:
    
    board_info = []
    
    for i in range(len(board) - 1):
        square = board[i]
        for s in square:
            board_info.append(s)
    
    board_info.append(board[-1])
    
    x.append(board_info)
    
for start_square in data['start']:
    y.append(start_square)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

# set up network

classifier = Sequential()
#First Hidden Layer
classifier.add(Dense(512, activation='relu', kernel_initializer='random_normal', input_dim=8)) # change input_dim
#Second  Hidden Layer
classifier.add(Dense(256, activation='relu', kernel_initializer='random_normal'))
#Output Layer
classifier.add(Dense(64, activation='softmax', kernel_initializer='random_normal'))

#Compiling the neural network
classifier.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])

#Fitting the data to the training dataset
classifier.fit(X_train,y_train, batch_size=10, epochs=100)

eval_model=classifier.evaluate(X_train, y_train)
eval_model

