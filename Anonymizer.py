from faker import Faker
from anonymization import Anonymization, AnonymizerChain, PhoneNumberAnonymizer, msisdnAnonymizer, NamedEntitiesAnonymizer,FilePathAnonymizer, EmailAnonymizer, UriAnonymizer,MacAddressAnonymizer,Ipv4Anonymizer,Ipv6Anonymizer

class Anonymizer:
    def __init__(self):
        self.faker = Faker()


    def fake_name_generator(self, n):
        fake_names = []
        fake_first_names = []
        fake_second_names = []
        for i in range(0, n):
            name = self.faker.name()
            fake_names.append(name)
            fake_first_names.append(name.split()[0])
            if len(name.split())>1:
                fake_second_names.append(name.split()[1])
            else:
                fake_second_names.append('')
        return fake_names,fake_first_names,fake_second_names


    def get_fake_cities(self,n):
        fake_cities = []
        for i in range(0, n):
            fake_cities.append(self.faker.city())
        return fake_cities


    def get_fake_countries(self,n):
        fake_countries = []
        for i in range(0,n):
             fake_countries.append(self.faker.country())
        return fake_countries


    def get_fake_addresses(self,n):
        fake_addresses = []
        for i in range(0,n):
            fake_addresses.append(self.faker.address().split('\n')[0])
        return fake_addresses


    def get_fake_uris(self,n):
        fake_uris = []
        for i in range(0,n):
            fake_uris.append(self.faker.uri())
        return fake_uris

    def get_anonymize_text(self,query):
        anon = AnonymizerChain(Anonymization('en_US'))
        anon.add_anonymizers(FilePathAnonymizer,\
                            EmailAnonymizer, UriAnonymizer,MacAddressAnonymizer,Ipv4Anonymizer, Ipv6Anonymizer,\
                            NamedEntitiesAnonymizer('en'))
        anonymizedText = anon.anonymize(query)
        return anonymizedText
