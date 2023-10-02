import argparse
from os import cpu_count

class RailFence:
    def __init__(self):
        pass

    def encrypt(self, plaintext):
        rail1 = []
        rail2 = []
        encrypt_text = ""

        for i, char in enumerate(plaintext):
            if i % 2 != 0:
                rail1.append(char)
            elif i % 2 == 0:
                rail2.append(char)
            else:
                rail1.append(char)

        encrypt_text = ''.join(rail2) + ''.join(rail1)
        return encrypt_text

    def decrypt(self, ciphertext):
        rail1_length = len(ciphertext) // 2
        rail1 = list(ciphertext[:rail1_length])
        rail2 = list(ciphertext[rail1_length:])
        decrypt_text = []

        for i in range(len(ciphertext)):
            if i % 2 == 0:
                decrypt_text.append(rail1.pop(0))
            else:
                decrypt_text.append(rail2.pop(0))

        return ''.join(decrypt_text)

class Substition:


  

   def __init__(self,password):
       password=password.lower()
       newKeyword = ''
       for ch in password:
            if ch not in newKeyword:
             newKeyword = newKeyword + ch
       alpha='a bcdefghijklmnopqrstuvwxyz'
       str=newKeyword
       for ch in alpha:
          if ch not in newKeyword:
           str=str+ch
       password=str
       
       self.password=password

 



   def Encrypt(self, plaintext):
          plaintext=plaintext.lower()
          alphabet = "a bcdefghijklmnopqrstuvwxyz"
          ciphertext = ""
          for ch in plaintext:
             idx = alphabet.find(ch)
             ciphertext = ciphertext + self.password[idx]
          return ciphertext

   
   def Decrypt(self, ciphertext):
     ciphertext=ciphertext.lower()
     alphabet = "a bcdefghijklmnopqrstuvwxyz"
     plaintext = " "
     for ch in ciphertext:
        idx = self.password.find(ch)
        plaintext = plaintext + alphabet[idx]
     return plaintext


class Playfair:
    def __init__(self, password):
        password = password.lower()
        newKeyword = ''
        for ch in password:
            if ch not in newKeyword:
                newKeyword = newKeyword + ch
        alpha = 'abcdefghiklmnopqrstuvwxyz'
        str_ = newKeyword
        for ch in alpha:
            if ch not in newKeyword:
                str_ = str_ + ch
        password = str_
        self.password = password

    def encode_playfair_digram(self, text):
        text = text.lower()
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        new_text = ''

        for ch in text:
            if alpha.find(ch) != -1:
                new_text = new_text + ch

        new_text = new_text.replace('q', 'x')  # Replace 'Q' with 'X'

        i = 0
        while i < len(new_text):
            if i == len(new_text) - 1:
                new_text += "q"  # Add a 'Q' to make it an even number of characters
                break

            if new_text[i] == new_text[i + 1]:
                new_text = new_text[:i + 1] + "q" + new_text[i + 1:]
            i += 2

        return new_text

    def create_playfair_grid(self, password):
        password = password.lower()
        newKeyword = ''
        for ch in password:
            if ch not in newKeyword:
                if ch == 'j':
                    newKeyword = newKeyword + 'i'
                elif ch == ' ':
                    pass
                else:
                    newKeyword = newKeyword + ch
        alpha = 'abcdefghiklmnopqrstuvwxyz'
        str_ = newKeyword
        for ch in alpha:
            if ch not in newKeyword:
                str_ = str_ + ch
        return str_

    def find_coordinates(self, grid, char):
        for i in range(5):
            for j in range(5):
                if grid[i * 5 + j] == char:
                    return i, j
        raise ValueError(f"Character '{char}' not found in the grid.")

    def encrypt(self, plaintext):
        ciphertext = ''
        plaintext = plaintext.upper()
        plaintext = plaintext.replace('Q', 'X')  # Replace 'Q' with 'X' in the plaintext
        digrams = self.encode_playfair_digram(plaintext)
        grid = self.create_playfair_grid(self.password)
        i = 0
        while i < len(digrams):
            char1 = digrams[i]
            char2 = digrams[i + 1]
            row1, col1 = self.find_coordinates(grid, char1)
            row2, col2 = self.find_coordinates(grid, char2)

            if row1 == row2:  # Characters in the same row
                col1 = (col1 + 1) % 5
                col2 = (col2 + 1) % 5
            elif col1 == col2:  # Characters in the same column
                row1 = (row1 + 1) % 5
                row2 = (row2 + 1) % 5
            else:  # Characters in different rows and columns
                col1, col2 = col2, col1  # Swap columns

            ciphertext += grid[row1 * 5 + col1] + grid[row2 * 5 + col2]
            i += 2
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        ciphertext = ciphertext.upper()
        grid = self.create_playfair_grid(self.password)

        i = 0
        while i < len(ciphertext):
            char1 = ciphertext[i]
            
            if i == len(ciphertext) - 1:
                plaintext += char1
                break

            char2 = ciphertext[i+1]

            try:
                row1, col1 = self.find_coordinates(grid, char1)
                row2, col2 = self.find_coordinates(grid, char2)
            except ValueError:
                i += 2
                continue

            if row1 == row2:
                col1 = (col1 - 1) % 5
                col2 = (col2 - 1) % 5
            elif col1 == col2:
                row1 = (row1 - 1) % 5
                row2 = (row2 - 1) % 5
    

            plaintext += grid[row1 * 5 + col1] + grid[row2 * 5 + col2]
            i += 2


    # Remove any extra spaces at the end and convert to lowercase
        plaintext = plaintext.rstrip().lower()
        return plaintext


def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a message using substitution")
    parser.add_argument("mode", choices=["railfence", "sub", "playfair"], help="Specify railfence or substitution")
    parser.add_argument("password", type=str, help="The password for the cipher")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Specify whether to encrypt or decrypt")
    parser.add_argument("message", help="The plaintext or ciphertext message")
    args = parser.parse_args()

    rF=RailFence()
    Sub = Substition(args.password)
    play=Playfair(args.password)

    if args.mode=='railfence':
        if args.operation=='encrypt':
            ciphertext=rF.encrypt(args.message)
            print(f'Encrypted message: {ciphertext}')
        elif args.operation=='decrypt':
            plaintext=rF.decrypt(args.message)
            print(f'Decrypted message: {plaintext}')
    elif args.mode=='sub':
        
        if args.operation == "encrypt":
            ciphertext = Sub.Encrypt(args.message)
            print(f"Encrypted message:{ciphertext}")
        elif args.operation == "decrypt":
            plaintext = Sub.Decrypt(args.message)
            print(f"Decrypted message: {plaintext}")
    
    elif args.mode=='playfair':
        
        if args.operation == "encrypt":
            ciphertext = play.encrypt(args.message)
            print(f"Encrypted message:{ciphertext}")
        elif args.operation == "decrypt":
            plaintext = play.decrypt(args.message)
            print(f"Decrypted message:{plaintext}")
    
    
    else:
        print("Unexpected translation mode")
    return
   
   
   
   
 

if __name__ == "__main__":
    main()
