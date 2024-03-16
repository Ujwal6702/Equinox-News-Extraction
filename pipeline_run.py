import luigi
import os
import datetime
from ScraperWorkFlow.mainScraper import mainWorkFlow


pipelineDirectory = os.path.dirname(os.path.abspath(__file__))
todayDate = datetime.datetime.today()


class RunScrapers(luigi.Task):
    
    
    scraperOutputFile = os.path.join(pipelineDirectory, "ScraperWorkFlow", "Output", "scraperOutput_"+todayDate.strftime("%d-%m-%Y")+".csv")
    
    
    def output(self):
        return luigi.LocalTarget(self.scraperOutputFile)
    
    def run(self):
        
        output = mainWorkFlow()
        output.to_csv(self.scraperOutputFile, index=False)
        
        



if  __name__ == "__main__":
    print(pipelineDirectory)