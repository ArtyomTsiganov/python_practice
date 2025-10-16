import os
import pickle

class PrimeNumbers:
    def __init__(self):
        self.filename = "primes.pickle"



    @staticmethod
    def is_prime(n: int) -> bool:
        for i in range(2, n):
            if i * i > n:
                break
            if n % i == 0:
                return False
        return True

    def _deserialize_primes(self):
        if not os.path.exists(self.filename):
            return [2]
        with open(self.filename, "rb") as f:
            return pickle.load(f)

    def _serialize_primes(self, values):
        with open(self.filename, "wb") as f:
            pickle.dump(values, f, protocol=pickle.HIGHEST_PROTOCOL)

    def get_primes(self, n: int) -> [int]:
        primes = self._deserialize_primes()
        for i in range(primes[-1], n):
            if self.is_prime(i):
                primes.append(i)
            if i % 300000 == 0:
                self._serialize_primes(primes)
                print(i)
        return primes


if __name__ == "__main__":
    p = PrimeNumbers()
    print(p.get_primes(10000000))