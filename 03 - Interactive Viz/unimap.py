import googlemaps as gm
import requests
import json

class Univ():
    """this class represents a university object, it offers a name translation method
    
    Args:
        name (str): the name of the university as found in the data
    
    Attr:
        raw (str): the raw name
        names ([str, str] or [str]): list of [name, acronym] or [name]
        names (str): cleaned and lowered name
        acronym (str): acronym if exists, '' otherwise
        
    """
    
    #used to clean the names
    replacements = {
        'inst.': 'institut',
        'eidg.': 'eidgenössisch',
        'schweiz.': 'schweizerisch',
        'rech.': 'recherche',
        'pädag.': 'pädagogische',
        'physikal.': 'physikalisch',
        'meteorolog.': 'meteorologisch',
        'wissensch.': 'wissenschaften',
    }
    
    def plussify(self, name):
        """replaces spaces in a string with + """
        return name.replace(' ', '+')
    
    def clean_name(self, name):
        """ replaces known abreviations with complete word,
            gets rid of parentheses
        """
        for key, value in self.replacements.items():
            name = name.replace(key, value)
        if name.find('(') != -1:
            name = name[:name.find(' (')]
        return name
    
    def __init__(self, name):
        self.raw = name
        self.names = self.raw.lower().split(' - ')
        self.name = self.clean_name(self.names[0])
        if len(self.names) > 1:
            self.acronym = self.names[1]
        else:
            self.acronym = ''    
        
    def translate_name(self, key):
        """translates uni name through yandex, to english"""
        baseurl = 'https://translate.yandex.net/api/v1.5/tr.json/translate?text='
        plus = self.plussify(self.name)
        urlend = '&lang=en&key='+key
        url = baseurl+plus+urlend
        
        get = requests.get(url)
        r = json.loads(get.text)
        
        return r['text'][0]
        
    def __repr__(self):
        return 'Uni: '+ str(self.raw)

class UniMapper():
    """ this class contains the gmaps related code and the geocoding logic,
        translates uni name if failure
        
    Args:
        gkey (str): the api key for gmaps
        ykey (str): the api key for yandex
        
    Attr:
        gmaps (object): gmaps client
        yandex (str): yandex translate api key
    """
    def __init__(self, gkey, ykey):
        self.gmaps = gm.Client(key = gkey)
        self.yandex = ykey
        
    def geo(self, s):
        """gmaps geocode lookup, region Switzerland
        
        Args:
            s (str): the lookup string (uni name or acronym)
        
        Returns:
            json: google's geocode api response
        """
        return self.gmaps.geocode(s, region='CH')
    
    def pla(self, s):
        """places api lookup
        
        Args:
            s (str): the lookup string (uni name or acronym)
        
        Returns:
            json: google's places api response
        """
        return self.gmaps.places(s)
    
    def get_canton(self, response):
        """parses the gmaps.geocode response to find canton name

        Args:
            response ([dict]): the g.maps response object

        Returns:
            [str, str]: the canton name and the country name (for checks)
        """
        g = response[0]['address_components']
        #the canton name is in an object whose type is 'administrative_area_level_1'
        #we parse the response and get the 'short_name' of that object
        canton = [x['short_name'] for x in g if (x['types'][0].find('level_1')!=-1)][0]
        return canton
    
    def get_swiss_address(self, response):
        """parses the gmaps.places response, checks if address is swiss, outputs it

        Args:
            response (dict): the g.places response object, {..., 'results': [{'formatted_address': '...', ...}]}

        Returns:
            str: lowered address if address is in CH, '' otherwise
        """
        if response['status'] != 'ZERO_RESULTS':
            a = response['results'][0]['formatted_address'].lower()
            
            if a.endswith('switzerland'):
                return a
            else:
                return ''
            
        else:
            return ''
    
    def map_uni(self, uni, name):
        """returns the canton of the university, or 'fail' if nothing found
        
        Args:
            uni (Univ object): the university object
            name (str): the uni name, already extracted from object because may be translated
            
        Returns:
            str: canton name, 'fail' if nothing found
        """
        response = self.pla(uni.acronym+' '+name)
        address = self.get_swiss_address(response)
        
        if len(address) > 0:
            g = self.geo(address)
            canton = self.get_canton(g)
        else:
            canton = 'fail'
            
        return canton
    
    def canton_lookup(self, uni):
        """returns university canton, tries translating if first failure
        
        Args:
            uni (Univ object): university object
        
        Returns:
            str: canton name, 'fail' if nothing found
        """
        #first direct attempt at geocoding
        canton = self.map_uni(uni, uni.name)
        #second attempt with name translated to english
        if canton == 'fail':
            canton = self.map_uni(uni, uni.translate_name(self.yandex))
        return canton

class CantonDict():
    def __init__(self):
        self.d = {}

    def populate(self, array, m):
        """populates the dict with cantons and their assigned unis

        Args:
            array (array): array of universities raw names
            m (UniMapper object): the UniMapper instance we want to use

        Returns nothing but updates self.d
        """
        #initiating counters
        good = 0
        bad = 0

        #looping through unis
        for uni in array:
            #discarding null values
            if uni != '':
                #creating an Univ object and passing to UniMapper to get its canton
                u = Univ(uni)
                canton = m.canton_lookup(u)
                
                #introducing minor corrections         
                canton = corrections(canton, uni)
                
                #updating self.d
                if canton in self.d:
                    self.d[canton].append(uni)
                else:
                    self.d[canton] = [uni]
                
                #printing result for tracking
                print(' ')
                print(canton+' <-- '+uni)

                #updating counters
                if canton == 'fail':
                    bad += 1
                else:
                    good += 1
        #printing final count
        print(' ')
        print('done')
        print('# good: '+str(good)+' / # bad: '+str(bad)+' ==> '+str(round(good*100/(good+bad),2))+'% assigned')

    def export(self, file):
        with open(file, "w") as outfile:
            json.dump(self.d, outfile)

def corrections(canton, uni):
    """provides 'manual' corrections on canton
    
    Args:
        canton (str): the canton as attributed by unimapper
        uni (str): raw university name
        
    Returns:
        str: corrected canton according to observations on the data
    """
    #in two cases google has 'Geneve' as short name
    if canton == 'Genève':
        canton = 'GE'
    #if the canton was not attributed, correct it according to observations, case to case basis
    elif canton == 'fail':
        if uni.find('Wallis') != -1:
            canton = 'VS'
        elif uni.find('Basel') != -1:
            canton = 'BS'
        elif uni.find('AO') != -1:
            canton = 'GR'
        elif uni.find('SAGW') != -1:
            canton = 'BE'
    return canton