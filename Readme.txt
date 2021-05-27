Teste 1	- Apenas treino

	- Utiliza o ImageDataGenerator e o data_generator
	- Normalização dividindo por 255
	- Separando 30% para validação

	- Rede neural convolucional
	  - Primeira camada
	    - Conv2D 64 com relu
	    - Tamanho do Downsampling utilizando MaxPooling2D com tamanho 2
	    - Dropout de 30%
	  - Segunda camada
	    - Conv2D 128 com relu
	    - Tamanho do Downsampling utilizando MaxPooling2D com tamanho 2
	    - Dropout de 30%
	  - Transforma em um array com o Flatten
	  - Terceira camada
	    - Dense 256 com relu
	    - Dropout 50%
	  - Camada de saida
	    - Dense 2 com sigmoid

	- Optimizer adam
	- Loss binary_crossentropy
	- Treino usando o fit_genarator

	- Treinamendo com 50 épocas
	- Checkpoint no menor valor do val_loss
	- Salva o arquivo em .hdf5
	- Early Stop quando o val_loss ficar 5 épocas sem melhorar
	
	Resultado do Treino
	- Épocas rodadas: 10
	- Época salva: 5ª
	  - loss: 0.5697
	  - val_loss: 0.5946
	  - accuracy: 0.7153
	  - val_accuracy: 0.7280