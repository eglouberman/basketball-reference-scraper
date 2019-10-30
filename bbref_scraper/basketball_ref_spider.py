import scrapy
from scrapy.http import HtmlResponse
import re
import pickle
import pandas as pd
import os

class BasketballReferenceSpider(scrapy.Spider):
    name = "bballRef"

    def __init__ (self, id = "", year = 2018, name = "", **kwargs):
        self.id = id
        self.log("ID:" + self.id)
        self.year = year
        self.log("year:" + self.year)
        # name is to verify that the page yields the correct player
        self.name = name
        self.log("name:" + self.name)

        super().__init__(**kwargs)

    def start_requests(self):
        urls = [
            'https://www.basketball-reference.com/players/' + self.id + '.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_per_poss)
    
    def appendDFToCSV_void(self, df, csvFilePath, sep=","):
        if not os.path.isfile(csvFilePath):
            df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
        else:
            df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)

    def parse_all_per_poss(self, response):
        """
        List of stats from first source, BBRef per 100 poss:
        DRtg, last item in list of stats from a given year. 
        """
        stats_scraped_into_df = pd.DataFrame()
        # xml path for commented sections: DRTG
        extracted_text = response.xpath('//div[@class="table_wrapper setup_commented commented"][@id="all_per_poss"]').extract_first()
        newer_response = re.sub("<!--", "", str(extracted_text), flags=re.DOTALL)
        newest_response = re.sub("-->", "", newer_response, flags=re.DOTALL)  
        all_per_poss_response = HtmlResponse(url = "my string", body = newest_response, encoding = 'utf-8')
        list_of_stats = all_per_poss_response.xpath('//table[@id="per_poss"]//tr[@id=\"per_poss.'+ str(self.year) + '\"]//td/text()').extract()
        self.log(list_of_stats)
        try:
            DRTG = list_of_stats[-1]
            self.log("DRTG: " + str(DRTG))
        except:
            pass
       
        # parse advanced table (function below)
        """
        List of stats from second source table, BBRef advanced:
        Def. BPM
        Def. WS/48
        Blk %
        Stl %
        Off Reb %
        Def Reb %
        True Reb %
        """
        self.log("EXTRACTING ADVANCED NOW")
        try:
            extracted_text = response.xpath('//div[@class="table_wrapper setup_commented commented"][@id="all_advanced"]').extract_first()
            newer_response = re.sub("<!--", "", extracted_text, flags=re.DOTALL)
            newest_response = re.sub("-->", "", newer_response, flags=re.DOTALL)  
            all_per_poss_response = HtmlResponse(url = "my string", body = newest_response, encoding = 'utf-8')
            DefBPM = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="dbpm"]//text()').extract()
            DefWS = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="ws_per_48"]//text()').extract()
            blk_p = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="blk_pct"]//text()').extract()
            stl_p = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="stl_pct"]//text()').extract()
            Or_p = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="orb_pct"]//text()').extract()
            Dr_p = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="drb_pct"]//text()').extract()
            Tr_p = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="trb_pct"]//text()').extract()
            mp = all_per_poss_response.xpath('//table[@id="advanced"]//tr[@id="advanced.'+ self.year +'"]//td[@data-stat="mp"]//text()').extract()
            stats_scraped_into_df.loc[0, 'Name'] = self.name
            stats_scraped_into_df.loc[0, 'Season'] = self.year
            stats_scraped_into_df.loc[0, 'DRTG'] = DRTG
            self.log(DefBPM)
            if (len(DefBPM) >1):
                stats_scraped_into_df.loc[0, 'MP'] = mp[0]
                stats_scraped_into_df.loc[0, 'Def. BPM'] = DefBPM[0]
                stats_scraped_into_df.loc[0, 'Def. WS/48'] = DefWS[0]
                stats_scraped_into_df.loc[0, 'Stl %'] = stl_p[0]
                stats_scraped_into_df.loc[0, 'Blk %'] = blk_p[0]
                stats_scraped_into_df.loc[0, 'Off Reb %'] = Or_p[0]
                stats_scraped_into_df.loc[0, 'Def Reb %'] = Dr_p[0]
                stats_scraped_into_df.loc[0, 'True Reb %'] = Tr_p[0]

            else:
                stats_scraped_into_df.loc[0, 'MP'] = mp
                stats_scraped_into_df.loc[0, 'Def. BPM'] = DefBPM
                stats_scraped_into_df.loc[0, 'Def. WS/48'] = DefWS
                stats_scraped_into_df.loc[0, 'Stl %'] = stl_p
                stats_scraped_into_df.loc[0, 'Blk %'] = blk_p
                stats_scraped_into_df.loc[0, 'Off Reb %'] = Or_p
                stats_scraped_into_df.loc[0, 'Def Reb %'] = Dr_p
                stats_scraped_into_df.loc[0, 'True Reb %'] = Tr_p
            self.log(stats_scraped_into_df)
            # stats_scraped_into_df.to_csv("../bbrefDF.csv")
            self.appendDFToCSV_void(stats_scraped_into_df,"../bbrefDF.csv", )
        except:
            self.appendDFToCSV_void(stats_scraped_into_df,"../bbrefDF.csv", )
            
        

        


# xml path for per game stats: response.xpath('//table[@id="per_game"]//tr[@id="per_game.YEAR"]//td/text()').extract()

# xml path for commented sections: DRTG
#   response.xpath('//div[@class="table_wrapper setup_commented commented"][@id="all_per_poss"]').extract_first()

# xml path for: Def. BPM, Def. WS/48, Blk %, Stl %,Off Reb %,Def Reb %,True Reb %
# new_response = response.xpath('//div[@class="table_wrapper setup_commented commented"][@id="all_advanced"]').extract_first()

#for commented out stats:
# 1. call extract_first() to get all of HTML.
"""
new_text = response.xpath('//div[@class="table_wrapper setup_commented commented"][@id="all_per_poss"]').extract_first()
newer_response = re.sub("<!--", "", new_text, flags=re.DOTALL)
newest_response = re.sub("-->", "", newer_response, flags=re.DOTALL)  
response = HtmlResponse(url = "my string", body = newest_response, encoding = 'utf-8')
response.xpath('//table[@id="per_poss"]//tr[@id="per_poss.YEAR"]//td/text()').extract()

--- continue with rest of parsing for new response! 

"""
# 2. clean HTML and rid of comments
# 3. Convert back to html response object
# 4. parse for stats