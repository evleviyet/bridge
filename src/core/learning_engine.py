"""
Simple learning engine using basic statistical methods.
"""
from typing import List
import statistics

class LearningEngine:
    def __init__(self):
        self.data: List[float] = []
        
    def train(self, data: List[float]) -> None:
        """Train the model with numerical data."""
        self.data = data
        
    def predict(self, value: float) -> float:
        """Make a simple prediction using mean-based approach."""
        if not self.data:
            return value
        mean = statistics.mean(self.data)
        return (value + mean) / 2