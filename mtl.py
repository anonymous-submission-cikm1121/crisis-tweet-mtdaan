from wordvec_utils import *
from models import *
from dataset_utils import *
import copy

def test_st(target,grl_lambda=0.4,dc_weight=0.1):

	train_cat = copy.deepcopy(crisis)
	train_cat.remove(target) # remove target from training

	print("Target: ", target)
	X_train_all = []
	Y_train_all = []
	X_test_all = []
	Y_test_all = []
	for task in tasks:
		X_train, Y_train, X_test, Y_test = create_data4lstm_allvsone_mtl(task, train_cat, target, wv_dict, Tx, Ty, dim=300, min_count=3500)
		X_train_all.append(X_train)
		Y_train_all.append(Y_train)
		X_test_all.append(X_test)
		Y_test_all.append(Y_test)

	X_dc, Y_dc, X_dc_test, X_dc_test  = create_data4lstm_DA_mtl(train_cat, wv_dict, Tx, Ty, dim=300, min_count=700)
	X_train_all.append(X_dc)
	Y_train_all.append(Y_dc)
	#X_test_all.append(X_test)
	#Y_test_all.append(Y_test)


	modelx = train_mtl(X_train_all, Y_train_all, Tx, Ty, epochs=epochs, dc_out_dim=len(train_cat),grl_lambda=grl_lambda, dc_weight=dc_weight, wv_dim=300)
	acc,f1 = evaluate_bilstm_attention_mtl(modelx, X_test_all, Y_test_all)

	print("Accuracy: ", acc)

### START 
Tx = 40 # Number of words
Ty = 1 # Binary Classifier / Final Output
epochs = 1

tasks = ['priority','Factoid','Sentiment','Irrelevant']
crisis = ['guatemalaEarthquake','typhoonYolanda','australiaBushfire','bostonBombings','queenslandFloods','chileEarthquake','typhoonHagupit','nepalEarthquake','parisAttacks','flSchoolShooting']

target = sys.argv[1]
word2vec_file = 'trec.vec'
wv_dict = wordvec_dict(word2vec_file, binary=False) # Change this to True if you are using a bin file.
test_st(target,grl_lambda=0.4,dc_weight=0.1) # grl_lambda and dc_weight are gradient reversal/domain classifier hyperparameters

