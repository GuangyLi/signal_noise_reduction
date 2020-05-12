# Machine learning related
from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Nerual Network related
import keras
from keras import layers
from keras.layers import Input,Reshape,ZeroPadding2D,Conv2D,Dropout,Flatten,Dense,Activation,MaxPooling2D,AlphaDropout,BatchNormalization
import keras.models as Model
from keras.regularizers import *
from keras.optimizers import adam
from keras.applications.vgg16 import VGG16
import tensorflow as tf

data_format = 'channels_first'

#======================================================================================
#============================CNN Sequence Generator====================================
#======================================================================================
def cnn_stack(Cn,kernel_size,Seq,pool_size,act,add_batch=False):
    Seq_str = "Layer%d" %Seq # String to print out
    
    # Change number of filters based on feature size
    if Seq < 0:
        filter_num = 32
    elif Seq < 3:
        filter_num = 64
    else:
        filter_num = 128
    
    # Each sequence will have at least two conv2d layer
    Cn = Conv2D(filter_num, kernel_size, padding='same', name=Seq_str+"_conv1", kernel_initializer='glorot_normal',data_format=data_format,activation=act)(Cn)
    Cn = Conv2D(filter_num, kernel_size, padding='same', name=Seq_str+"_conv2", kernel_initializer='glorot_normal',data_format=data_format,activation=act)(Cn)

    # Add one layer of conv2d after 3 sequences
    if Seq > 3:
        Cn = Conv2D(filter_num, kernel_size, padding='same', name=Seq_str+"_conv3", kernel_initializer='glorot_normal',data_format=data_format,activation=act)(Cn)
    
    # Add a batchnormal layer
    if add_batch:
        Cn = BatchNormalization()(Cn)
    
    # Add a pooling layer to decrease size
    Cn = MaxPooling2D(pool_size=pool_size, strides=pool_size, padding='valid', data_format=data_format)(Cn)

    return Cn


#======================================================================================
#==========================Model Modified from VGG16===================================
#======================================================================================
def VGG_result(X_train, X_test, y_train_reshaped, y_test_reshaped, data_length, label_num, train=True, retrain=False, model_name="auto"):
    p_testdata = []
    
    #============================Generate Model=================================
    act_temp = "relu"
    act_temp_dense = "selu"
    
    in_shp = X_train.shape[1:]
    #input layer
    Cn_input = Input(in_shp)
    Cn = Reshape([1,data_length,1], input_shape=in_shp)(Cn_input)
    #CNN Stack
    Cn = cnn_stack(Cn,kernel_size=(5,1),Seq=0,pool_size=(2,1),act=act_temp,add_batch=True)   #output shape:(64,512,1)
    Cn = cnn_stack(Cn,kernel_size=(3,1),Seq=1,pool_size=(2,1),act=act_temp,add_batch=False)   #output shape:(64,256,1)
    Cn = cnn_stack(Cn,kernel_size=(3,1),Seq=2,pool_size=(2,1),act=act_temp,add_batch=False)   #output shape:(64,128,1)
    Cn = cnn_stack(Cn,kernel_size=(3,1),Seq=3,pool_size=(2,1),act=act_temp,add_batch=False)   #output shape:(128,64,1)
    Cn = cnn_stack(Cn,kernel_size=(3,1),Seq=4,pool_size=(2,1),act=act_temp,add_batch=False)   #output shape:(128,32,1)
    Cn = cnn_stack(Cn,kernel_size=(3,1),Seq=5,pool_size=(2,1),act=act_temp,add_batch=False)   #output shape:(128,16,1)
    Cn = cnn_stack(Cn,kernel_size=(3,1),Seq=6,pool_size=(2,1),act=act_temp,add_batch=False)   #output shape:(128,8,1)
    #Full Con 1-3
    Cn = Flatten(data_format=data_format)(Cn)
    Cn = Dense(128, activation=act_temp_dense, kernel_initializer='glorot_normal', name="dense1")(Cn)
    Cn = AlphaDropout(0.3)(Cn)
    Cn = Dense(128, activation=act_temp_dense, kernel_initializer='glorot_normal', name="dense2")(Cn)
    Cn = AlphaDropout(0.3)(Cn)
    Cn = Dense(label_num, activation='softmax', kernel_initializer='glorot_normal', name="dense3")(Cn)
    
    print("\n==========================================================\n")
    print("Input Shape is " + str(Cn_input) + ".\n")
    print("Output Shape is " + str(Cn) + ".\n")
    
    #Create Model
    model = Model.Model(inputs=Cn_input,outputs=Cn)

    # Two optimizer to choose
    if retrain:
        learn_rate = 0.00001
        patience = 10
    else:
        learn_rate = 0.0005
        patience = 50

    adam = keras.optimizers.Adam(lr=learn_rate, beta_1=0.9, beta_2=0.999)
    nadam = keras.optimizers.Nadam()
    model.compile(loss='categorical_crossentropy', metrics = ['accuracy'], optimizer=adam)

    model.summary()
    
    # ====================Training=======================
    
    batch_size_tmp = 512
    if model_name == "auto":
        filepath_loss = 'model_history/Model_cnn_loss_new.h5'
        filepath_acc = 'model_history/Model_cnn_acc_new.h5'
    else:
        filepath_loss = 'model_history/Model_cnn_loss%s.h5' %model_name
        filepath_acc = 'model_history/Model_cnn_acc%s.h5' %model_name
    checkpoint_loss = keras.callbacks.ModelCheckpoint(filepath_loss, monitor='val_loss', verbose=0, save_best_only=True, mode='auto')
    checkpoint_acc = keras.callbacks.ModelCheckpoint(filepath_acc, monitor='val_accuracy', verbose=0, save_best_only=True, mode='max')

    if retrain:
        model.load_weights(filepath_acc)
    
    # Training for 300 epoch and store the one with lowest val_loss, early stop after certain epoch without loss decrease
    if train:
        history = model.fit(X_train, y_train_reshaped,
            batch_size=batch_size_tmp,
            epochs=300,
            verbose=2,
            validation_data=(X_test, y_test_reshaped),
            #validation_split = 0.2,
            callbacks = [checkpoint_loss, checkpoint_acc,
                keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=patience)
                ]        
            )
    
    print("\n========Epoch Ends========\n")
    # Load the stored model with min loss
    model.load_weights(filepath_loss)

    # Predict both train and test result and estimate accuracy
    p_train_loss = model.predict(X_train, batch_size=batch_size_tmp)
    p_test_loss = model.predict(X_test, batch_size=batch_size_tmp)

    # Load the stored model with min loss
    model.load_weights(filepath_acc)

    p_train_acc = model.predict(X_train, batch_size=batch_size_tmp)
    p_test_acc = model.predict(X_test, batch_size=batch_size_tmp)
    
    return p_train_loss, p_test_loss, p_train_acc, p_test_acc