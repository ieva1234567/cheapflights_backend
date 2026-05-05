import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .models import Airport, Flight


class RyanairAPI:
    BASE_URL = "https://api.ryanair.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_airports(self) -> List[Dict]:
        """Get list of Ryanair airports"""
        try:
            # Try the Ryanair API first
            url = f"{self.BASE_URL}/aggregate/3/common"
            params = {
                'embedded': 'airports,countries,cities,regions,nearbyAirports,defaultAirport',
                'market': 'en-gb'
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            airports = []
            for airport in data.get('airports', []):
                airports.append({
                    'iata_code': airport.get('iataCode', ''),
                    'name': airport.get('name', ''),
                    'city': airport.get('city', ''),
                    'country': airport.get('country', {}).get('name', '')
                })
            
            return airports
            
        except requests.RequestException as e:
            print(f"Error fetching airports from API: {e}")
            print("Using fallback airport list...")
            return self._get_fallback_airports()
    
    def _get_fallback_airports(self) -> List[Dict]:
        """Get fallback list of major Ryanair airports"""
        return [
            # Ireland
            {'iata_code': 'DUB', 'name': 'Dublin Airport', 'city': 'Dublin', 'country': 'Ireland'},
            {'iata_code': 'SNN', 'name': 'Shannon Airport', 'city': 'Shannon', 'country': 'Ireland'},
            {'iata_code': 'ORK', 'name': 'Cork Airport', 'city': 'Cork', 'country': 'Ireland'},
            {'iata_code': 'NOC', 'name': 'Ireland West Airport Knock', 'city': 'Knock', 'country': 'Ireland'},
            
            # United Kingdom
            {'iata_code': 'STN', 'name': 'London Stansted Airport', 'city': 'London', 'country': 'United Kingdom'},
            {'iata_code': 'LTN', 'name': 'London Luton Airport', 'city': 'London', 'country': 'United Kingdom'},
            {'iata_code': 'LGW', 'name': 'London Gatwick Airport', 'city': 'London', 'country': 'United Kingdom'},
            {'iata_code': 'MAN', 'name': 'Manchester Airport', 'city': 'Manchester', 'country': 'United Kingdom'},
            {'iata_code': 'BHX', 'name': 'Birmingham Airport', 'city': 'Birmingham', 'country': 'United Kingdom'},
            {'iata_code': 'EDI', 'name': 'Edinburgh Airport', 'city': 'Edinburgh', 'country': 'United Kingdom'},
            {'iata_code': 'GLA', 'name': 'Glasgow Airport', 'city': 'Glasgow', 'country': 'United Kingdom'},
            {'iata_code': 'LPL', 'name': 'Liverpool John Lennon Airport', 'city': 'Liverpool', 'country': 'United Kingdom'},
            {'iata_code': 'BRS', 'name': 'Bristol Airport', 'city': 'Bristol', 'country': 'United Kingdom'},
            {'iata_code': 'EMA', 'name': 'East Midlands Airport', 'city': 'Nottingham', 'country': 'United Kingdom'},
            {'iata_code': 'LBA', 'name': 'Leeds Bradford Airport', 'city': 'Leeds', 'country': 'United Kingdom'},
            {'iata_code': 'NCL', 'name': 'Newcastle Airport', 'city': 'Newcastle', 'country': 'United Kingdom'},
            {'iata_code': 'CWL', 'name': 'Cardiff Airport', 'city': 'Cardiff', 'country': 'United Kingdom'},
            {'iata_code': 'SOU', 'name': 'Southampton Airport', 'city': 'Southampton', 'country': 'United Kingdom'},
            
            # Spain
            {'iata_code': 'BCN', 'name': 'Barcelona Airport', 'city': 'Barcelona', 'country': 'Spain'},
            {'iata_code': 'MAD', 'name': 'Madrid Barajas Airport', 'city': 'Madrid', 'country': 'Spain'},
            {'iata_code': 'PMI', 'name': 'Palma de Mallorca Airport', 'city': 'Palma', 'country': 'Spain'},
            {'iata_code': 'AGP', 'name': 'Malaga Airport', 'city': 'Malaga', 'country': 'Spain'},
            {'iata_code': 'ALC', 'name': 'Alicante Airport', 'city': 'Alicante', 'country': 'Spain'},
            {'iata_code': 'VLC', 'name': 'Valencia Airport', 'city': 'Valencia', 'country': 'Spain'},
            {'iata_code': 'IBZ', 'name': 'Ibiza Airport', 'city': 'Ibiza', 'country': 'Spain'},
            {'iata_code': 'PMI', 'name': 'Palma de Mallorca Airport', 'city': 'Palma', 'country': 'Spain'},
            {'iata_code': 'LPA', 'name': 'Las Palmas Airport', 'city': 'Las Palmas', 'country': 'Spain'},
            {'iata_code': 'TFS', 'name': 'Tenerife South Airport', 'city': 'Tenerife', 'country': 'Spain'},
            {'iata_code': 'TFN', 'name': 'Tenerife North Airport', 'city': 'Tenerife', 'country': 'Spain'},
            {'iata_code': 'SVQ', 'name': 'Seville Airport', 'city': 'Seville', 'country': 'Spain'},
            {'iata_code': 'ZAZ', 'name': 'Zaragoza Airport', 'city': 'Zaragoza', 'country': 'Spain'},
            {'iata_code': 'BIH', 'name': 'Bilbao Airport', 'city': 'Bilbao', 'country': 'Spain'},
            {'iata_code': 'OVD', 'name': 'Asturias Airport', 'city': 'Oviedo', 'country': 'Spain'},
            {'iata_code': 'SCQ', 'name': 'Santiago de Compostela Airport', 'city': 'Santiago', 'country': 'Spain'},
            {'iata_code': 'FUE', 'name': 'Fuerteventura Airport', 'city': 'Fuerteventura', 'country': 'Spain'},
            {'iata_code': 'ACE', 'name': 'Lanzarote Airport', 'city': 'Lanzarote', 'country': 'Spain'},
            {'iata_code': 'VDE', 'name': 'La Gomera Airport', 'city': 'La Gomera', 'country': 'Spain'},
            {'iata_code': 'SPC', 'name': 'La Palma Airport', 'city': 'La Palma', 'country': 'Spain'},
            {'iata_code': 'EAS', 'name': 'San Sebastian Airport', 'city': 'San Sebastian', 'country': 'Spain'},
            {'iata_code': 'GRO', 'name': 'Girona Airport', 'city': 'Girona', 'country': 'Spain'},
            {'iata_code': 'REU', 'name': 'Reus Airport', 'city': 'Reus', 'country': 'Spain'},
            {'iata_code': 'MJV', 'name': 'Murcia Airport', 'city': 'Murcia', 'country': 'Spain'},
            {'iata_code': 'XRY', 'name': 'Jerez Airport', 'city': 'Jerez', 'country': 'Spain'},
            
            # Italy
            {'iata_code': 'FCO', 'name': 'Rome Fiumicino Airport', 'city': 'Rome', 'country': 'Italy'},
            {'iata_code': 'MXP', 'name': 'Milan Malpensa Airport', 'city': 'Milan', 'country': 'Italy'},
            {'iata_code': 'CIA', 'name': 'Rome Ciampino Airport', 'city': 'Rome', 'country': 'Italy'},
            {'iata_code': 'BGY', 'name': 'Bergamo Airport', 'city': 'Bergamo', 'country': 'Italy'},
            {'iata_code': 'TSF', 'name': 'Treviso Airport', 'city': 'Treviso', 'country': 'Italy'},
            {'iata_code': 'VRN', 'name': 'Verona Airport', 'city': 'Verona', 'country': 'Italy'},
            {'iata_code': 'NAP', 'name': 'Naples Airport', 'city': 'Naples', 'country': 'Italy'},
            {'iata_code': 'CTA', 'name': 'Catania Airport', 'city': 'Catania', 'country': 'Italy'},
            {'iata_code': 'PMO', 'name': 'Palermo Airport', 'city': 'Palermo', 'country': 'Italy'},
            {'iata_code': 'BRI', 'name': 'Bari Airport', 'city': 'Bari', 'country': 'Italy'},
            {'iata_code': 'BLQ', 'name': 'Bologna Airport', 'city': 'Bologna', 'country': 'Italy'},
            {'iata_code': 'FLR', 'name': 'Florence Airport', 'city': 'Florence', 'country': 'Italy'},
            {'iata_code': 'Pisa', 'name': 'Pisa Airport', 'city': 'Pisa', 'country': 'Italy'},
            {'iata_code': 'CAG', 'name': 'Cagliari Airport', 'city': 'Cagliari', 'country': 'Italy'},
            {'iata_code': 'OLB', 'name': 'Olbia Airport', 'city': 'Olbia', 'country': 'Italy'},
            
            # Germany
            {'iata_code': 'BER', 'name': 'Berlin Brandenburg Airport', 'city': 'Berlin', 'country': 'Germany'},
            {'iata_code': 'MUC', 'name': 'Munich Airport', 'city': 'Munich', 'country': 'Germany'},
            {'iata_code': 'FRA', 'name': 'Frankfurt Airport', 'city': 'Frankfurt', 'country': 'Germany'},
            {'iata_code': 'HHN', 'name': 'Frankfurt Hahn Airport', 'city': 'Frankfurt', 'country': 'Germany'},
            {'iata_code': 'DUS', 'name': 'Dusseldorf Airport', 'city': 'Dusseldorf', 'country': 'Germany'},
            {'iata_code': 'CGN', 'name': 'Cologne Bonn Airport', 'city': 'Cologne', 'country': 'Germany'},
            {'iata_code': 'HAM', 'name': 'Hamburg Airport', 'city': 'Hamburg', 'country': 'Germany'},
            {'iata_code': 'BRE', 'name': 'Bremen Airport', 'city': 'Bremen', 'country': 'Germany'},
            {'iata_code': 'STR', 'name': 'Stuttgart Airport', 'city': 'Stuttgart', 'country': 'Germany'},
            {'iata_code': 'LEJ', 'name': 'Leipzig Airport', 'city': 'Leipzig', 'country': 'Germany'},
            {'iata_code': 'DRS', 'name': 'Dresden Airport', 'city': 'Dresden', 'country': 'Germany'},
            {'iata_code': 'NUE', 'name': 'Nuremberg Airport', 'city': 'Nuremberg', 'country': 'Germany'},
            
            # France
            {'iata_code': 'CDG', 'name': 'Paris Charles de Gaulle Airport', 'city': 'Paris', 'country': 'France'},
            {'iata_code': 'ORY', 'name': 'Paris Orly Airport', 'city': 'Paris', 'country': 'France'},
            {'iata_code': 'BVA', 'name': 'Beauvais Airport', 'city': 'Paris', 'country': 'France'},
            {'iata_code': 'NCE', 'name': 'Nice Airport', 'city': 'Nice', 'country': 'France'},
            {'iata_code': 'MRS', 'name': 'Marseille Airport', 'city': 'Marseille', 'country': 'France'},
            {'iata_code': 'LYS', 'name': 'Lyon Airport', 'city': 'Lyon', 'country': 'France'},
            {'iata_code': 'TLS', 'name': 'Toulouse Airport', 'city': 'Toulouse', 'country': 'France'},
            {'iata_code': 'BOD', 'name': 'Bordeaux Airport', 'city': 'Bordeaux', 'country': 'France'},
            {'iata_code': 'NTE', 'name': 'Nantes Airport', 'city': 'Nantes', 'country': 'France'},
            {'iata_code': 'MPL', 'name': 'Montpellier Airport', 'city': 'Montpellier', 'country': 'France'},
            
            # Portugal
            {'iata_code': 'LIS', 'name': 'Lisbon Airport', 'city': 'Lisbon', 'country': 'Portugal'},
            {'iata_code': 'OPO', 'name': 'Porto Airport', 'city': 'Porto', 'country': 'Portugal'},
            {'iata_code': 'FAO', 'name': 'Faro Airport', 'city': 'Faro', 'country': 'Portugal'},
            {'iata_code': 'FNC', 'name': 'Funchal Airport', 'city': 'Funchal', 'country': 'Portugal'},
            {'iata_code': 'PDL', 'name': 'Ponta Delgada Airport', 'city': 'Ponta Delgada', 'country': 'Portugal'},
            {'iata_code': 'TER', 'name': 'Terceira Airport', 'city': 'Terceira', 'country': 'Portugal'},
            
            # Netherlands
            {'iata_code': 'AMS', 'name': 'Amsterdam Schiphol Airport', 'city': 'Amsterdam', 'country': 'Netherlands'},
            {'iata_code': 'EIN', 'name': 'Eindhoven Airport', 'city': 'Eindhoven', 'country': 'Netherlands'},
            {'iata_code': 'RTM', 'name': 'Rotterdam Airport', 'city': 'Rotterdam', 'country': 'Netherlands'},
            {'iata_code': 'MST', 'name': 'Maastricht Airport', 'city': 'Maastricht', 'country': 'Netherlands'},
            
            # Belgium
            {'iata_code': 'BRU', 'name': 'Brussels Airport', 'city': 'Brussels', 'country': 'Belgium'},
            {'iata_code': 'CRL', 'name': 'Charleroi Airport', 'city': 'Charleroi', 'country': 'Belgium'},
            {'iata_code': 'ANR', 'name': 'Antwerp Airport', 'city': 'Antwerp', 'country': 'Belgium'},
            {'iata_code': 'LGG', 'name': 'Liege Airport', 'city': 'Liege', 'country': 'Belgium'},
            
            # Austria
            {'iata_code': 'VIE', 'name': 'Vienna International Airport', 'city': 'Vienna', 'country': 'Austria'},
            {'iata_code': 'SZG', 'name': 'Salzburg Airport', 'city': 'Salzburg', 'country': 'Austria'},
            {'iata_code': 'LNZ', 'name': 'Linz Airport', 'city': 'Linz', 'country': 'Austria'},
            {'iata_code': 'Graz', 'name': 'Graz Airport', 'city': 'Graz', 'country': 'Austria'},
            {'iata_code': 'INN', 'name': 'Innsbruck Airport', 'city': 'Innsbruck', 'country': 'Austria'},
            {'iata_code': 'KLU', 'name': 'Klagenfurt Airport', 'city': 'Klagenfurt', 'country': 'Austria'},
            
            # Czech Republic
            {'iata_code': 'PRG', 'name': 'Prague Vaclav Havel Airport', 'city': 'Prague', 'country': 'Czech Republic'},
            {'iata_code': 'BRQ', 'name': 'Brno Airport', 'city': 'Brno', 'country': 'Czech Republic'},
            {'iata_code': 'OSR', 'name': 'Ostrava Airport', 'city': 'Ostrava', 'country': 'Czech Republic'},
            {'iata_code': 'PARD', 'name': 'Pardubice Airport', 'city': 'Pardubice', 'country': 'Czech Republic'},
            
            # Poland
            {'iata_code': 'WAW', 'name': 'Warsaw Chopin Airport', 'city': 'Warsaw', 'country': 'Poland'},
            {'iata_code': 'KRK', 'name': 'Krakow Airport', 'city': 'Krakow', 'country': 'Poland'},
            {'iata_code': 'GDN', 'name': 'Gdansk Airport', 'city': 'Gdansk', 'country': 'Poland'},
            {'iata_code': 'WRO', 'name': 'Wroclaw Airport', 'city': 'Wroclaw', 'country': 'Poland'},
            {'iata_code': 'POZ', 'name': 'Poznan Airport', 'city': 'Poznan', 'country': 'Poland'},
            {'iata_code': 'KTW', 'name': 'Katowice Airport', 'city': 'Katowice', 'country': 'Poland'},
            {'iata_code': 'LUZ', 'name': 'Lublin Airport', 'city': 'Lublin', 'country': 'Poland'},
            {'iata_code': 'RZE', 'name': 'Rzeszow Airport', 'city': 'Rzeszow', 'country': 'Poland'},
            {'iata_code': 'BZG', 'name': 'Bydgoszcz Airport', 'city': 'Bydgoszcz', 'country': 'Poland'},
            {'iata_code': 'SZZ', 'name': 'Szczecin Airport', 'city': 'Szczecin', 'country': 'Poland'},
            {'iata_code': 'MOD', 'name': 'Modlin Airport', 'city': 'Warsaw', 'country': 'Poland'},
            
            # Lithuania
            {'iata_code': 'KUN', 'name': 'Kaunas Airport', 'city': 'Kaunas', 'country': 'Lithuania'},
            {'iata_code': 'VNO', 'name': 'Vilnius Airport', 'city': 'Vilnius', 'country': 'Lithuania'},
            {'iata_code': 'PLQ', 'name': 'Palanga Airport', 'city': 'Palanga', 'country': 'Lithuania'},
            
            # Hungary
            {'iata_code': 'BUD', 'name': 'Budapest Ferenc Liszt Airport', 'city': 'Budapest', 'country': 'Hungary'},
            {'iata_code': 'DEB', 'name': 'Debrecen Airport', 'city': 'Debrecen', 'country': 'Hungary'},
            
            # Greece
            {'iata_code': 'ATH', 'name': 'Athens International Airport', 'city': 'Athens', 'country': 'Greece'},
            {'iata_code': 'SKG', 'name': 'Thessaloniki Airport', 'city': 'Thessaloniki', 'country': 'Greece'},
            {'iata_code': 'HER', 'name': 'Heraklion Airport', 'city': 'Heraklion', 'country': 'Greece'},
            {'iata_code': 'CHQ', 'name': 'Chania Airport', 'city': 'Chania', 'country': 'Greece'},
            {'iata_code': 'RHO', 'name': 'Rhodes Airport', 'city': 'Rhodes', 'country': 'Greece'},
            {'iata_code': 'KGS', 'name': 'Kos Airport', 'city': 'Kos', 'country': 'Greece'},
            {'iata_code': 'ZTH', 'name': 'Zakynthos Airport', 'city': 'Zakynthos', 'country': 'Greece'},
            {'iata_code': 'CFU', 'name': 'Corfu Airport', 'city': 'Corfu', 'country': 'Greece'},
            {'iata_code': 'JMK', 'name': 'Mykonos Airport', 'city': 'Mykonos', 'country': 'Greece'},
            {'iata_code': 'JTR', 'name': 'Santorini Airport', 'city': 'Santorini', 'country': 'Greece'},
            {'iata_code': 'PVK', 'name': 'Preveza Airport', 'city': 'Preveza', 'country': 'Greece'},
            {'iata_code': 'KVA', 'name': 'Kavala Airport', 'city': 'Kavala', 'country': 'Greece'},
            
            # Denmark
            {'iata_code': 'CPH', 'name': 'Copenhagen Airport', 'city': 'Copenhagen', 'country': 'Denmark'},
            {'iata_code': 'BLL', 'name': 'Billund Airport', 'city': 'Billund', 'country': 'Denmark'},
            {'iata_code': 'AAL', 'name': 'Aalborg Airport', 'city': 'Aalborg', 'country': 'Denmark'},
            {'iata_code': 'AAR', 'name': 'Aarhus Airport', 'city': 'Aarhus', 'country': 'Denmark'},
            
            # Sweden
            {'iata_code': 'ARN', 'name': 'Stockholm Arlanda Airport', 'city': 'Stockholm', 'country': 'Sweden'},
            {'iata_code': 'GOT', 'name': 'Gothenburg Airport', 'city': 'Gothenburg', 'country': 'Sweden'},
            {'iata_code': 'MMX', 'name': 'Malmo Airport', 'city': 'Malmo', 'country': 'Sweden'},
            
            # Norway
            {'iata_code': 'OSL', 'name': 'Oslo Gardermoen Airport', 'city': 'Oslo', 'country': 'Norway'},
            {'iata_code': 'TRD', 'name': 'Trondheim Airport', 'city': 'Trondheim', 'country': 'Norway'},
            {'iata_code': 'BGO', 'name': 'Bergen Airport', 'city': 'Bergen', 'country': 'Norway'},
            {'iata_code': 'SVG', 'name': 'Stavanger Airport', 'city': 'Stavanger', 'country': 'Norway'},
            
            # Finland
            {'iata_code': 'HEL', 'name': 'Helsinki-Vantaa Airport', 'city': 'Helsinki', 'country': 'Finland'},
            {'iata_code': 'TMP', 'name': 'Tampere Airport', 'city': 'Tampere', 'country': 'Finland'},
            {'iata_code': 'TKU', 'name': 'Turku Airport', 'city': 'Turku', 'country': 'Finland'},
            
            # Croatia
            {'iata_code': 'ZAG', 'name': 'Zagreb Airport', 'city': 'Zagreb', 'country': 'Croatia'},
            {'iata_code': 'SPU', 'name': 'Split Airport', 'city': 'Split', 'country': 'Croatia'},
            {'iata_code': 'DBV', 'name': 'Dubrovnik Airport', 'city': 'Dubrovnik', 'country': 'Croatia'},
            {'iata_code': 'PUY', 'name': 'Pula Airport', 'city': 'Pula', 'country': 'Croatia'},
            {'iata_code': 'ZAD', 'name': 'Zadar Airport', 'city': 'Zadar', 'country': 'Croatia'},
            {'iata_code': 'RJK', 'name': 'Rijeka Airport', 'city': 'Rijeka', 'country': 'Croatia'},
            
            # Slovenia
            {'iata_code': 'LJU', 'name': 'Ljubljana Airport', 'city': 'Ljubljana', 'country': 'Slovenia'},
            
            # Slovakia
            {'iata_code': 'BTS', 'name': 'Bratislava Airport', 'city': 'Bratislava', 'country': 'Slovakia'},
            {'iata_code': 'KSC', 'name': 'Kosice Airport', 'city': 'Kosice', 'country': 'Slovakia'},
            
            # Romania
            {'iata_code': 'OTP', 'name': 'Bucharest Airport', 'city': 'Bucharest', 'country': 'Romania'},
            {'iata_code': 'CLJ', 'name': 'Cluj-Napoca Airport', 'city': 'Cluj-Napoca', 'country': 'Romania'},
            {'iata_code': 'TSR', 'name': 'Timisoara Airport', 'city': 'Timisoara', 'country': 'Romania'},
            {'iata_code': 'IAS', 'name': 'Iasi Airport', 'city': 'Iasi', 'country': 'Romania'},
            
            # Bulgaria
            {'iata_code': 'SOF', 'name': 'Sofia Airport', 'city': 'Sofia', 'country': 'Bulgaria'},
            {'iata_code': 'BOJ', 'name': 'Burgas Airport', 'city': 'Burgas', 'country': 'Bulgaria'},
            {'iata_code': 'VAR', 'name': 'Varna Airport', 'city': 'Varna', 'country': 'Bulgaria'},
            {'iata_code': 'PDV', 'name': 'Plovdiv Airport', 'city': 'Plovdiv', 'country': 'Bulgaria'},
            
            # Serbia
            {'iata_code': 'BEG', 'name': 'Belgrade Airport', 'city': 'Belgrade', 'country': 'Serbia'},
            {'iata_code': 'INI', 'name': 'Nis Airport', 'city': 'Nis', 'country': 'Serbia'},
            
            # Bosnia and Herzegovina
            {'iata_code': 'SJJ', 'name': 'Sarajevo Airport', 'city': 'Sarajevo', 'country': 'Bosnia and Herzegovina'},
            {'iata_code': 'BNX', 'name': 'Banja Luka Airport', 'city': 'Banja Luka', 'country': 'Bosnia and Herzegovina'},
            {'iata_code': 'OMO', 'name': 'Mostar Airport', 'city': 'Mostar', 'country': 'Bosnia and Herzegovina'},
            
            # Montenegro
            {'iata_code': 'TGD', 'name': 'Podgorica Airport', 'city': 'Podgorica', 'country': 'Montenegro'},
            {'iata_code': 'TIV', 'name': 'Tivat Airport', 'city': 'Tivat', 'country': 'Montenegro'},
            
            # North Macedonia
            {'iata_code': 'SKP', 'name': 'Skopje Airport', 'city': 'Skopje', 'country': 'North Macedonia'},
            {'iata_code': 'OHD', 'name': 'Ohrid Airport', 'city': 'Ohrid', 'country': 'North Macedonia'},
            
            # Albania
            {'iata_code': 'TIA', 'name': 'Tirana Airport', 'city': 'Tirana', 'country': 'Albania'},
            
            # Kosovo
            {'iata_code': 'PRN', 'name': 'Pristina Airport', 'city': 'Pristina', 'country': 'Kosovo'},
            
            # Malta
            {'iata_code': 'MLA', 'name': 'Malta Airport', 'city': 'Malta', 'country': 'Malta'},
            
            # Cyprus
            {'iata_code': 'LCA', 'name': 'Larnaca Airport', 'city': 'Larnaca', 'country': 'Cyprus'},
            {'iata_code': 'PFO', 'name': 'Paphos Airport', 'city': 'Paphos', 'country': 'Cyprus'},
            
            # Israel
            {'iata_code': 'TLV', 'name': 'Tel Aviv Airport', 'city': 'Tel Aviv', 'country': 'Israel'},
            {'iata_code': 'OVD', 'name': 'Ovda Airport', 'city': 'Ovda', 'country': 'Israel'},
            
            # Jordan
            {'iata_code': 'AMM', 'name': 'Amman Airport', 'city': 'Amman', 'country': 'Jordan'},
            
            # Morocco
            {'iata_code': 'RAK', 'name': 'Marrakech Airport', 'city': 'Marrakech', 'country': 'Morocco'},
            {'iata_code': 'CMN', 'name': 'Casablanca Airport', 'city': 'Casablanca', 'country': 'Morocco'},
            {'iata_code': 'AGA', 'name': 'Agadir Airport', 'city': 'Agadir', 'country': 'Morocco'},
            {'iata_code': 'FEZ', 'name': 'Fes Airport', 'city': 'Fes', 'country': 'Morocco'},
            {'iata_code': 'TNG', 'name': 'Tangier Airport', 'city': 'Tangier', 'country': 'Morocco'},
            {'iata_code': 'NDR', 'name': 'Nador Airport', 'city': 'Nador', 'country': 'Morocco'},
            
            # Tunisia
            {'iata_code': 'TUN', 'name': 'Tunis Airport', 'city': 'Tunis', 'country': 'Tunisia'},
            {'iata_code': 'MIR', 'name': 'Monastir Airport', 'city': 'Monastir', 'country': 'Tunisia'},
            {'iata_code': 'DJE', 'name': 'Djerba Airport', 'city': 'Djerba', 'country': 'Tunisia'},
            {'iata_code': 'SFA', 'name': 'Sfax Airport', 'city': 'Sfax', 'country': 'Tunisia'},
            
            # Egypt
            {'iata_code': 'CAI', 'name': 'Cairo Airport', 'city': 'Cairo', 'country': 'Egypt'},
            {'iata_code': 'SSH', 'name': 'Sharm El Sheikh Airport', 'city': 'Sharm El Sheikh', 'country': 'Egypt'},
            {'iata_code': 'HRG', 'name': 'Hurghada Airport', 'city': 'Hurghada', 'country': 'Egypt'},
            
            # Turkey
            {'iata_code': 'IST', 'name': 'Istanbul Airport', 'city': 'Istanbul', 'country': 'Turkey'},
            {'iata_code': 'SAW', 'name': 'Sabiha Gokcen Airport', 'city': 'Istanbul', 'country': 'Turkey'},
            {'iata_code': 'AYT', 'name': 'Antalya Airport', 'city': 'Antalya', 'country': 'Turkey'},
            {'iata_code': 'BJV', 'name': 'Bodrum Airport', 'city': 'Bodrum', 'country': 'Turkey'},
            {'iata_code': 'DLM', 'name': 'Dalaman Airport', 'city': 'Dalaman', 'country': 'Turkey'},
            {'iata_code': 'ADB', 'name': 'Izmir Airport', 'city': 'Izmir', 'country': 'Turkey'},
            
            # Ukraine
            {'iata_code': 'KBP', 'name': 'Kyiv Airport', 'city': 'Kyiv', 'country': 'Ukraine'},
            {'iata_code': 'LWO', 'name': 'Lviv Airport', 'city': 'Lviv', 'country': 'Ukraine'},
            {'iata_code': 'ODS', 'name': 'Odessa Airport', 'city': 'Odessa', 'country': 'Ukraine'},
            {'iata_code': 'KHE', 'name': 'Kherson Airport', 'city': 'Kherson', 'country': 'Ukraine'},
        ]
    
    def search_all_destinations(self, origin_iata: str, 
                            departure_date_from: str, departure_date_to: str,
                            passengers: int = 1) -> List[Dict]:
        """
        Search for flights to all destinations from a given origin
        Returns cheapest flights for each destination in the date range
        """
        try:
            # Get all airports to search as destinations
            airports = self.get_airports()
            all_flights = []
            
            # Search for each destination (excluding the origin)
            for airport in airports:
                dest_iata = airport['iata_code']
                if dest_iata == origin_iata:
                    continue
                
                # Search flights to this destination
                flights_to_dest = self._search_one_way(
                    origin_iata, dest_iata,
                    departure_date_from, departure_date_to, passengers
                )
                
                if flights_to_dest:
                    # Add the cheapest flight for this destination
                    cheapest_flight = min(flights_to_dest, key=lambda x: x['price'])
                    cheapest_flight['destination_name'] = f"{dest_iata} - {airport['name']}, {airport['city']}"
                    all_flights.append(cheapest_flight)
            
            # Sort by price
            all_flights.sort(key=lambda x: x['price'])
            return all_flights[:20]  # Return top 20 cheapest destinations
            
        except Exception as e:
            print(f"Error searching all destinations: {e}")
            return []

    def search_flights(self, origin_iata: str, destination_iata: Optional[str] = None, 
                      departure_date_from: str = '', departure_date_to: str = '',
                      return_date_from: Optional[str] = None, 
                      return_date_to: Optional[str] = None,
                      passengers: int = 1) -> List[Dict]:
        """
        Search for flights within date ranges
        Returns cheapest flights for each day in the range
        """
        flights = []
        
        # If no destination specified, search all destinations
        if not destination_iata:
            return self.search_all_destinations(
                origin_iata, departure_date_from, departure_date_to, passengers
            )
        
        # Search outbound flights
        outbound_flights = self._search_one_way(
            origin_iata, destination_iata, 
            departure_date_from, departure_date_to, passengers
        )
        flights.extend(outbound_flights)
        
        # Search return flights if dates provided
        if return_date_from and return_date_to:
            return_flights = self._search_one_way(
                destination_iata, origin_iata,
                return_date_from, return_date_to, passengers
            )
            flights.extend(return_flights)
        
        return flights
    
    def _search_one_way(self, origin_iata: str, destination_iata: str,
                       date_from: str, date_to: str, passengers: int) -> List[Dict]:
        """Search one-way flights for a date range"""
        try:
            # Use the desktopapps API for flight search
            url = "https://desktopapps.ryanair.com/en-gb/availability"
            
            all_flights = []
            
            # Search each day in the range
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            
            current_date = date_from_obj
            while current_date <= date_to_obj:
                date_str = current_date.strftime('%Y-%m-%d')
                
                params = {
                    'ADT': passengers,
                    'CHD': 0,
                    'INF': 0,
                    'TEEN': 0,
                    'DateOut': date_str,
                    'DateIn': '',  # One-way
                    'Destination': destination_iata,
                    'Origin': origin_iata,
                    'RoundTrip': 'false',
                    'FlexDaysOut': 6,
                    'FlexDaysIn': 0,
                    'ToUs': 'AGREED'
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Process the response
                trips = data.get('trips', [])
                if trips:
                    for trip in trips[0].get('dates', []):
                        for date_info in trip.get('flights', []):
                            for flight in date_info.get('regularFares', {}).get('fares', []):
                                price = flight.get('price', {}).get('value', 0)
                                currency = flight.get('price', {}).get('currencyCode', 'EUR')
                                
                                all_flights.append({
                                    'flight_number': flight.get('flightKey', ''),
                                    'origin': origin_iata,
                                    'destination': destination_iata,
                                    'departure_time': flight.get('departureTime', ''),
                                    'arrival_time': flight.get('arrivalTime', ''),
                                    'price': price,
                                    'currency': currency,
                                    'available_seats': flight.get('availableSeats', 0),
                                    'date': date_str
                                })
                
                current_date += timedelta(days=1)
            
            return all_flights
            
        except requests.RequestException as e:
            print(f"Error searching flights from Ryanair API: {e}")
            print("Using mock flight data for demonstration...")
            return self._get_mock_flights(origin_iata, destination_iata, date_from, date_to, passengers)
    
    def _get_mock_flights(self, origin_iata: str, destination_iata: str,
                         date_from: str, date_to: str, passengers: int) -> List[Dict]:
        """Generate mock flight data for demonstration purposes"""
        import random
        
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
        
        mock_flights = []
        current_date = date_from_obj
        
        # Generate 1-3 flights per day
        while current_date <= date_to_obj:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Generate random number of flights for this day
            num_flights = random.randint(1, 3)
            
            for i in range(num_flights):
                # Generate random flight times
                departure_hour = random.randint(6, 22)
                departure_minute = random.choice([0, 15, 30, 45])
                flight_duration = random.randint(1, 4)  # 1-4 hours
                
                departure_time = f"{current_date.strftime('%Y-%m-%d')}T{departure_hour:02d}:{departure_minute:02d}:00"
                # Calculate arrival time properly handling hour overflow
                arrival_datetime = current_date.replace(hour=departure_hour, minute=departure_minute) + timedelta(hours=flight_duration)
                arrival_time = arrival_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                
                # Generate realistic prices based on route popularity
                base_price = random.uniform(20, 150)
                if origin_iata in ['DUB', 'STN', 'LTN'] or destination_iata in ['DUB', 'STN', 'LTN']:
                    base_price *= 1.2  # Popular routes are more expensive
                
                price = round(base_price * passengers, 2)
                
                mock_flights.append({
                    'flight_number': f"FR{random.randint(1000, 9999)}",
                    'origin': origin_iata,
                    'destination': destination_iata,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'price': price,
                    'currency': 'EUR',
                    'available_seats': random.randint(5, 50),
                    'date': date_str
                })
            
            current_date += timedelta(days=1)
        
        # Sort by price
        mock_flights.sort(key=lambda x: x['price'])
        
        return mock_flights
    
        
    def get_cheapest_flights_in_range(self, origin_iata: str, destination_iata: Optional[str] = None,
                                    departure_date_from: str = '', departure_date_to: str = '',
                                    return_date_from: Optional[str] = None,
                                    return_date_to: Optional[str] = None,
                                    passengers: int = 1) -> Dict:
        """
        Get cheapest flights within the specified date ranges
        Returns both outbound and return flights organized by cheapest options
        """
        all_flights = self.search_flights(
            origin_iata, destination_iata,
            departure_date_from, departure_date_to,
            return_date_from, return_date_to,
            passengers
        )
        
        # If searching all destinations, return flights as outbound only
        if not destination_iata:
            return {
                'outbound': all_flights[:20],  # Top 20 cheapest destinations
                'return': [],  # No return flights for all destinations search
                'total_flights_found': len(all_flights)
            }
        
        # Separate outbound and return flights
        outbound_flights = [f for f in all_flights if f['origin'] == origin_iata]
        return_flights = [f for f in all_flights if f['origin'] == destination_iata]
        
        # Sort by price
        outbound_flights.sort(key=lambda x: x['price'])
        return_flights.sort(key=lambda x: x['price'])
        
        return {
            'outbound': outbound_flights[:10],  # Top 10 cheapest outbound
            'return': return_flights[:10] if return_flights else [],  # Top 10 cheapest return
            'total_flights_found': len(all_flights)
        }
