from django.test import TestCase

from pdf.single_report import SingleReport, SingleReportData


class SingleReportTest(TestCase):
    def test_single_report(self):
        single_report = SingleReport()
        single_report.generate_pdf(
            SingleReportData(
                participant_name="Pablo",
                lang="en",
            ),
            path="test",
        )
        single_report = SingleReport()
        single_report.generate_pdf(
            SingleReportData(
                participant_name="Павел",
                lang="ru",
            ),
            path="test",
        )
