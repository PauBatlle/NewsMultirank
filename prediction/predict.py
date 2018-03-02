import pickle
import tensorflow as tf
from util import *
from keras.models import load_model
from keras.backend import clear_session
def doPredict(body, title):
    # MISLEAD

    tf.reset_default_graph()

    # Add ops to save and restore all the variables.
    interpretation = ["Agrees", "Disagrees", "Discusses", "Unrelated"]

    feature_size = 10001
    hidden_size = 100
    target_size = 4

    features_pl = tf.placeholder(tf.float32, [None, feature_size], 'features')
    stances_pl = tf.placeholder(tf.int64, [None], 'stances')
    keep_prob_pl = tf.placeholder(tf.float32)
    batch_size = tf.shape(features_pl)[0]
    hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, hidden_size)), keep_prob=keep_prob_pl)
    logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer, target_size), keep_prob=keep_prob_pl)
    logits = tf.reshape(logits_flat, [batch_size, target_size])
    softmaxed_logits = tf.nn.softmax(logits)
    predict = tf.argmax(softmaxed_logits, 1)
    saver = tf.train.Saver()

    bow_vectorizer = pickle.load((open("BoW.p", 'rb')))
    tfreq_vectorizer = pickle.load((open("Tfreq.p", 'rb')))
    tfidf_vectorizer = pickle.load((open("Tfidf.p", 'rb')))

    file_test_instances = "Training_Datasets/test_stances_unlabeled.csv"
    file_test_bodies = "Training_Datasets/test_bodies.csv"

    raw_test = FNCData(title, body, one_sentence=True)
    test_set = pipeline_test(raw_test, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)

    with tf.Session() as sess:
        # Restore variables from disk.
        saver.restore(sess, "../Pretrained_models/misleadmodel.ckpt")

        test_feed_dict = {features_pl: test_set, keep_prob_pl: 1.0}

        scores, prediction = sess.run([softmaxed_logits, predict], feed_dict=test_feed_dict)

    
    clear_session()
    #Clickbait

    cbmodel = load_model('../Pretrained_models/Clickbaitv3.h5')
    tfidf = pickle.load(open("tfidf_clickbait.p", "rb"))
    s = np.array([title])
    clickbait_score = cbmodel.predict(tfidf.transform(s).todense())[0,0]

    return scores, interpretation[prediction[0]], clickbait_score
