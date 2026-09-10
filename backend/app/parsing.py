import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorSignature:
    failing_step: str
    exception_type: str
    relevant_lines: list[str]
    stack_trace: str

    @property
    def text(self) -> str:
        parts = [f"Failing step: {self.failing_step}", f"Exception: {self.exception_type}"]
        if self.relevant_lines:
            parts.append("Relevant lines:\n" + "\n".join(self.relevant_lines))
        if self.stack_trace:
            parts.append("Stack trace:\n" + self.stack_trace)
        return "\n".join(parts)


def extract_error_signature(log_text: str) -> ErrorSignature:
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    step = "unknown step"
    for line in lines:
        match = re.search(r"(?:step|job|stage)\s*[:\-]\s*(.+)", line, re.I)
        if match:
            step = match.group(1).strip()
        elif line.startswith("##["):
            step = line.strip("#[] ")
    error_lines = [
        line
        for line in lines
        if re.search(r"error|exception|failed|failure|importerror|traceback", line, re.I)
    ]
    exception = "unknown error"
    for line in error_lines:
        match = re.search(r"([A-Za-z_][\w.]*(?:Error|Exception|Failure|Timeout))\b", line)
        if match:
            exception = match.group(1)
            break
    traceback_lines: list[str] = []
    in_traceback = False
    for line in lines:
        if "traceback" in line.lower():
            in_traceback = True
        if in_traceback:
            traceback_lines.append(line)
    relevant = error_lines[:6]
    return ErrorSignature(step, exception, relevant, "\n".join(traceback_lines[:20]))
