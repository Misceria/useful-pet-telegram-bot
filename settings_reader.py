


def read_settings():
    settings_dictionary = {}
    with open(".setts", "r") as settings_file:
        for line in settings_file.read().split("\n"):
            key, value = line.split(" = ")
            settings_dictionary[key] = value
    return settings_dictionary

