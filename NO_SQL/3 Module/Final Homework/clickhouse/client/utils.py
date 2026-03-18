def format_percentage(value, total):
    if total == 0:
        return "0.0%"
    return f"{(value / total * 100):.1f}%"

def truncate_string(s, max_length=50):
    if len(s) <= max_length:
        return s
    return s[:max_length-3] + "..."

def grade_to_letter(grade):
    if grade >= 5:
        return 'A'
    elif grade >= 4:
        return 'B'
    elif grade >= 3:
        return 'C'
    else:
        return 'F'
