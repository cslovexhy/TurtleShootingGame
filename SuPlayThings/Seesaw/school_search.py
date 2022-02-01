import time

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


def get_time_in_ms():
    return int(round(time.time() * 1000))


class SchoolSearcher:

    def __init__(self):
        self.file_name = "sl051bai.csv"
        self.item_list = self.read_file()
        self.keyword_map = dict()
        self.build_indices()

        # print index for debugging
        # for k, v in self.keyword_map.items():
        #     print("{} - {}".format(k, v))
        # print(self.keyword_map['school'])
        # print(self.keyword_map['scottdale'])

    def build_indices(self):
        keys_relevant = [SCHNAM05, LSTATE05, LCITY05]
        for m in self.item_list:
            for key in keys_relevant:
                keywords = [v.lower() for v in m[key].split(" ")]
                for keyword in keywords:
                    if keyword not in self.keyword_map:
                        self.keyword_map[keyword] = set()
                    self.keyword_map[keyword].add((m[SCHNAM05], m[LSTATE05], m[LCITY05]))

    def search_schools(self, search_str):

        def print_result(items_to_show, start_time, keywords):
            print("Results for {} (search took: {}ms)".format(search_str, get_time_in_ms() - start_time))
            for rank, (frequency, school_info) in enumerate(items_to_show):
                print("{}. {}".format(rank+1, school_info[0]))
                print("   {}, {} ({}% relevant)".format(school_info[2], school_info[1], int(frequency*100/len(keywords))))

        start_time = get_time_in_ms()
        require(search_str, "Empty search string")
        keywords = [v.lower() for v in search_str.split(" ")]
        match_frequency_map = dict()
        for keyword in keywords:
            if keyword in self.keyword_map:
                rs = self.keyword_map[keyword]
                for school_info in rs:
                    if school_info not in match_frequency_map:
                        match_frequency_map[school_info] = 0
                    match_frequency_map[school_info] += 1
        match_frequency_ordered_list = sorted(
            [(frequency, school_info) for school_info, frequency in match_frequency_map.items()], reverse=True)

        # for frequency, school_info in match_frequency_ordered_list:
            # print("{}, {}".format(frequency, school_info))

        items_to_show = match_frequency_ordered_list[:3]
        print_result(items_to_show, start_time, keywords)

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


ss = SchoolSearcher()
ss.search_schools("douglas al high")
