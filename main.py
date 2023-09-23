import sys


class Block:
    def __init__(self):
        self.name = ""
        self.data = {}

    def set_name(self, name):
        self.name = name

    def set(self, key, value):
        self.data[key] = value

    def has_key(self, key):
        return key in self.data

    def get_name_as_int(self):
        return int(float(self.name))

    def get_value(self, key):
        return self.data[key]

    def get_value_as_int(self, key):
        return int(self.data[key])

    def to_str(self):
        name = "[" + self.name + "]"
        list = []
        list.append(name)
        for key, value in self.data.items():
            list.append(key + "=" + str(value))
        return "\n".join(list)

    def copy(self):
        c = Block()
        c.set_name(self.name)
        for key, value in self.data.items():
            c.set(key, value)
        return c

    def set_value_if_has_key(self, key, value):
        if self.has_key(key):
            self.set(key, value)

    def add_num_to_name(self, n):
        if "." in self.name:
            f = float(self.name)
            f = f + n
            self.name = str(f)
        elif self.name.isdecimal():
            i = int(self.name)
            i = i + n
            self.name = str(i)

    def get_name(self):
        return self.name


class Exo:
    def __init__(self):
        self.block_list = []

    def add_block(self, block):
        self.block_list.append(block)
        return self

    def count_obj(self):
        return self.block_list[-1].get_name_as_int() + 1

    def make_gaps(self):
        i = 0
        for block in self.block_list:
            if block.has_key("start"):
                start = block.get_value_as_int("start")
                block.set("start", start + i * 60)
            if block.has_key("end"):
                end = block.get_value_as_int("end")
                block.set("end", end + i * 60)
                i += 1
        return self

    def to_str(self):
        list = []
        for block in self.block_list:
            block_str = block.to_str()
            list.append(block_str)
        return "\n".join(list)

    def index(self, name):
        for i, block in enumerate(self.block_list):
            if block.get_name() == name:
                return i

    def fill_gaps(self):
        n = self.index("1")
        offset = self.count_obj() - 1
        for block in self.block_list[n:]:
            short_block = block.copy()
            self.block_list.append(short_block)
            short_block.add_num_to_name(offset)
            short_block.set_value_if_has_key("layer", "2")
            short_block.set_value_if_has_key("再生速度", "0.0")
            if short_block.has_key("start"):
                start = short_block.get_value_as_int("start")
                end = start - 1
                start = start - 60
                short_block.set("start", start)
                short_block.set("end", end)
        return self

    def add_sounds(self, path):
        obj_num = self.count_obj()
        for block in self.block_list:
            if block.has_key("layer") and block.get_value("layer") == "2":
                name = str(obj_num)
                start = block.get_value_as_int("start")
                end = start + 30
                sound = Block()
                sound.set_name(name)
                sound.set("start", start)
                sound.set("end", end)
                sound.set("layer", 3)
                sound.set("overlay", 1)
                sound.set("audio", 1)
                self.add_block(sound)
                sound = Block()
                sound.set_name(name + ".0")
                sound.set("_name", "音声ファイル")
                sound.set("再生位置", "0.00")
                sound.set("再生速度", "100.0")
                sound.set("ループ再生", "0")
                sound.set("動画ファイルと連携", "0")
                sound.set("file", path)
                self.add_block(sound)
                sound = Block()
                sound.set_name(name + ".1")
                sound.set("_name", "標準再生")
                sound.set("音量", "100.0")
                sound.set("左右", "0.0")
                self.add_block(sound)
                obj_num += 1
        return self


def read_file(path):
    file = open(path, "r")
    str = file.read()
    file.close()
    return str


def str_lines_to_Exo(lines):
    exo = Exo()
    block = Block()
    for line in lines:
        if line.startswith("["):
            block = Block()
            name = line.replace("[", "").replace("]", "")
            block.set_name(name)
            exo.add_block(block)
        else:
            key_and_value = line.split("=")
            key = key_and_value[0]
            value = key_and_value[1]
            block.set(key, value)
    return exo


def write_file(path, str):
    f = open(path, "w")
    f.write(str)
    f.close()


def main():
    args = sys.argv
    path = "before.exo"
    if len(args) > 1:
        path = args[1]
    lines = read_file(path).split()
    exo = str_lines_to_Exo(lines)
    exo.make_gaps()
    exo.fill_gaps()
    sound_path = "sound.mp3"
    exo.add_sounds(sound_path)

    path = "after.exo"
    write_file(path, exo.to_str())


if __name__ == "__main__":
    main()
