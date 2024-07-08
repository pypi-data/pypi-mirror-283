def main():
    for num in range(1001, 9999, 1):
        sum_of_odd_digits = 0
        temp_num = num

        while temp_num > 0:
            digit = temp_num % 10
            if digit % 2 != 0:
                sum_of_odd_digits += digit
            temp_num //= 10

        if sum_of_odd_digits > 0 and num % sum_of_odd_digits == 0:
            print("بزرگترین عدد چهار رقمی که بر مجموع ارقام فردش بخش‌پذیر است:", num)
            break

if __name__ == "__main__":
    main()
