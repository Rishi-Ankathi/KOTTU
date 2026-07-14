from src.train import Trainer
from src.evaluate import Evaluator

trainer = Trainer()

history, model, X_test, y_test = trainer.train()

evaluator = Evaluator()

accuracy, report, matrix = evaluator.evaluate(
    model,
    X_test,
    y_test
)