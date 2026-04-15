import sys

def solve():
    print("--- Affine Cipher Solver ---")
    
    # 1. Input the known ciphertext for "cheddar"
    print("In the netcat terminal, encrypt the cheese: cheddar")
    encrypted_cheddar = input("Enter the result (7 characters): ").strip().upper()
    
    if len(encrypted_cheddar) != 7:
        print("Error: The encrypted output for 'cheddar' should be 7 characters.")
        return

    known_plain = "CHEDDAR"
    target_cipher = " VSXNXYNEEUEIVF" # From your challenge description
    
    # 2. Find keys 'a' and 'b' that match the transformation
    # Equation: Cipher = (a * Plain + b) % 26
    
    found_key = None
    
    # 'a' must be coprime to 26 (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
    valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    
    print("\nAttempting to crack Linear Equation parameters...")
    
    for a in valid_a:
        for b in range(26):
            is_match = True
            for i in range(len(known_plain)):
                p_val = ord(known_plain[i]) - ord('A')
                c_val = ord(encrypted_cheddar[i]) - ord('A')
                
                # Check if this (a, b) pair works for this character
                if (a * p_val + b) % 26 != c_val:
                    is_match = False
                    break
            
            if is_match:
                found_key = (a, b)
                break
        if found_key:
            break
            
    if not found_key:
        print("[-] Could not find a valid Linear Equation match. Is the cipher actually Hill/Vigenere?")
        return

    a, b = found_key
    print(f"[+] Key Found! a = {a}, b = {b}")
    print(f"[+] Equation: y = {a}x + {b} (mod 26)")

    # 3. Decrypt the Secret Cheese
    # Decryption: P = a_inv * (C - b) % 26
    
    # Calculate modular inverse of a
    a_inv = pow(a, -1, 26)
    
    decrypted_cheese = ""
    for char in target_cipher:
        c_val = ord(char) - ord('A')
        p_val = (a_inv * (c_val - b)) % 26
        decrypted_cheese += chr(p_val + ord('A'))
        
    print(f"\n*******************************************")
    print(f" SECRET CHEESE: {decrypted_cheese}")
    print(f"*******************************************")
    print("Action: Copy the SECRET CHEESE above and select '(g)uess my cheese'!")

if __name__ == "__main__":
    solve()