import sys
import os
import pandas as pd
import xlrd

def calculate_id(name):
    names = name.split(' ')
    id_ = names[1][0] + '/' + names[1][:5] + names[0][:2]
    return id_.lower()

def get_names_and_scrape_bbref():
    """
    download excel file and go by names one by one
    for each row:
        grab id
        grab date of season ending
        call main(id, year, name)

        grab pickle files dataframe and 
        append pickle file to current name
    """
    df = pd.read_excel(r'../Eligible_List.xlsx',sheet_name='Data')
    eligible_df = df[df['Eligible?'] == 1]

    for row,col in eligible_df.iterrows():
        name = eligible_df.name[row]
        season = eligible_df.Season[row][5:]
        id_ = calculate_id(name)
        # grab players stats using the main function
        main(id_, season, name)


def main(id, year, name):
    cmd_line = "scrapy crawl bballRef " + "-a id=" + id + " -a year=" + year + " -a name=" + "\"" + name + "\"" 
    print (cmd_line)
    os.system(cmd_line)


if __name__ == '__main__':
    # if len(sys.argv) != 4:
    #     print('eg. id, year, name')
    #     sys.exit(1)
    get_names_and_scrape_bbref()
    #main(sys.argv[1], sys.argv[2], sys.argv[3])