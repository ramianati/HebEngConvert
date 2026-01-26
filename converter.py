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
        'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י', 'J': 'ח', 'K': 'ל', 'L': 'ך', 
        # Shifted symbols that stay same or follow layout
        ':': ':', '"': '"', '<': '<', '>': '>', '?': '?',
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

def test_all_cases():
    """ Runs a comprehensive suite of tests for the converter """
    try:
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

    test_cases = [
        # (Input, Expected Heb, Expected Eng)
        ("akuo", "שלום", "שךואם"),
        ("אקערטי", "אקערטי", "qwerty"),
        ("123!@#", "123!@#", "123!@#"),
        ("akuo kfuko' nv vgbhhbho?", "שלום לכולם, מה העניינים?", "שךואם ךכואם, מה העמיימים?"),
        ("Punctuation: , . / ; ' [ ]", "פונבחואבהין: ת ץ . ף , ] [", "Punctuation: , . / ; ' [ ]"),
        ("Hello, World!", "הללך, וךךקד!", "Hello, World!"),
        ("Mirrored Brackets ( ) [ ]", "מיהיהקיהבד בקשבלעקד ) ( ] [", "Mirrored Brackets ( ) [ ]"),
    ]
    
    print(f"{'Input':<30} | {'Output (To Heb)':<30} | {'Output (To Eng)':<30}")
    print("-" * 100)
    for inp, res_heb, _ in test_cases: # Simple iteration
        res_heb = convert_eng_to_heb(inp)
        res_eng = convert_heb_to_eng(inp)
        try:
            print(f"{inp:<30} | {res_heb:<30} | {res_eng:<30}")
        except:
            print(f"{inp:<30} | [Encoding Error] | [Encoding Error]")

if __name__ == "__main__":
    test_all_cases()
