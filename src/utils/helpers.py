def clean_text(text):
    """Cleans the input text by removing unnecessary whitespace and special characters."""
    return ' '.join(text.split())

def format_summary(summary):
    """Formats the summary text for display."""
    return summary.strip()

def log_error(error_message):
    """Logs error messages for debugging purposes."""
    with open('error.log', 'a') as f:
        f.write(f"{error_message}\n")