from aip import AipNlp
from snownlp import SnowNLP
from NewsSpider import settings
import pymysql

APP_ID = '11267465'
API_KEY = 'xdW8oXbVD9tGY5OztwGUV4CE'
SECRET_KEY = 'XHVhwKpVfn1LDjjVXfO3h7XtGob5mSad'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
# text='兵马俑在美展出时手指受损 陕西文物部门怒斥美方博物馆：如此恶性前所未有'
# result=client.sentimentClassify(text)
# print(result)
class  textAnalysis:
    #初始化时连接数据库，分析时从数据库中取出正文进行分析
    def __init__(self):
        self.connect=pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor=self.connect.cursor()
        for data in self.getRawData():
            newsid,emotion=self.operation(data)
            self.update(newsid,emotion)


    #获得原始数据
    def getRawData(self):
        self.cursor.execute('select id,title from news')
        return self.cursor.fetchall()

    #进行分析
    def operation(self,data):
        # print(data)
        newsid=data[0]
        content=''.join(data[1:])
        result=client.sentimentClassify(content[0])
        data=result['items']
        items=data[0]
        positive_prob = items['positive_prob']
        negative_prob = items['negative_prob']
        print("新闻id:"+str(newsid))
        print("正面程度:"+str(positive_prob))
        print("负面程度:"+str(negative_prob))
        if positive_prob>negative_prob:
            emotion=1
        else:
            emotion=0
        # print(emotion)
        return (newsid,emotion)

    #更新数据库
    def update(self,newsid,emotion):
        self.cursor.execute(
            'update news set nature = {} where id = {}'.format(emotion, newsid)
        )
        self.connect.commit()


if __name__ == '__main__':
    textAnalysis()
