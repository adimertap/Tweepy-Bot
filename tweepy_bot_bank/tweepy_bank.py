import tweepy
import time
from db_con import *
from keys import*
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def check_update():
    print("check data dari univ...\n",flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline( last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(mention.full_text.lower(), flush=True)
        hasil1 = (mention.full_text.lower().split("#"))[1]
        nim = (hasil1.split("-"))[0]
        nama = (hasil1.split("-"))[1]
        spp = int((hasil1.split("-"))[2])
        print(nim)
        print(nama)
        print(spp)
        insert = "insert into tb_pembayaran_ukt(nim, nama_mhs, nominal_ukt,status) values('%s','%s',%d,'0')" %(nim,nama, spp)
        cursor_db.execute(insert)
        db.commit()
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        # sql_select = "select * from tb_pembayaran_ukt"
        # cursor_db.execute(sql_select)
        # results = cursor_db.fetchall()
        # flag=0
        # for row in results:
        #     if row[1] in mention.full_text.lower():
        #         text=row[2]
        #         flag=flag+1
        # if flag == 0:
        #     text = "Semangat kak!"
        #
        # flag = 0
        # api.update_status('@' + mention.user.screen_name + ' ' + "widi", mention.id)
        # print("reply has been sent")

def send_update():
    select_pembayaran = "select *from tb_pembayaran_ukt where status_kirim = '0'"
    cursor_db.execute(select_pembayaran)
    db.commit()
    data = cursor_db.fetchall()
    for datum in data:
        if(datum[4]=='1'):
            nim_kirim = datum[1]
            status_pembayaran_kirim = datum[4]
            api.update_status('@ProjectKalahari' + ' #' +nim_kirim+"-"+status_pembayaran_kirim)
            update_status = "update tb_pembayaran_ukt set status_kirim ='1'"
            cursor_db.execute(update_status)
            db.commit()
            print("terdapat perubahan data dari bank")
            print("perubahan telah dikirim ke univ\n")

while True:
    check_update()
    send_update()
    time.sleep(3)


