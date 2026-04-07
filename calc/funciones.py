from math import pow

def sumar(nums):
    suma = nums[0]
    for num in nums[1:]:
        suma += num
    return suma

def restar(nums):
    rest = nums[0]
    for num in nums[1:]:
        rest -= num
    return rest

def multiplicar(nums):
    mult = 1
    for num in nums:
        mult = mult * num
    return mult

def dividir(nums):
    try:
        div = nums[0]
        for num in nums[1:]:
            div /= num
    except ZeroDivisionError:
        print("\033[31mNo se permite la división por cero.\033[0m")
        return None
    return div

def potencia(nums):
    if len(nums) > 2:
        print("\033[31mDemasiados operandos\033[0m")
        return None
    return pow(nums[0], nums[1])

def root(nums):
    if len(nums) > 2:
        print("\033[31mDemasiados operandos\033[0m")
        return None
    nums[1] = 1 / nums[1]
    return potencia(nums)

def absoluto(nums):
    if len(nums) > 1:
        print("\033[31mDemasiados operandos\033[0m")
        return None
    if nums[0] < 0:
        nums[0] = -nums[0]
    return nums[0]

