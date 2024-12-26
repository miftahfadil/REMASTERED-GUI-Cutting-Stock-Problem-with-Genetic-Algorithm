def validate_entry_len(value: str) -> bool:
    if value == "":
        return True
    
    try:
        float(value)

    except ValueError:
        return False
    
    return True

def validate_entry_amt(value: str) -> bool:
    if value == "":
        return True
    
    try:
        int(value)
        
    except ValueError:
        return False
    
    return True