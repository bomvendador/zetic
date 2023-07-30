from django.test import TestCase

from pdf.single_report import SingleReport, SingleReportData, SectionData

cattel_example = SectionData(
    {
        "1_1": 1,
        "1_2": 2,
        "1_3": 3,
        "1_4": 4,
        "1_5": 5,
        "1_6": 6,
        "1_7": 7,
        "1_8": 8,
        "1_9": 9,
        "1_10": 10,
        "1_11": 1,
        "1_12": 2,
        "1_13": 3,
        "1_14": 4,
        "1_15": 5,
    }
)
coping_example = SectionData(
    {
        "2_1": 1,
        "2_2": 2,
        "2_3": 3,
        "2_4": 4,
        "2_5": 5,
        "2_6": 6,
        "2_7": 7,
        "2_8": 8,
        "2_9": 9,
        "2_10": 10,
        "2_11": 1,
        "2_12": 2,
        "2_13": 3,
        "2_14": 4,
        "2_15": 5,
        "2_16": 6,
        "2_17": 7,
        "2_18": 8,
        "2_19": 9,
        "2_20": 10,
    }
)


class SingleReportTest(TestCase):
    def test_single_report(self):
        single_report = SingleReport()
        single_report.generate_pdf(
            SingleReportData(
                participant_name="Pablo",
                lang="en",
                cattell_data=cattel_example,
                coping_data=coping_example,
            ),
            path="test",
        )
        single_report = SingleReport()
        single_report.generate_pdf(
            SingleReportData(
                participant_name="Павел",
                lang="ru",
                cattell_data=cattel_example,
                coping_data=coping_example,
            ),
            path="test",
        )
