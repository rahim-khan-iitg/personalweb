from statsmodels.tsa.arima.model import ARIMA
import warnings 
import os
import requests
import pandas as pd
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

api_key=os.environ.get("ALPHAVENTAGE_API_KEY")

from dataclasses import dataclass

warnings.filterwarnings('ignore')

class DataTransformation:
    def __init__(self) -> None:
        pass
    
    def initiate_data_transformation(self,data_path,column)->tuple:
        try:
            df=pd.read_csv(data_path)
            data=df[[column]]
            train_data=data.iloc[0:70]
            test_data=data.iloc[70:]
            history=[x for x in train_data[column]]
            test_data=[x for x in test_data[column]]
            return (history,test_data)
        except Exception as e:
            pass


@dataclass
class DataIngestionConfig:
    data_path=os.path.join("artifacts","stocks.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self,key):
        try:
            data_url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={key}&output_size=compact&apikey={api_key}"
            os.makedirs(os.path.dirname(self.ingestion_config.data_path),exist_ok=True)
            response=requests.get(data_url)
            json_data=response.json()
            df=pd.DataFrame(json_data["Time Series (Daily)"])
            df=df.T
            df.columns=['open', 'high', 'low', 'close','volume']
            df.open=df.open.astype('float')
            df.high=df.high.astype('float')
            df.low=df.low.astype('float')
            df.close=df.close.astype('float')
            df.volume=df.volume.astype('float')
            df=df.iloc[::-1]

            df.to_csv(self.ingestion_config.data_path,index=True,header=True)
            return self.ingestion_config.data_path
        
        except Exception as e:
            pass


def start_training(key,col):
    obj=DataIngestion()
    data_path=obj.initiate_data_ingestion(key)
    obj2=DataTransformation()
    history,test_data=obj2.initiate_data_transformation(data_path,col)
    return (history,test_data)


class predict:
    def __init__(self,key,col) -> None:
        self.key=key
        self.col=col
    def make_prediction(self):
        try:
            history,test=start_training(self.key,self.col)
            pred=list()
            for i in range(len(test)):
                m=ARIMA(history,order=(1,1,1))
                res=m.fit()
                prediction=res.forecast()
                pred.append(prediction[0])
                history.append(test[i])
            m=ARIMA(history,order=(1,1,1))
            res=m.fit()
            next=res.forecast()
            return (test,pred,next)
        except Exception as e:
            pass
