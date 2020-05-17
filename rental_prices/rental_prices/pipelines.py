# -*- coding: utf-8 -*-
import logging
import sqlite3
from scrapy.exceptions import DropItem
import pandas as pd
from pathlib import Path


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class RentalPricesPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:

    def __init__(self):
        file_path = (Path(__file__).parent.parent /
                     'rental_prices.db').as_posix()
        self.connection = sqlite3.connect(file_path)
        df = pd.read_sql("SELECT Url from immobilienscout24",
                         con=self.connection)
        self.urls_seen = set(df['Url'].tolist())

    def process_item(self, item, spider):
        if item['Url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item['Url'])
        else:
            self.urls_seen.add(item['Url'])
            return item


class SQLLitePipeline(object):

    def open_spider(self, spider):
        file_path = (Path(__file__).parent.parent /
                     'rental_prices.db').as_posix()
        self.connection = sqlite3.connect(file_path)
        self.c = self.connection.cursor()
        try:
            self.c.execute("""
                    CREATE TABLE immobilienscout24(
                        Titel TEXT,
                        Url TEXT,
                        Kaltmiete TEXT,
                        Nebenkosten TEXT,
                        Heizkosten TEXT,
                        Gesamtmiete TEXT,
                        KautionGenossenschaftsanteile TEXT,
                        MieteGarageStellplatz TEXT,
                        Typ TEXT,
                        Etage TEXT,
                        Wohnfläche TEXT,
                        Bezugsfrei TEXT,
                        Zimmer TEXT,
                        Schlafzimmer TEXT,
                        Badezimmer TEXT,
                        Haustiere TEXT,
                        GarageStellplatz TEXT,
                        BalkonTerrasse TEXT,
                        Keller TEXT,
                        Personenaufzug TEXT,
                        Einbauküche TEXT,
                        GästeWC TEXT,
                        StufenloserZugang TEXT,
                        Baujahr TEXT,
                        ModernisierungSanierung TEXT,
                        Objektzustand TEXT,
                        Ausstattung TEXT,
                        Heizungsart TEXT,
                        WesentlicheEnergieträger TEXT,
                        Energieausweis TEXT,
                        Energieausweistyp TEXT,
                        Endenergieverbrauch TEXT,
                        Energieeffizienzklasse TEXT,
                        Anbieter TEXT,
                        Adreese TEXT,
                        Timestamp TEXT
                    )
            """),
            self.connection.commit(),
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute("""
            INSERT INTO immobilienscout24(
                Titel,
                Url,
                Kaltmiete,
                Nebenkosten,
                Heizkosten,
                Gesamtmiete,
                KautionGenossenschaftsanteile,
                MieteGarageStellplatz,
                Typ,
                Etage,
                Wohnfläche,
                Bezugsfrei,
                Zimmer,
                Schlafzimmer,
                Badezimmer,
                Haustiere,
                GarageStellplatz,
                BalkonTerrasse,
                Keller,
                Personenaufzug,
                Einbauküche,
                GästeWC,
                StufenloserZugang,
                Baujahr,
                ModernisierungSanierung,
                Objektzustand,
                Ausstattung,
                Heizungsart,
                WesentlicheEnergieträger,
                Energieausweis,
                Energieausweistyp,
                Endenergieverbrauch,
                Energieeffizienzklasse,
                Anbieter,
                Adreese,
                Timestamp
            )
            VALUES(
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """, (
            item.get("Titel"),
            item.get("Url"),
            item.get("Kaltmiete"),
            item.get("Nebenkosten"),
            item.get("Heizkosten"),
            item.get("Gesamtmiete"),
            item.get("Kaution o. Genossenschaftsanteile"),
            item.get("Miete für Garage/Stellplatz"),
            item.get("Typ"),
            item.get("Etage"),
            item.get("Wohnfläche ca."),
            item.get("Bezugsfrei ab"),
            item.get("Zimmer"),
            item.get("Schlafzimmer"),
            item.get("Badezimmer"),
            item.get("Haustiere"),
            item.get("Garage/ Stellplatz"),
            item.get("Balkon/ Terrasse"),
            item.get("Keller"),
            item.get("Personenaufzug"),
            item.get("Einbauküche"),
            item.get("Gäste-WC"),
            item.get("Stufenloser Zugang"),
            item.get("Baujahr"),
            item.get("Modernisierung/ Sanierung"),
            item.get("Objektzustand"),
            item.get("Ausstattung"),
            item.get("Heizungsart"),
            item.get("Wesentliche Energieträger"),
            item.get("Energieausweis"),
            item.get("Energieausweistyp"),
            item.get("Endenergieverbrauch"),
            item.get("Energieeffizienzklasse"),
            item.get("Anbieter"),
            item.get("Adreese"),
            str(item.get('Timestamp'))
        ))
        self.connection.commit()
