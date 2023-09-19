def transform_value_to_percentage(value):
    min_value = 0
    max_value = 4095
    percentage = (value - min_value) / (max_value - min_value) * 100
    return percentage

# Exemplo de uso:
input_value = int(input("Digite um valor entre 0 e 4095: "))

if 0 <= input_value <= 4095:
    percentage_value = transform_value_to_percentage(input_value)
    print(f"O valor {input_value} corresponde a {percentage_value}%")
else:
    print("O valor digitado está fora do intervalo válido.")
