def parse_ad(self, response):
    url = response.status
    title = response.xpath('//h1//text()').extract_first()

    details = response.xpath('//div[@class="clear"]//text()').extract()
    details = [e.strip() for e in details]
    details = [e for e in details if e != '']

    price_list_index = details.index('Preise')
    apartment_list_index = details.index('Immobilie')
    pricing = details[price_list_index+1:apartment_list_index]
    if '(in Warmmiete enthalten)' in pricing:
        pricing.remove('(in Warmmiete enthalten)')
    pricing_dict = dict(zip(pricing[::2], [e.replace(' €', '').replace('.', '').replace(',', '.')
                                           for e in pricing[1::2]]))

    wohnanlage_list_index = details.index('Wohnanlage')
    wohnung_list_index = details.index('Die Wohnung')
    ad_details = details[apartment_list_index+1:wohnung_list_index]

    wohnung_details = details[wohnung_list_index+1:wohnanlage_list_index]
    flat_type = wohnung_details[0]
    moving_in_date = wohnung_details[1]

    rennovated = False
    refurbished = False
    bath_tub = False
    hardwood_floor = False
    linoleum = False
    kitchen = False
    balcony = False
    basement = False

    for detail in wohnung_details:
        if 'Parkettboden' in detail:
            hardwood_floor = True
        elif 'Einbauküche' in detail:
            kitchen = True
        elif 'Linoleum' in detail:
            linoleum = True
        elif 'Wanne' in detail:
            bath_tub = True
        elif 'renoviert' in detail:
            rennovated = True
        elif 'saniert' in detail:
            refurbished = True
        elif 'Balkon' in detail:
            balcony = True
        elif 'Kelleranteil' in detail:
            basement = True

    Wanne

    renoviert

    hard_facts = response.xpath('//div[@class="hardfacts clear"]')
    for fact in hard_facts:
        cold_rent = fact.xpath('.//strong//text()').extract_first()
        cold_rent = cold_rent.replace(' €', '').replace('.', '').rep
        fact.xpath('.//text()').extract()

    final_dict = {
        'Titel': title,
        'Url': url,
        'Type': flat_type,
        'Frei ab': moving_in_date,


    }


[]
