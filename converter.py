def convert_eng_to_heb(text):
    """
    Converts English QWERTY key presses to their Hebrew keyboard equivalents.
    Useful for when a user typed in English but meant to type in Hebrew.
    """
    mapping = {
        'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ', '[': ']', ']': '[',
        'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף', "'": ',',
        'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ', '/': '.',
        # Uppercase
        'Q': '/', 'W': "'", 'E': 'ק', 'R': 'ר', 'T': 'א', 'Y': 'ט', 'U': 'ו', 'I': 'ן', 'O': 'ם', 'P': 'פ', '{': '}', '}': '{',
        'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י', 'J': 'ח', 'K': 'ל', 'L': 'ך', ':': 'ף', '"': ',',
        'Z': 'ז', 'X': 'ס', 'C': 'ב', 'V': 'ה', 'B': 'נ', 'N': 'מ', 'M': 'צ', '<': 'ת', '>': 'ץ', '?': '.',
        # Mirrored brackets
        '(': ')', ')': '(',
    }
    
    converted = ""
    for char in text:
        converted += mapping.get(char, char)
    return converted

def convert_heb_to_eng(text):
    """
    Converts Hebrew keyboard key presses to their English QWERTY equivalents.
    Useful for when a user typed in Hebrew but meant to type in English.
    """
    mapping = {
        '/': 'q', "'": 'w', 'ק': 'e', 'ר': 'r', 'א': 't', 'ט': 'y', 'ו': 'u', 'ן': 'i', 'ם': 'o', 'פ': 'p', ']': '[', '[': ']',
        'ש': 'a', 'ד': 's', 'ג': 'd', 'כ': 'f', 'ע': 'g', 'י': 'h', 'ח': 'j', 'ל': 'k', 'ך': 'l', 'ף': ';', ',': "'",
        'ז': 'z', 'ס': 'x', 'ב': 'c', 'ה': 'v', 'נ': 'b', 'מ': 'n', 'צ': 'm', 'ת': ',', 'ץ': '.', '.': '/',
        # Brackets mirrored
        ')': '(', '(': ')',
    }
    
    converted = ""
    for char in text:
        converted += mapping.get(char, char)
    return converted

if __name__ == "__main__":
    # Test
    print(f"Eng to Heb: 'akuo' -> {convert_eng_to_heb('akuo')}")
    print(f"Heb to Eng: 'שלום' -> {convert_heb_to_eng('שלום')}") # This is slightly wrong because of standard mapping, let's test specific chars
    print(f"Heb to Eng: 'אקעם' -> {convert_heb_to_eng('אקעם')}") # Should be 't e g o'
