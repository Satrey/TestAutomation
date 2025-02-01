from faker import Faker

faker = Faker('ru_RU')

male_name_list = []
female_name_list = []

for i in range(1, 6):
    male_name_list.append(faker.name_male())
    female_name_list.append(faker.name_female())

for name in male_name_list:
    print(name)

for name in female_name_list:
    print(name)