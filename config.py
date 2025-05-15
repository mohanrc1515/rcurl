import os, time, re
id_pattern = re.compile(r'^.\d+$')



class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "12655645")
    API_HASH  = os.environ.get("API_HASH", "05c4cafe00b81ed83207bb4365e0053b")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7696984863:AAEiUA76NTYiQ2dYlCzxEAaymT_FMnnkKpM") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","mohan")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://mohan:rc151515@cluster0.evtah9f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1025922801').split()]

    # channels logs
    FORCE_SUB   = os.environ.get("FORCE_SUB", "") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001714238387"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))



class Txt(object):
    # part of text configuration
    START_TXT = """Hello {} 👋 

➻ RC RENAME BOT வணக்கம் 
"""

    
