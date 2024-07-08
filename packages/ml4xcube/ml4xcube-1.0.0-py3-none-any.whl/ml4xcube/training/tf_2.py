import numpy as np
import tensorflow as tf
from typing import Union

class Trainer:
    """
    A trainer class for training TensorFlow models on single or no GPU systems.
    """
    def __init__(
            self,
            model: tf.keras.Model,
            train_data: tf.data.Dataset,
            test_data: tf.data.Dataset,
            optimizer: Union[tf.keras.optimizers.Optimizer, str],
            best_model_path: str,
            learning_rate: float = 0.001,
            loss: Union[tf.keras.losses.Loss, str] = "mean_squared_error",
            early_stopping: bool = True,
            patience: int = 10,
            metrics: list = ['mean_squared_error'],
            tf_log_dir: str = './logs',
            mlflow_run=None,
            summary: bool = False,
            epochs: int = 100,
    ) -> None:
        self.model = model
        self.train_data = train_data
        self.test_data = test_data
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.best_model_path = best_model_path
        self.loss = loss
        self.max_epochs = epochs
        self.early_stopping = early_stopping
        self.patience = patience
        self.metrics = metrics
        self.tf_log_dir = tf_log_dir
        self.mlflow_run = mlflow_run
        self.summary = summary

        # Initialize the optimizer if it's provided as a string
        if isinstance(self.optimizer, str):
            self.optimizer = tf.keras.optimizers.get(self.optimizer)
        elif not isinstance(self.optimizer, tf.keras.optimizers.Optimizer):
            raise ValueError("Optimizer should be either a string or an instance of tf.keras.optimizers.Optimizer")

        # Compile the model
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.metrics)
        self.model.optimizer.learning_rate.assign(self.learning_rate)

        if self.summary:
            self.model.summary()

    @tf.function
    def train_step(self, X_batch, y_batch):
        with tf.GradientTape() as tape:
            predictions = self.model(X_batch, training=True)
            loss = self.model.compiled_loss(y_batch, predictions)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.model.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return loss

    @tf.function
    def test_step(self, X_batch, y_batch):
        predictions = self.model(X_batch, training=False)
        loss = self.model.compiled_loss(y_batch, predictions)
        for metric in self.model.metrics:
            metric.update_state(y_batch, predictions)
        metric_results = {metric.name: metric.result() for metric in self.model.metrics}
        print('============================================================')
        print(loss)
        print('==================================')
        print(metric_results)
        print('==================================')
        print(metric_results['compile_metrics'])
        print('============================================================')
        return loss, metric_results['compile_metrics']

    def train(self):
        callbacks = [
            tf.keras.callbacks.TensorBoard(log_dir=self.tf_log_dir, histogram_freq=1)
        ]

        if self.early_stopping:
            callbacks.append(tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.patience,
                verbose=1,
                mode='min',
                restore_best_weights=True
            ))

        if self.best_model_path:
            callbacks.append(tf.keras.callbacks.ModelCheckpoint(
                self.best_model_path,
                monitor='val_loss',
                save_best_only=True,
                mode='min'
            ))

        for callback in callbacks:
            callback.set_model(self.model)

        for epoch in range(self.max_epochs):
            print(f"Epoch {epoch + 1}/{self.max_epochs}")
            # Training loop
            for step, (X_batch, y_batch) in enumerate(self.train_data):
                if tf.size(X_batch) == 0 or tf.size(y_batch) == 0:
                    continue
                self.train_step(X_batch, y_batch)

            for metric in self.model.metrics:
                metric.reset_state()

            # Validation loop
            total_val_loss = 0.0
            total_samples = 0
            total_val_metrics = {}

            for step, (X_batch, y_batch) in enumerate(self.test_data):
                if tf.size(X_batch) == 0 or tf.size(y_batch) == 0:
                    continue
                loss, metric_results = self.test_step(X_batch, y_batch)
                print(loss)
                print(metric_results)
                batch_size = tf.shape(X_batch)[0]
                total_val_loss += loss * tf.cast(batch_size, tf.float32)
                total_samples += tf.cast(batch_size, tf.float32)
                for name, result in metric_results.items():
                    if name not in total_val_metrics:
                        total_val_metrics[name] = 0.0
                    total_val_metrics[name] += result.numpy() * tf.cast(batch_size, tf.float32).numpy()

            avg_val_loss = total_val_loss / total_samples
            avg_val_metrics = {name: total / total_samples for name, total in total_val_metrics.items()}

            avg_val_loss = avg_val_loss.numpy()
            avg_val_metrics = {name: metric for name, metric in avg_val_metrics.items()}

            print(f"Validation loss: {avg_val_loss}, Validation metrics: {avg_val_metrics}")

            for callback in callbacks:
                callback.on_epoch_end(epoch, logs={'val_loss': avg_val_loss, **avg_val_metrics})

            # Check if early stopping should stop training
            if self.early_stopping and hasattr(callbacks[1], 'stop_training') and callbacks[1].stop_training:
                print(f"Early stopping at epoch {epoch + 1}")
                break

        if self.mlflow_run:
            self.mlflow_run.log_artifact(self.best_model_path, "model")

        return self.model
