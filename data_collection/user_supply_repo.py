# Detects the user that supplies this repo

def get_user_from_repo(address: str):
    repo_name = address.split("/")[-1]
    user = address.replace(repo_name, "")
    return user

if __name__ == "__main__":
    # Test script for this file
    TEST_ADDRESS = ["https://github.com/0064Unknown/lede",
                    "https://github.com/00NoisyMime00/Tick-Tac-Toe",
                    "https://github.com/0420syj/kosm",
                    "https://github.com/05nelsonm/authentication-manager"]
    for address in TEST_ADDRESS:
        print(get_user_from_repo(address))