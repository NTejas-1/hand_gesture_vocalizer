Directions to implement the project:

connect 5 flex sensor to a0, a1, a2, a3 and a6 of arduino and connect mpu600 to rx and tx of arduino. Use the code "collect_data" and collect around 1000 samples for each letter in the alphabet. For example run the code to print 1000 samples for A, copy the samples from the output window and paste it into a csv file, after that change the letter 'A' in the 94th line of 'collect_data' code to B and then collect 1000 samples for B. repeat the same for all the alphabet.name the csv file as 'raw_data.csv'. 

now use 'train_model' code to train the model over the data in 'raw_data.csv' file. the code will print the weights and biases at the end. If cost and losses are close to 0 continue... else train the model again with more epochs or more neuron in the hidden layer.

copy the weghts and biases and past them in the 'predict_letter_and_convert_to_voice' code as constant matrix at global level. 'predict_letter_and_convert_to_voice' code will perform forward propagation to predict the alphabet and transmit it via BlueTooth.
