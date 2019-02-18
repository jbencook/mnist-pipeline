"""
Given a compiled dataset and a model, this module is responsible for training the model.
"""
from typing import Optional

import tensorflow as tf

from .dataset import load_dataset
from .preprocess import preprocess
from .model import classifier


def train(train_path: str, test_path: str, save_path: Optional[str] = None) -> Optional[tf.keras.Model]:
    """Train the model."""
    x_train, y_train = preprocess(*load_dataset(train_path))
    x_test, y_test = preprocess(*load_dataset(test_path))
    model = classifier(x_train)
    model.compile(
        loss=tf.keras.losses.categorical_crossentropy,
        optimizer=tf.keras.optimizers.Adagrad(),
        metrics=['accuracy'],
        target_tensors=[y_train],
    )
    model.fit(
        x_train, y_train,
        verbose=1,
        epochs=2,
        steps_per_epoch=60000 // 128,
    )
    _, accuracy = model.evaluate(
        x_test, y_test,
        verbose=1,
        steps=10000 // 128,
    )
    print(f'Test accuracy: {accuracy:0.3f}')
    if save_path:
        model.save_weights(
            save_path,
            overwrite=True,
        )
        return
    return model
