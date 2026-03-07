# from vnstock import Company

# # Khuyến nghị - Ổn định hơn cho Google Colab/Kaggle
# company = Company(symbol='VCB', source='KBS')

# # Hoặc sử dụng VCI (dữ liệu đầy đủ hơn)
# company = Company(symbol='VCB', source='VCI')
# print(company.overview())


from vnstock import Listing, Quote, Company, Finance, Trading, Screener
listing = Listing(source='KBS')
print(listing.all_symbols())