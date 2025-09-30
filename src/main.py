from rsa import genprimes, keygen, crypto

#print(f"Generating prime number that is 2048 bits long:\n\n{genprimes.genPrimeNumber(2048)}")

#number = 359334085968622831041960188598043661065388726959079837

#print(f"\n\nThe number {number} is prime? {genprimes.millerRabin(number, 40)}")

#number2 = 36

#print(f"\n\nCharmichael function for the number {number2} is {keygen.charmichael(number2)}")

keys = keygen.generateKeys()

print(f"The e, d and n of RSA are:\n\n{keys}\n\n")

c = crypto.dummyEncrypt(12345, keys["e"], keys["n"])

print(f"The ciphertext of '12345' is {c}\n\n")

m = crypto.dummyDecrypt(c, keys["d"], keys["n"])

print(f"The plaintext of the ciphertext is {m}\n")

