def factorial(n):
    if n < 0:
        raise ValueError("Факториал не определен для отрицательных чисел")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    num = int(input("Введите число: "))
    try:
        result = factorial(num)
        print(f"Факториал {num} равен {result}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
