NCESSCH = "NCESSCH"
LEAID = "LEAID"
LEANM05 = "LEANM05"
SCHNAM05 = "SCHNAM05"
LCITY05 = "LCITY05"
LSTATE05 = "LSTATE05"
LATCOD = "LATCOD"
LONCOD = "LONCOD"
MLOCALE = "MLOCALE"
ULOCALE = "ULOCALE"
status05 = "status05"

def require(flag, msg):
    if not flag:
        print(msg)
        exit(0)

class SchoolCounter:

    def __init__(self):
        self.file_name = "sl051bai.csv"
        self.item_list = self.read_file()
        self.state_map = dict()
        # i have no idea if city is unique by itself, but with state, it should be.
        self.state_city_map = dict()
        self.metro_centric_locale_map = dict()
        self.build_indices()
        self.print_answers()

    def print_answers(self):
        def question(q):
            print("******** " + q)
        question("How many schools are in data set {}: {}".format(self.file_name, str(len(self.item_list))))
        question("How many schools are in each state: ")
        for state, school_list in self.state_map.items():
            print("{}: {}".format(state, len(school_list)))
        question("How many schools are in each Metro-centric locale:")
        for mcl, school_list in self.metro_centric_locale_map.items():
            print("{}: {}".format(mcl, len(school_list)))
        question("Which city has the most schools in it, and what are they?")
        cities_ranked_by_school_count = \
            sorted([(len(school_list), state_city, school_list)
                    for state_city, school_list in self.state_city_map.items()], reverse=True)
        record = cities_ranked_by_school_count[0]
        question("City (State) with the most schools: {} ({}): {}".format(record[1][1], record[1][0], record[0]))
        question("The schools are:")
        for m in record[2]:
            print(m[SCHNAM05])
        question("How many unique cities has at least one school in it: {}".format(len(self.state_city_map)))

        # informational
        # for record in cities_ranked_by_school_count:
        #     print("{} ({}): {}".format(record[1][1], record[1][0], record[0]))

    def build_indices(self):
        def add_to_index(index, key, value):
            if key not in index:
                index[key] = []
            index[key].append(value)

        for m in self.item_list:
            add_to_index(self.state_map, m[LSTATE05], m)
            add_to_index(self.state_city_map, (m[LSTATE05], m[LCITY05]), m)
            add_to_index(self.metro_centric_locale_map, m[MLOCALE], m)

    def read_file(self):
        # https://stackoverflow.com/questions/19699367/for-line-in-results-in-unicodedecodeerror-utf-8-codec-cant-decode-byte
        with open(self.file_name, "r", encoding='ISO-8859-1') as file:
            lines = file.readlines()
            require(len(lines) > 1, "empty file")
            keys = lines[0].split(",")
            item_list = []
            for line_id, line in enumerate(lines[1:]):
                values = self.extract_values(line)
                require(len(values) == len(keys), "line {} has wrong number of values".format(str(line_id+2)))
                line_dict = {keys[i]: values[i] for i in range(len(keys))}
                item_list.append(line_dict)
            return item_list

    # this function may not cover all edge cases, but it could handle the file in question.
    def extract_values(self, line):
        values = []
        in_quote = False
        c_list = []
        for i, c in enumerate(line):
            if c == ',' and not in_quote or i == len(line)-1:
                values.append("".join(c_list))
                c_list = []
            else:
                if c == '"':
                    in_quote = not in_quote
                else:
                    c_list.append(c)
        return values


sc = SchoolCounter()
