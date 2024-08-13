def snake_case_to_pascal_case(string: str) -> str:
    characters = string.split('_')
    return string if len(characters) == 1 else ''.join(char.capitalize() for char in characters)
