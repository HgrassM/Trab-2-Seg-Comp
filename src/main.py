from rsa import genprimes

print(f"Generating prime number that is 2048 bits long:\n{genprimes.genPrimeNumber(2048)}")

number = 359334085968622831041960188598043661065388726959079837

print(f"\n\nThe number {number} is prime? {genprimes.millerRabin(number, 40)}")
