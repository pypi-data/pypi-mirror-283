def intinput(prompt, err="Invalid input, please enter an integer."):
    if not isinstance(prompt, str):
        raise TypeError("The prompt must be a string.")
    while True:
        inter = input(prompt)
        if inter.isnumeric():
            return int(inter)
        else:
            print(err)
