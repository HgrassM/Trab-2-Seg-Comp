from keygen import genprimes

print(f"Generation prime number 2048 bits long:\n {genprimes.genPrimeNumber(2048)}")

number = 8683317618811886495518194401279999999

print(f"\n\nThe number {number} is prime? {genprimes.millerRabin(number, 40)}")
