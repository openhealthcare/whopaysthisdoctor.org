from django.core.management.base import BaseCommand, CommandError
from doctors.models import Doctor, ImportedDoctorCompanyLink
import json

class Command(BaseCommand):
    help = 'Import an OpenCorporate query in JSON format. See https://github.com/drcjar/wptd2/blob/master/wptd-opencorporates.ipynb'

    def add_arguments(self, parser):
        parser.add_argument('data', help='JSON data')

    def handle(self, *args, **options):
        self.stdout.write(args[0])
        with open (args[0], "r") as myfile:
            data=myfile.read()

        datastore = json.loads(data)

        for person in datastore:
            nameParts = person[0]['name'].split()
            drs = Doctor.objects.filter(name__icontains = nameParts[0]).filter(name__icontains = nameParts[len(nameParts) - 1]);
            self.stdout.write(drs[0].name)
            if len(drs) == 0:
                self.stdout.write("Could not identify existing doctor for " + person[0]['name'])
            elif len(drs) > 1:
                self.stdout.write("Identified more than one existing doctor for " + person[0]['name'])
            else:
                for directorship in person:
                    self.stdout.write(directorship['position'])
                    newLink = ImportedDoctorCompanyLink(
                        doctor=drs[0], 
                        company=directorship['company']['name'], 
                        officer_link=directorship['opencorporates_url'],
                        company_link=directorship['company']['opencorporates_url'])
                    newLink.save()

