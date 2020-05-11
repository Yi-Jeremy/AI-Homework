import numpy as np
from keras.utils.np_utils import to_categorical as toc
from keras.layers import Convolution2D,MaxPooling2D,Dense,Dropout,Flatten,Activation,BatchNormalization
from keras.models import Sequential
from keras.optimizers import Adam,Adadelta

def loadData(mode=True):
    if mode:
        print('Loading data.....')
        trainX,trainY=np.load('trainX.npy')/255,np.load('trainY.npy')
        testX,testY=np.load('testX.npy')/255,np.load('testY.npy')
    else:
        try:
            from keras.datasets import mnist
        except:
            print('请安装Keras库')
            exit(0)
        print('Loading data.....')
        (trainX,trainY),(testX,testY)=mnist.load_data()

    class_num=10
    print('Reshaping training data.....')
    trainX=trainX.reshape(trainX.shape[0],trainX.shape[1],trainX.shape[2],1)
    print('Reshaping validation data.....')
    testX=testX.reshape(testX.shape[0],testX.shape[1],testX.shape[2],1)
    print('Encoding to one-hot label.....')

    trainY,testY=toc(trainY,class_num),toc(testY,class_num)
    return trainX,trainY,testX,testY

def runModel():
    class_num=10
    input_shape=(trainX.shape[1],trainX.shape[2],1)
    model=Sequential()
    model.add(Convolution2D(filters=5,kernel_size=(3,3),padding='same',
                            input_shape=input_shape,activation='relu'))
    model.add(BatchNormalization())
    model.add(Convolution2D(filters=5,kernel_size=(5,5),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Activation('tanh'))
    model.add(Dropout(rate=0.3))
    model.add(Convolution2D(filters=1,kernel_size=(5,5),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    model.add(Dense(12,activation='relu'))
    model.add(Dense(class_num,activation='softmax'))
    ada=Adadelta(lr=2)
    model.compile(loss='categorical_crossentropy',
                  optimizer=ada,
                  metrics=['accuracy'])
    history=model.fit(x=trainX,y=trainY,validation_data=(testX,testY),batch_size=128,epochs=50)
    score=model.evaluate(x=testX,y=testY)
    try:
        print('Score = ',score[0])
        print('Accuracy = ',score[1])
        return score,history
    except:
        return score,history

if __name__=='__main__':
    trainX,trainY,testX,testY=loadData()
    score,history=runModel(False)