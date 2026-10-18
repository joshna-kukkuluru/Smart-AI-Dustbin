
import os
import tensorflow as tf

# Dataset location
DATASET_DIR = "ai/datasets"

IMG_SIZE = (160, 160)
BATCH_SIZE = 8
SEED = 42
EPOCHS = 15

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

# Load validation images
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

# Improve input pipeline performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(100).prefetch(
    buffer_size=AUTOTUNE
)
val_ds = val_ds.cache().prefetch(
    buffer_size=AUTOTUNE
)

# Small CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(160, 160, 3)),
    tf.keras.layers.Rescaling(1.0 / 255),

    tf.keras.layers.Conv2D(
        16, 3, activation="relu"
    ),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(
        32, 3, activation="relu"
    ),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(
        64, 3, activation="relu"
    ),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(
        len(class_names), activation="softmax"
    )
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# Save model and class names
os.makedirs("ai/models", exist_ok=True)

model.save("ai/models/waste_classifier.keras")

with open("ai/models/class_names.txt", "w") as file:
    file.write("\n".join(class_names))

print("Training completed!")
print("Model saved to ai/models/waste_classifier.keras")
print("Class names saved.")
