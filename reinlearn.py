from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from keras import Sequential
from keras.layers import Dense

import json

# create X and y

with open('boards.json', 'r') as f:
    data = json.load(f)
    
x_start = []
y_start = []
x_end = []
y_end = []

for n in range(len(data['board'])):
    
    board = data['board'][n]
    board_info = []
    board_info_with_start = []
    
    for i in range(len(board) - 1):
        square = board[i]
        for s in square:
            board_info.append(s)
            board_info_with_start.append(s)
    
    board_info.append(board[-1])
    board_info_with_start.append(board[-1])
    
    x_start.append(board_info)
    
    start_square = data['start'][n]
    end_square = data['end'][n]
    
    y_start.append(start_square)
    y_end.append(end_square)
    
    for s in start_square:
        board_info_with_start.append(s)
        
    x_end.append(board_info_with_start)
        

# network 1: get starting square from board        

X_train, X_test, y_train, y_test = train_test_split(x_start, y_start, test_size=0.3)

classifier_start = Sequential()
#First Hidden Layer
classifier_start.add(Dense(512, activation='relu', kernel_initializer='random_normal', input_dim=833)) # change input_dim
#Second  Hidden Layer
classifier_start.add(Dense(256, activation='relu', kernel_initializer='random_normal'))
#Output Layer
classifier_start.add(Dense(64, activation='softmax', kernel_initializer='random_normal'))

#Compiling the neural network
classifier_start.compile(optimizer ='adam',loss='categorical_crossentropy', metrics =['accuracy'])

#Fitting the data to the training dataset
classifier_start.fit(X_train,y_train, batch_size=10, epochs=50)


# network 2: get ending square from board and starting square    

X_train, X_test2, y_train, y_test2 = train_test_split(x_end, y_end, test_size=0.3)

classifier_end = Sequential()
#First Hidden Layer
classifier_end.add(Dense(512, activation='relu', kernel_initializer='random_normal', input_dim=897)) # change input_dim
#Second  Hidden Layer
classifier_end.add(Dense(256, activation='relu', kernel_initializer='random_normal'))
#Output Layer
classifier_end.add(Dense(64, activation='softmax', kernel_initializer='random_normal'))

#Compiling the neural network
classifier_end.compile(optimizer ='adam',loss='categorical_crossentropy', metrics =['accuracy'])

#Fitting the data to the training dataset
classifier_end.fit(X_train,y_train, batch_size=10, epochs=50)


# evaluation

classifier_start.save("start_net")
classifier_end.save("end_net")

eval_model=classifier_start.evaluate(X_test, y_test)
eval_model
print(eval_model)

eval_model=classifier_end.evaluate(X_test2, y_test2)
eval_model
print(eval_model)