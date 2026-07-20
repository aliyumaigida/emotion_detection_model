import tensorflow as tf

# model = tf.keras.models.load_model("ai_model/emotion_mobilenetv2.keras")
model = tf.keras.models.load_model("ai_model/emotion_model.keras")
model.summary()