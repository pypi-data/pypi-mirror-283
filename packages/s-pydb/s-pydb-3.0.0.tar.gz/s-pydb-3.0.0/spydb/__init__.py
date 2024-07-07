"""# Simple-PyDB
# A Simple Database Module"""

__version__ = "3.0.0"
__name__ = "spydb"


class pydb:

    """
    ## Example:
    ```python3
    import spydb
    db = spydb.pydb("File")
    ```
    """

    # Constructor
    def __init__(self, file: str):
        try:
            f = open(file+".pydb")
            f.close()

        except FileNotFoundError:
            f = open(file+".pydb", "w", encoding="utf-8")
            f.close()

        self.file = file+".pydb"

    # Get Attribute like `db_obj.key`
    def __getattr__(self, name):
        return self.getData(name)

    def getData(self, var_key):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        print(db.getData("key1"))
        ```
        ### Output:
        ```
        hello
        ```
        """
        key = str(var_key)

        with open(self.file, 'r', encoding="utf-8") as f:

            lines = f.read().splitlines()

            i = 0
            while i < len(lines):

                line = lines[i]
                # if this line is not a data line
                if line.find(":") == -1:
                    # pass this line
                    lines.pop(i)

                elif line.split(':')[0] == key:
                    value = ":".join(line.split(":")[1:])

                    if value == "{True}":
                        return True
                    elif value == "{False}":
                        return False
                    elif value == "{None}":
                        return None
                    else:
                        return value

                else:
                    i += 1

            # if the key is not found
            return None

    def keys(self):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        print(db.keys())
        ```
        ### Output:
        ```
        ('key1','key2')
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:

            keys = []

            lines = f.readlines()
            for i in lines:
                keys.append(i.split(':')[0])

            return tuple(keys)

    def values(self):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        print(db.values())
        ```
        ### Output:
        ```
        ('hello','hallo')
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:

            keys = []

            lines = f.read().splitlines()
            for i in lines:
                keys.append(":".join(i.split(':')[1:]))

            return tuple(keys)

    def items(self):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        print(db.items())
        ```
        ### Output:
        ```
        (('key','hello'),('key2','hallo'))
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:

            items = []

            lines = f.read().splitlines()
            for i in lines:
                items.append([i.split(':')[0], ":".join(i.split(':')[1:])])

            return tuple(items)

    def addData(self, key, input_value):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.addData("key3", "holla")
        ```
        ### New file.pydb file:
        ```
        key1:hello
        key2:hallo
        key3:holla
        ```
        """
        value = str(input_value)
        key = str(key)

        with open(self.file, 'r+', encoding="utf-8") as f:

            new_value = value

            if value == True:
                new_value = "{True}"
            if value == False:
                new_value = "{False}"
            if value == None:
                new_value = "{None}"
            else:
                new_value = value.replace("\n", "\\n")

            keys = []

            lines = f.readlines()
            for line in lines:
                # if line is not a empty
                if line != "\n":
                    keys.append(line.split(':')[0])

            if (not key in keys) and (lines != []) and (lines[len(lines)-1].find('\n') == -1):
                # add line break to last line
                lines[len(lines)-1] += '\n'
                # add variable to end of file
                lines.append(str(key).replace("\n", "\\n").replace(":", "") + ':' + str(new_value).replace("\n", "\\n") + '\n')

            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def removeData(self, key):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        key3:holla
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.removeData("key3")
        ```
        ### New file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        """
        key = str(key)

        with open(self.file, 'r+', encoding="utf-8") as f:

            lines = f.readlines()

            i = 0
            while i < len(lines):
                if lines[i].split(':')[0] == str(key):
                    lines.pop(i)
                i += 1

            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def clear(self):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.clear()
        ```
        ### New file.pydb file:
        ```
        (Empty)
        ```
        """
        with open(self.file, 'w') as f:
            f.write('')

    def backUp(self, newfile: str):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.backUp("newFile")
        ```
        ### newFile.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            content = f.read()
            with open(newfile+".pydb", 'w') as f:
                f.write(content)

    def setData(self, key, newValue):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.setData("key2", "holla")
        ```
        ### newFile.pydb file:
        ```
        key1:hello
        key2:holla
        ```
        """
        key = str(key)

        modified_new_value = str(newValue).replace("\n", "\\n")

        if newValue == True:
            modified_new_value = "{True}"
        if newValue == False:
            modified_new_value = "{False}"
        if newValue == None:
            modified_new_value = "{None}"

        with open(self.file, 'r', encoding="utf-8") as f:

            lines = f.readlines()

            i = 0
            while i < len(lines):
                line = lines[i]

                if line.split(':')[0] == str(key):
                    lines[i] = str(key).replace("\n", "").replace(":", "") + ':' + modified_new_value + '\n'

                    f.seek(0)

                    with open(self.file, 'w') as fi:
                        fi.writelines(lines)
                i += 1

    def fileToDICT(self):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.fileToDICT()
        ```
        ### Output:
        ```
        {'key1':'hello','key2','hallo'}
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:
            dictionary = {}

            lines = f.read().splitlines()
            for line in lines:

                if line.find(":") != -1:

                    value = line.split(':')

                    if len(value) == 2:
                        if value[1] == "{True}":
                            dictionary[value[0]] = True
                        if value[1] == "{False}":
                            dictionary[value[0]] = False
                        if value[1] == "{None}":
                            dictionary[value[0]] = None
                        dictionary[value[0]] = value[1]

                    if len(value) > 2:
                        dictionary[value[0]] = ":".join(value[1:])

            return dictionary

    def dictToFILE(self, dictionary: dict):
        """
        ## Example:
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        db.dictToFILE({'key1':'hello','key2','hallo'})
        ```
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        """
        with open(self.file, 'w', encoding="utf-8") as f:

            lines = []

            for key, value in dictionary.items():

                if value == True:
                    lines.append("{}:{}\n".format(str(key).replace("\n", "\\n").replace(":", ""), "{True}"))
                if value == False:
                    lines.append("{}:{}\n".format(str(key).replace("\n", "\\n").replace(":", ""), "{False}"))
                if value == None:
                    lines.append("{}:{}\n".format(str(key).replace("\n", "\\n").replace(":", ""), "{None}"))

                lines.append("{}:{}\n".format(str(key).replace("\n", "\\n").replace(":", ""), str(value).replace("\n", "\\n")))

            f.writelines(lines)

    def contains(self, key: str):
        """
        ## Example:
        ### file.pydb file:
        ```
        key1:hello
        key2:hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pydb("file")
        print(db.contains("key1"), db.contains("key3"))
        ```
        ### Output
        ```
        True False
        ```
        """
        key = str(key)

        with open(self.file, 'r', encoding="utf-8") as f:

            lines = f.read().splitlines()

            i = 0
            while i < len(lines):
                if lines[i].find(":") == -1:
                    lines.pop(i)
                i += 1

            for line in lines:
                if line.split(':')[0] == str(key):
                    return True

            return False


class pylist:
    """
    ## Example:
    ```python3
    import spydb
    db = spydb.pylist("Filename")
    ```
    """

    # Constructor
    def __init__(self, file: str):
        self.f = file+".pylist"

    def getData(self, index: int):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        print(db.getData(0))
        ```
        ### Output:
        ```
        hello
        ```
        """
        with open(self.f, 'r', encoding="utf-8") as f:

            lines = f.read().splitlines()

            # if index is out of range
            if len(lines) - 1 < index:
                return None

            else:
                if lines[int(index)] == "{True}":
                    return True
                elif lines[int(index)] == "{False}":
                    return False
                elif lines[int(index)] == "{None}":
                    return None
                else:
                    return lines[int(index)]

    def listFile(self):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        print(db.listFile())
        ```
        ### Output:
        ```
        ['hello','hallo']
        ```
        """
        with open(self.f, 'r', encoding="utf-8") as f:

            llist = []

            lines = f.read().splitlines()
            for line in lines:
                if line == "{True}":
                    llist.append(True)
                    continue
                if line == "{False}":
                    llist.append(False)
                    continue
                if line == "{None}":
                    llist.append(None)
                    continue

                value = line
                llist.append(value)

            return llist

    def listToFILE(self, lst : list):
        """
        ## Example:
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        db.listToFILE(['hello','hallo'])
        ```
        ### New db.pylist file:
        ```
        hello
        hallo
        ```
        """
        with open(self.f, 'w', encoding="utf-8") as f:

            liste = []
            for i in lst:
                if i == True:
                    liste.append("{True}\n")
                    continue
                if i == False:
                    liste.append("{False}\n")
                    continue
                if i == None:
                    liste.append("{None}\n")
                    continue

                liste.append(str(i).replace("\n", "\\n") + "\n")

            f.writelines(liste)

    def addData(self, value):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        db.addData("holla")
        ```
        ### New db.pylist file:
        ```
        hello
        hallo
        holla
        ```
        """
        with open(self.f, 'r+', encoding="utf-8") as f:

            lines = f.read().splitlines()

            if value == True:
                lines.append("{True}\n")
            if value == False:
                lines.append("{False}\n")
            if value == None:
                lines.append("{None}\n")
            else:
                lines.append(str(value).replace("\n", "\\n"))

            f.seek(0)
            f.write("\n".join(lines))
            f.truncate()

    def setData(self, index: int, value):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        db.setData(1, "holla")
        ```
        ### New db.pylist file:
        ```
        hello
        holla
        ```
        """
        with open(self.f, 'r+', encoding="utf-8") as f:

            lines = f.read().splitlines()

            if value == True:
                lines[int(index)] = "{True}\n"
            if value == False:
                lines[int(index)] = "{False}\n"
            if value == None:
                lines[int(index)] = "{None}\n"
            else:
                lines[int(index)] = str(value).replace("\n", "\\n")

            f.seek(0)
            f.write("\n".join(lines))
            f.truncate()

    def removeData(self, index: int):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        holla
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        db.removeData(2)
        ```
        ### New db.pylist file:
        ```
        hello
        hallo
        ```
        """
        with open(self.f, 'r+', encoding="utf-8") as f:

            lines = f.readlines()
            lines.pop(int(index))

            f.seek(0)
            f.writelines(lines)
            f.truncate()

    def clear(self):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        holla
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        db.clear()
        ```
        ### New db.pylist file:
        ```
        (Empty)
        ```
        """
        f = open(self.f, 'w', encoding="utf-8")
        f.write("")
        f.close()

    def backUp(self, newfile: str):
        """
        ## Example:
        ### file.pydb file:
        ```
        hello
        hallo
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        db.backUp("newFile")
        ```
        ### newFile.pydb file:
        ```
        hello
        hallo
        ```
        """
        with open(self.file, 'r', encoding="utf-8") as f:

            lines = f.readlines()
            with open(newfile+".pydb", 'w') as f:
                f.writelines(lines)

    def length(self):
        """
        ## Example:
        ### db.pylist file:
        ```
        hello
        hallo
        holla
        ```
        ### Python File:
        ```python3
        import spydb
        db = spydb.pylist("filename")
        print(db.length())
        ```
        ### Output:
        ```
        3
        ```
        """
        with open(self.f, 'r', encoding="utf-8") as f:

            lines = f.read().splitlines()
            return len(lines)

    def index(self, value):
        if not value == True or not value == False or not value == None:
            if str(value) in self.listFile():
                return self.listFile().index(str(value))
            else:
                return -1
        else:
            if value in self.listFile():
                return self.listFile().index(value)
            else:
                return -1


class convert:
    def csv_to_pydb(csv_file, new_file_name):
        """
        ## Example:
        ### database.csv file content:
        ```csv
        keys,variables
        key1,var1
        key2,var2
        ```
        ### Python code:
        ```python3
        import spydb
        spydb.convert.csv_to_pydb("database.csv", "database")
        ```
        ### Created database.pydb file content:
        ```
        key1:var1
        key2:var2
        ```
        """
        import csv

        result_dict = {}

        with open(csv_file, mode='r', encoding='utf-8') as file:

            # get first line
            line1 = file.readline().replace("\n", "")

            file.seek(0)

            csv_reader = csv.DictReader(file)

            args = line1.split(",")
            key = args[0]
            var = args[1]

            for row in csv_reader:
                result_dict[row[key]] = row[var]

        with open(new_file_name+".pydb", 'w', encoding="utf-8") as f:

            lines = []
            for k, v in result_dict.items():

                if v == True:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), "{True}"))
                if v == False:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), "{False}"))
                if v == None:
                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), "{None}"))

                lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), str(v).replace("\n", "\\n")))

            f.writelines(lines)

        return new_file_name+".pydb"

    def json_to_pydb(json_file, new_file_name):
        """
        # Examples:
        ## Dictionary
        ### database.json file content
        ```json
        {
        "key1": "var1",
        "key2": "var2"
        }
        ```
        ### Python code:
        ```python3
        import spydb
        spydb.convert.json_to_pydb("database.json", "database")
        ```
        ### Created database.pydb file content:
        ```
        key1:var1
        key2:var2
        ```
        ## List
        ### database.json file content
        ```json
        [
        "var1",
        "var2"
        ]
        ```
        ### Python code:
        ```python3
        import spydb
        spydb.convert.json_to_pydb("database.json", "database")
        ```
        ### Created database.pydb file content:
        ```
        var1
        var2
        ```
        """
        import json

        data = None

        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if type(data) == dict:

            with open(new_file_name+".pydb", 'w', encoding="utf-8") as f:

                lines = []
                for k, v in data.items():
                    if v == True:
                        lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), "{True}"))
                    if v == False:
                        lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), "{False}"))
                    if v == None:
                        lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), "{None}"))

                    lines.append("{}:{}\n".format(str(k).replace("\n", "\\n").replace(":", ""), str(v).replace("\n", "\\n")))

                f.writelines(lines)

        elif type(data) == list:

            with open(new_file_name+".pydb", 'w', encoding="utf-8") as f:

                liste = []
                for i in data:
                    if i == True:
                        liste.append("{True}\n")
                        continue
                    if i == False:
                        liste.append("{False}\n")
                        continue
                    if i == None:
                        liste.append("{None}\n")
                        continue

                    liste.append(str(i).replace("\n", "\\n") + "\n")

                f.writelines(liste)

        return new_file_name+".pydb"


def dictToTABLE(dictionary):
    """
    ## Example:
    ```python3
    import spydb
    print(spydb.dictToTABLE({"apple": "den", "armuts": "den2", 1: 2}))
    ```
    ## Output:
    ```
    +--------+-------+
    | Key    | Value |
    +--------+-------+
    | apple  | den   |
    +--------+-------+
    | armuts | den2  |
    +--------+-------+
    | 1      | 2     |
    +--------+-------+
    ```
    """
    if dictionary == {}:
        return ""

    dictin = {"Key": "Value"}

    for k, v in dictionary.items():
        dictin[k] = v

    max_key_len = max(len(str(k)) for k in dictin.keys())
    max_val_len = max(len(str(v)) for v in dictin.values())

    ll = "+" + "-" * (max_key_len + 2) + "+" + "-" * (max_val_len + 2) + "+\n"
    table = ll

    for k, v in dictin.items():
        table += "| {:<{}} | {:<{}} |\n".format(
            str(k), max_key_len, str(v), max_val_len)
        table += ll

    return table


def listToTABLE(inplist):
    """
    ## Example:
    ```python3
    import spydb
    print(spydb.listToTABLE(["as","asd","jkasdg", True]))
    ```
    ## Output:
    ```
    +---+--------+
    | 0 | as     |
    +---+--------+
    | 1 | asd    |
    +---+--------+
    | 2 | jkasdg |
    +---+--------+
    | 3 | True   |
    +---+--------+
    ```
    """
    if tuple(inplist) == tuple(()):
        return ""

    dictin = {}

    sayis = range(len(inplist))
    for i in sayis:
        dictin[i] = inplist[i]

    max_key_len = max(len(str(k)) for k in sayis)
    max_val_len = max(len(str(v)) for v in inplist)

    ll = "+" + "-" * (max_key_len + 2) + "+" + "-" * (max_val_len + 2) + "+\n"
    table = ll

    for k, v in dictin.items():
        table += "| {:<{}} | {:<{}} |\n".format(str(k), max_key_len, str(v), max_val_len)
        table += ll

    return table
