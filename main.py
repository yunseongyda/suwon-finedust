import requests
import config

airKorURL = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'

params = {
  "serviceKey" : config.AIRKOREA_API_KEY,
  "returnType" : "json",
  "numOfRows" : 
}