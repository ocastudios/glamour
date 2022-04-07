def reverse(original):
    if original.__class__ in (int, float):
        return original * -1
    elif original.__class__ == str:
        if original == "right":
            return "left"
        elif original == "left":
            return "right"

        elif original == "up":
            return "down"
        elif original == "down":
            return "up"
