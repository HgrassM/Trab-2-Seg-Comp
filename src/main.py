from rsa import genprimes, keygen

#print(f"Generating prime number that is 2048 bits long:\n\n{genprimes.genPrimeNumber(2048)}")

#number = 359334085968622831041960188598043661065388726959079837

#print(f"\n\nThe number {number} is prime? {genprimes.millerRabin(number, 40)}")

#number2 = 36

#print(f"\n\nCharmichael function for the number {number2} is {keygen.charmichael(number2)}")

print(f"The e, d and n of RSA are:\n\n{keygen.generateKeys()}")
