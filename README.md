# basketball-reference-scraper

This scraper is written in Python and can be used to download defensive stats for any given player and season. It requires a xlsx file with a list of valid NBA player names and eligible seasons (the year being when the season ends). For example:

  <table>
  <tr>
    <th>Name</th>
    <th>Season</th>
  </tr>
  <tr>
    <td>James Harden</td>
    <td>2019</td> </tr>
  <tr>
    <td>Kyrie Irving</td>
    <td>2012</td> </tr></table>
 
 The web scraper then gets defensive results in the following categories:
 
 * DRTG (Points allowed per 100 possessions)
   
 * MP (Minutes Played
   
  * Defensive BPM (Overall Box plus minus – offensive BPM)
   
   * Def WS/48 min (Credited defensive win shares to players)
   
  * Stl
      
 * Blk
   
* Off. Reb
  
 * Def. Reb
  
 * Total. Reb % (Estimate of percentage of rebounds a player grabbed) 
 
 The results will be saved as a csv under your_output_file_name

## Dependencies and running the program: 

1. In command line, navigate to the parent directory folder where "requirements.txt" is located.

2. Run the code: 
 
    `pip install -r requirements.txt`
    
3. Cd into directory where "run_scrape.py" is stored

4. Run the code:

    `python run_scrape.py YOUR_DATA_FILE YOUR_OUPUT_FILE_NAME`
