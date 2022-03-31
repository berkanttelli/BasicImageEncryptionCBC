import argparse
import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import PIL.Image as Image

class CBCEncryption:
    def __init__(self, key, iv):
        self.cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        self.encryptor = self.cipher.encryptor()
        self.decryptor = self.cipher.decryptor()

    def encrypt(self, image):
        return self.encryptor.update(image)
    def decrypt(self, image):
        return self.decryptor.update(image)

    def finalize_encrypt(self):
        return self.encryptor.finalize()
    def finalize_decrypt(self):
        return self.decryptor.finalize()

def Parser():
    parser = argparse.ArgumentParser(description='Encrypts or decrypts images using AES-CBC')
    parser.add_argument('-e', '--encrypt', help='Encrypts an image, If -e or -d is not specified, the program will encrypt the image.', action='store_true')
    parser.add_argument('-d', '--decrypt', help='Decrypts an image, If -e or -d is not specified, the program will encrypt the image.', action='store_true')
    parser.add_argument('-iv', '--iv', type=str,help='Initialization vector to use for encryption/decryption. If the IV is not 16 characters long, it is completed by the code to 16 characters.If it is not provided, an IV will be generated from the key.')
    parser.add_argument('-o','--output', type=str, help='Output file name. If not specified, the image will be saved as encrypted.bmp or decrypted.jpeg') 
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument('-i', '--image', metavar='PATH/image.jpg',type=str ,help='Image to encrypt/decrypt. ',required=True)
    requiredArgs.add_argument('-k', '--key',type=str ,help='Key to use for encryption/decryption. Maximum key length is 32 characters.',required=True)
    return parser.parse_args()

def EncryptImage(encryption, image, output):
    if output is None:
        output = 'encrypted.bmp'
    else:
        output = output + '.bmp'
    image = Image.open(image)
    image.save('temp.bmp')
    with open('temp.bmp', 'rb') as reader:
        with open(output, 'wb') as writer:
            image_data = reader.read()
            header, body = image_data[:54], image_data[54:]
            body += b'\x35' * (16 -(len(body) % 16))
            body = encryption.encrypt(body) + encryption.finalize_encrypt()
            writer.write(header + body)
            writer.close()
            reader.close()
    os.remove('temp.bmp')


def DecryptImage(decryption, image, output):
    if output is None:
        output = 'decrypted.jpeg'
    else:
        output = output + '.jpeg'
    
    image = Image.open(image)
    image.save('temp.bmp')
    with open('temp.bmp', 'rb') as reader:
        with open('decrypted.bmp', 'wb') as writer:
            image_data = reader.read()
            header, body = image_data[:54], image_data[54:]
            body = body[:len(body) - (len(body) % 16)+1]
            body = decryption.decrypt(body) + decryption.finalize_decrypt()
            writer.write(header + body)
            writer.close()
            reader.close()
    translateToBMP = Image.open('decrypted.bmp')
    translateToBMP.save(output)
    os.remove('decrypted.bmp')
    os.remove('temp.bmp')


def main():
    args = Parser()

    if len(args.key) > 32:
        print('Key is too long. Maximum key length is 32 characters.')
        sys.exit(1)
    else:
        key = args.key.encode('utf-8')
        key = key.ljust(32, b'\x35')
    
    if args.iv is not None:
        if len(args.iv) > 16:
            print('IV is too long. IV length must be 16 characters.')
            sys.exit(1)

    if args.iv is None:
        iv = key[:16]
        iv = bytearray(iv)
        for i in range(16):
            iv[i] = iv[i] ^ 0x35
        iv = bytes(iv)
    else:
        iv = args.iv.encode('utf-8')
        iv = iv.ljust(16, b'\x35')

    AesCbc = CBCEncryption(key, iv)

    if args.encrypt and args.decrypt:
        print('You cannot specify both -e and -d')
        sys.exit(1)
    elif args.decrypt:
        DecryptImage(decryption=AesCbc, image=args.image, output=args.output)
    elif args.encrypt:
        EncryptImage(encryption=AesCbc, image=args.image, output=args.output)
    else:
        EncryptImage(encryption=AesCbc, image=args.image, output=args.output)
    
    print("Done!")
    print("Please keep your key safe.")

if __name__ == '__main__':
    main()