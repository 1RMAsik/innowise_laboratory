def generate_profile(age: int):
    if 0 < age <= 12:
        return "Child"
    if 13 <= age <= 19:
        return "Teenager"
    if age >= 20:
        return "Adult"
    return None

user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)
current_year = 2025 - birth_year

hobbies = []

while True:
    hobbies.append(input("Enter a favorite hobby or type 'stop' to finish: "))
    if "stop" in hobbies:
        hobbies.remove("stop")
        break

life_stage = generate_profile(current_year)
user_profile = {'name': user_name, 'age': current_year, 'stage': life_stage, 'hobby': hobbies}

print("\n---")
print("Profile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")
if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite hobbies ({len(hobbies)}): ")
    for hobby in hobbies:
        print(f"- {hobby}")
print("---")