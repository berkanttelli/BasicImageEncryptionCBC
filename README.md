
# Basic Image Encryption with CBC
This python code encrypts or decrypts Images using AES-CBC. I used the .bmp extension so that the image is openable but unintelligible when encrypted. Also, encrypted images are saved as .bmp and when decrypted, they are converted back to .jpeg format.


## Usage/Examples
Do not forget to install the libraries given in `requirements.txt.` 
```
python basicImageEncryption.py -e -k password -i image.jpeg -o imageDecrypted
```
```bash
optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         Encrypts an image, If -e or -d is not specified, the program will encrypt the image.
  -d, --decrypt         Decrypts an image, If -e or -d is not specified, the program will encrypt the image.
  -iv IV, --iv IV       Initialization vector to use for encryption/decryption. If the IV is not 16 characters 
                        long, it is completed by the code to 16 characters.If it is not provided, an IV will be 
                        generated from the key.
  -o OUTPUT, --output OUTPUT Output file name. If not specified, the image will be 
                             saved as encrypted.bmp or decrypted.jpeg

required arguments:
  -i PATH/image.jpg, --image PATH/image.jpg Image to encrypt/decrypt.
  -k KEY, --key KEY     Key to use for encryption/decryption. Maximum key length is 32 characters.
```
    
## LICENSE
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/berkanttelli/BasicImageEncryptionCBC/blob/master/LICENSE)


