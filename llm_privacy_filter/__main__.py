from .core import Masker

if __name__ == "__main__":
    masker = Masker()
    text = "Dr. Jane A. Smith, a senior researcher at MIT, was born on March 12, 1985. She can be reached at jane.smith@example.com or +1-202-555-0198. She lives at 45 Cherry Street, Boston, MA, and holds a US passport number X1234567."
    print(masker.mask_text(text))
