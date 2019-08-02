def read_preset(path):
    users = []
    with open(path) as fr:
        for line in fr:
            if line[0] == "#":
                continue
            else:
                args = line.strip().split(" ")
                if len(args) == 2:
                    users.append({'name': args[0], 'uid': args[1]})
                elif len(args) == 1 and len(line.strip()) == 10:
                    users.append({'name': None, 'uid': line.strip()})
                else:
                    print("Wrong arguments: %s"
                          % line)
    return users
