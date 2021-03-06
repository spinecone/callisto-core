import importlib

from django.core.management.base import BaseCommand

from callisto.delivery.matching import run_matching
from callisto.delivery.report_delivery import PDFMatchReport


class Command(BaseCommand):
    help = 'finds matches and sends match reports'

    def add_arguments(self, parser):
        parser.add_argument('report_class', nargs='?', default=None)
        # eventually: add test option that verifies that passed class can be imported & has necessary methods
        # https://github.com/SexualHealthInnovations/callisto-core/issues/56

    def handle(self, *args, **options):
        report_class_name = options['report_class']
        if report_class_name:
            module_name, class_name = report_class_name.rsplit(".", 1)
            ReportClass = getattr(importlib.import_module(module_name), class_name)
        else:
            ReportClass = PDFMatchReport

        run_matching(report_class=ReportClass)

        self.stdout.write('Matching run')
