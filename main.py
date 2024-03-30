import requests
import json
from time import sleep

users_list = []


def get_user_info(userid):
    url = f'https://users.roblox.com/v1/users/{userid}'
    response = requests.get(url)

    count = 0
    while count < 10:
        if response.status_code == 200:
            user_data = response.json()

            print(f"Processing user (id): {userid}")
            print(f"User data fetched: {user_data}")

            user_data = {
                'bio': user_data.get('description', 'Bio not found'),
                'banned': user_data.get('isBanned', False),
                'user_name': user_data.get('name', 'Username not found'),
                'display_name': user_data.get('displayName', 'Display name not found'),
                'id': user_data.get('id', 'ID not found'),
            }
            return user_data
        else:
            count += 1
            print(f"Error: {response.status_code}. Retrying... Attempt {count}")
            if response.status_code == 429:
                sleep(5)
    return None


def main():
    input_file = 'termers.txt'
    output_file = 'output.json'

    total_users = len(open(input_file, 'r').readlines())
    print(f"Processing: {total_users} users.\n")

    for line in open(input_file, 'r'):

        # if line has no numbers, skip
        if not any(char.isdigit() for char in line):
            continue

        print(f"Processing line: {line}")
        # get id of the user
        userid = line.split('/')[4]
        user_data = get_user_info(userid)

        if user_data is None:
            print(f"User with id: {userid} not found.")
            continue

        users_list.append(user_data)
        print(f"Percentage complete: {len(users_list) / total_users * 100:.2f}%\n")

    with open(output_file, 'w') as file:
        json.dump(users_list, file, indent=4)

    print(f"\nProcessed {len(users_list)} users. User data written to {output_file}.")


if __name__ == "__main__":
    main()
