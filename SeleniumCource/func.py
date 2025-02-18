# first_dict = {'Sauce Labs Backpack': '29.99', 'Sauce Labs Bike Light': '9.99'}
# second_dict = {'Sauce Labs Backpack': '29.99', 'Sauce Labs Bike Light': '9.99'}

# def name_price_comparison(first_dict: dict, second_dict: dict):
#     if first_dict == second_dict:
#         return 'Наименования и цены соответствуют!!!'
#     elif first_dict.keys() != second_dict.keys():
#         return 'Несоответствие наименований!!!'
#     elif first_dict.values() != second_dict.values():
#         return 'Несоответствие цен!!!'

# print(name_price_comparison(first_dict, second_dict))

# def cart_total(products: dict):
#     cart_total = 0
#     for price in products.values():
#         cart_total += float(price)
#     return round(cart_total, 2)

# print(cart_total(first_dict))

# print(cart_total(second_dict))


# import math
# fun = lambda x : 1 if x == 1 else math.ceil(math.sinh(fun (x-1)))
# print(fun(5))


# values = [20, 30, 50, 40, 10]
# values.sort()
# squared = {x: x**2 for x in values}
# print(squared)
# squared.setdefault(50, 2500)
# print(squared[50])


# def process(input_string: str) -> str:
#     A = 0
#     B = 0
#     C = 0

#     lst = input_string.split(" ")
#     for temp in lst:
#         if int(temp) > 0:
#             A += 1
#         elif int(temp) == 0:
#             B += 1
#         elif int(temp) < 0:
#             C += 1
#     return f"выше нуля: {A}, ниже нуля: {C}, равна нулю: {B}"


# input_string = input()
# output_string = process(input_string)
# print(output_string)


# def check_all_students_passed(scores_input: str, names_input: str) -> str:
#     students_dict = {}
#     score_list = []
#     students_list = []
#     for score in scores_input.split(","):
#         score_list.append(score)
#     for i, name in enumerate(names_input.split(",")):
#         students_dict[name] = score_list[i]
#     for key, value in students_dict.items():
#         if int(value) < 35:
#             students_list.append(key)
#         else:
#             continue
#     if len(students_list) == 0:
#         return "Все прошли!"
#     else:
#         return f"Есть не поступившие! \n {students_list}"


# # scores_input = input()
# # names_input = input()

# scores_input = "21, 40, 27"
# names_input = "Max, Alex, Brenden"

# result = check_all_students_passed(scores_input, names_input)
# print(result)
