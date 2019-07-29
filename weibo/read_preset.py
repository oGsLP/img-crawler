def read_preset(path):
    users = []
    with open(path) as fr:
        for line in fr:
            if (line[0] == "#"):
                continue
            else:
                [name, uid] = line.strip().split(" ")
                users.append({'name': name, 'uid': uid})
    return users
