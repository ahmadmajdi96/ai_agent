# fast_api/utils.py

def is_valid_email(email: str) -> bool:
    """
    Check if the provided email address is valid.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    # Regular expression for validating an Email
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email) is not None

def to_camel_case(snake_str: str) -> str:
    """
    Convert a snake_case string to camelCase.
    
    Args:
        snake_str (str): The snake_case string to convert.
        
    Returns:
        str: The converted camelCase string.
    """
    components = snake_str.split('_')
    # Capitalize the first letter of each component except the first one
    return components[0] + ''.join(x.title() for x in components[1:])

def get_current_timestamp() -> int:
    """
    Get the current timestamp in seconds since the epoch.
    
    Returns:
        int: The current timestamp.
    """
    import time
    return int(time.time())

def format_bytes(size: int) -> str:
    """
    Format a number of bytes into a human-readable string.
    
    Args:
        size (int): The number of bytes to format.
        
    Returns:
        str: A human-readable string representing the size.
    """
    # Define suffixes for different sizes
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    if size == 0:
        return "0 B"
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size /= 1024.0
        i += 1
    return f"{size:.2f} {suffixes[i]}"