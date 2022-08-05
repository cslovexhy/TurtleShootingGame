ROOT = "/Volumes/workspace/DadetAviaryService/src/DadetAviaryScripts/callexamples/Su/GemrQuery/ImpressionPrediction"
INPUT_DATE = "20220629"
INPUT_SSID = "413"

BID = "bid"
NO_BID = "nobid"
IMPRESSION = "impression"
PIXEL = "pixel"

COL_SOURCE_ID = "sourceid"
COL_PAGE_TYPE = "pagetype"
COL_SLOT_NAME = "slotname"
COL_COUNT = "count"

BID_2_NOBID_RATIO = "bid_2_nobid_ratio"
IMP_2_PIXEL_RATIO = "imp_2_pixel_ratio"

RESULT_DISPLAY_FORMAT = "{0: >20} | {1: >40} | {2: >20} | {3: >20} | {4: >10} | {5: >10} | {6: >10} | {7: >10}"


def require(flag, msg):
    if not flag:
        print(msg)
        exit(0)


class MergeGemrResult:
    def __init__(self, date, supply_source_id):
        self.date = date
        self.ssid = supply_source_id
        bid_dl = self.read_file(BID)
        nobid_dl = self.read_file(NO_BID)
        impression_dl = self.read_file(IMPRESSION)
        pixel_dl = self.read_file(PIXEL)

        print("Loaded supply source = {}, Calculating...".format(supply_source_id))

        key_set = set()
        key_set |= set([(m[COL_PAGE_TYPE], m[COL_SLOT_NAME]) for m in bid_dl])
        key_set |= set([(m[COL_PAGE_TYPE], m[COL_SLOT_NAME]) for m in nobid_dl])
        key_set |= set([(m[COL_PAGE_TYPE], m[COL_SLOT_NAME]) for m in impression_dl])
        key_set |= set([(m[COL_PAGE_TYPE], m[COL_SLOT_NAME]) for m in pixel_dl])

        combined_dd = {key: {BID: 0, NO_BID: 0, IMPRESSION: 0, PIXEL: 0} for key in key_set}
        self.add_records(combined_dd, bid_dl, BID)
        self.add_records(combined_dd, nobid_dl, NO_BID)
        self.add_records(combined_dd, impression_dl, IMPRESSION)
        self.add_records(combined_dd, pixel_dl, PIXEL)

        # some calculation
        for key, d in combined_dd.items():
            d[BID_2_NOBID_RATIO] = -1 if d[NO_BID] == 0 else d[BID] / d[NO_BID]
            d[IMP_2_PIXEL_RATIO] = -1 if d[PIXEL] == 0 else d[IMPRESSION] / d[PIXEL]

        # show result
        combined_dl = [{COL_PAGE_TYPE: key[0],
                        COL_SLOT_NAME: key[1],
                        BID: d[BID],
                        NO_BID: d[NO_BID],
                        IMPRESSION: d[IMPRESSION],
                        PIXEL: d[PIXEL],
                        BID_2_NOBID_RATIO: d[BID_2_NOBID_RATIO],
                        IMP_2_PIXEL_RATIO: d[IMP_2_PIXEL_RATIO]} for key, d in combined_dd.items()]

        combined_dl = sorted(combined_dl, key=lambda d: d[PIXEL], reverse=True)
        print(RESULT_DISPLAY_FORMAT.format(COL_PAGE_TYPE, COL_SLOT_NAME, BID_2_NOBID_RATIO, IMP_2_PIXEL_RATIO, BID, NO_BID, IMPRESSION, PIXEL))
        for d in combined_dl:
            print(RESULT_DISPLAY_FORMAT.format(
                d[COL_PAGE_TYPE][:20],
                d[COL_SLOT_NAME][:40],
                str(d[BID_2_NOBID_RATIO])[:6],
                str(d[IMP_2_PIXEL_RATIO])[:6],
                d[BID],
                d[NO_BID],
                d[IMPRESSION],
                d[PIXEL]
            ))
        print(RESULT_DISPLAY_FORMAT.format(COL_PAGE_TYPE, COL_SLOT_NAME, BID_2_NOBID_RATIO, IMP_2_PIXEL_RATIO, BID, NO_BID, IMPRESSION, PIXEL))

    def add_records(self, combined_dd, dl, type_key):
        for d in dl:
            # print("type = " + type_key + ", " + str(d))
            combined_dd[(d[COL_PAGE_TYPE], d[COL_SLOT_NAME])][type_key] += int(d[COL_COUNT])

    def read_file(self, prefix):
        file_name = "{root}/{date}/{prefix}-{date}.csv".format(
            root=ROOT, date=self.date, prefix=prefix
        )
        # https://stackoverflow.com/questions/19699367/for-line-in-results-in-unicodedecodeerror-utf-8-codec-cant-decode-byte
        with open(file_name, "r", encoding='ISO-8859-1') as file:
            lines = file.readlines()
            require(len(lines) > 1, "empty file")
            keys = lines[0][:-1].split(",")
            # print("keys = " + str(keys))
            item_list = []
            for line_id, line in enumerate(lines[1:]):
                if not line.startswith(self.ssid + ","):
                    continue
                values = self.extract_values(line)
                require(len(values) == len(keys), "line {} has wrong number of values".format(str(line_id+2)))
                line_dict = {keys[i]: values[i] for i in range(len(keys))}
                item_list.append(line_dict)
            # print("{} line count = {}".format(prefix, str(len(item_list))))
            # print(str(item_list))
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


MergeGemrResult(INPUT_DATE, INPUT_SSID)