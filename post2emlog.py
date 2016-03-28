# -*- coding: utf-8 -*-
# Create a new post to emlog by python.
# Coded by Junchao Wang
# www.junchaowang.com
import MySQLdb, time

def jwemlogpost(title, content, abstract, tag_set):
    host = '' ## MySQL host
    user = '' ## MySQL username
    passwd = '' ## MySQL password
    db = '' ## MySQL database

    now_time = str(int(time.time()))


    try:
        conn = MySQLdb.connect(host, user, passwd, db, port=3306, charset="utf8")
        cur = conn.cursor()
        # get gid
        data = cur.execute('select max(gid) from emlog_blog')
        next_gid = str(cur.fetchmany(data)[0][0] + 1)
    ##    print next_gid

        # post title, content, abstract
        post_sql = "insert into emlog_blog(gid, date, title, excerpt, content) values " + \
                   "('" + next_gid + "','" + now_time + "','" + title + "','" + \
                   abstract + "','"  + content + "')"
    ##    print post_sql
        data = cur.execute(post_sql)
        
        # post tag
        for each_tag in tag_set:
            print each_tag
            tag = each_tag
            tag_sql = 'select * from emlog_tag where tagname like "%'  + tag + '%" '
            data = cur.execute(tag_sql)
    ##        print data
            if data != 0:
                info = cur.fetchmany(data)
                tid = info[0][0]
                old_gid = info[0][2]
                new_gid = old_gid + next_gid + ','
                update_tag_sql = "update emlog_tag set gid = '" \
                                 + new_gid + "' where tid = " + str(tid)
                cur.execute(update_tag_sql)
            else:
                new_tag_sql = "insert into emlog_tag(tagname, gid) values " + \
                              "('" + tag + "','," + next_gid + ",')"
                print new_tag_sql
                print cur.execute(new_tag_sql)
                
        
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
