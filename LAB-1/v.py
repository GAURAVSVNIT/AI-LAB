import sys

def solve_final():
    # Ciphertext from challenge
    ciphertext = " VSXNXYNEEUEIVF"
    
    # Derived Keys from 'cheddar' -> 'DAHSSZU'
    # a = 15, b = 25
    a = 15
    b = 25
    
    # Calculate modular inverse of a (15) mod 26
    # 15 * x = 1 (mod 26) -> x = 7
    a_inv = 7 
    
    plaintext = ""
    for char in ciphertext:
        y = ord(char) - ord('A')
        # Decrypt: x = a_inv * (y - b)
        x = (a_inv * (y - b)) % 26
        plaintext += chr(x + ord('A'))
        
    print(f"[-] Raw Decrypted (Upper): {plaintext}")
    print(f"[-] Raw Decrypted (Lower): {plaintext.lower()}")
    
    # Check for Rotational Ciphers (Just in case 'BLEEC' -> 'BLUE' or similar)
    print("\n--- Checking Shifts (Caesar) ---")
    for s in range(1, 26):
        shifted = ""
        for char in plaintext:
            val = ord(char) - ord('A')
            shifted += chr(((val + s) % 26) + ord('A'))
        # Heuristic: Check if 'CHEESE' or 'BLUE' appears
        if "CHEESE" in shifted or "BLUE" in shifted or "RAT" in shifted:
            print(f"Shift +{s}: {shifted} <--- POSSIBLE MATCH?")

if __name__ == "__main__":
    solve_final()