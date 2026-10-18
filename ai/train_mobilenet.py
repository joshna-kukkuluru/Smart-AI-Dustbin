
import os
import tensorflow as tf

# Dataset and model settings
DATASET_DIR = "ai/datasets"
MODEL_DIR = "ai/models"
IMG_SIZE = (160, 160)
BATCH_SIZE = 8
SEED = 42
EPOCHS = 15

os.makedirs(MODEL_DIR, exist_ok=True)

# Load training images
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

class_names = train_ds.class_names
print("Classes:", class_names)

# Data augmentation for training images
augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.08),
    tf.keras.layers.RandomZoom(0.1),
])

# Load pretrained MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights="imagenet"
)

# Initially freeze pretrained layers
base_model.trainable = False

inputs = tf.keras.Input(shape=(160, 160, 3))
x = augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.3)(x)
outputs = tf.keras.layers.Dense(
    len(class_names), activation="softmax"
)(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train the classification head
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# Save the new model separately
model_path = os.path.join(
    MODEL_DIR, "waste_classifier_mobilenet_v2_new.keras"
)
model.save(model_path)

class_path = os.path.join(
    MODEL_DIR, "class_names_mobilenet_v2_new.txt"
)
with open(class_path, "w") as file:
    file.write("\n".join(class_names))

print("\nTraining completed!")
print("Model saved:", model_path)
print("Classes saved:", class_path)
print("Final training accuracy:",
      round(history.history["accuracy"][-1] * 100, 2), "%")
print("Final validation accuracy:",
      round(history.history["val_accuracy"][-1] * 100, 2), "%")
