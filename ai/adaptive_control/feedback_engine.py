import os
import json

class FeedbackEngine:
    def __init__(self):
        self.feedback_log = []

    def record_outcome(self, tick: int, action_id: int, action_type: str, target: str, predicted_reduction: float, actual_reduction: float):
        """
        Records the outcome of an intervention.
        Computes the prediction error.
        """
        error = abs(predicted_reduction - actual_reduction)
        error_percent = 0.0
        if predicted_reduction > 0:
            error_percent = (error / predicted_reduction) * 100.0
            
        entry = {
            "tick": tick,
            "action_id": action_id,
            "type": action_type,
            "target": target,
            "predicted_reduction": predicted_reduction,
            "actual_reduction": actual_reduction,
            "error": error,
            "error_percent": error_percent
        }
        self.feedback_log.append(entry)
        
        # Write to datasets
        os.makedirs("datasets", exist_ok=True)
        log_path = os.path.join("datasets", "layer6_feedback_log.jsonl")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_summary(self) -> dict:
        """
        Returns average feedback metrics.
        """
        if not self.feedback_log:
            return {"avg_error": 0.0, "avg_error_percent": 0.0, "total_records": 0}
            
        total_err = sum(item["error"] for item in self.feedback_log)
        total_err_pct = sum(item["error_percent"] for item in self.feedback_log)
        n = len(self.feedback_log)
        
        return {
            "avg_error": float(total_err / n),
            "avg_error_percent": float(total_err_pct / n),
            "total_records": n
        }
