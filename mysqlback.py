#!/usr/bin/env python
#coding=utf8
import  MySQLdb,os

# os.system('mysqldump -u chenweimeng -pcwmasdasd icgoo-v721>/home/chenweimeng/v721.bak')
db_new=MySQLdb.connect("192.168.2.161","icgoov7","asdasd","icgoo-v73" )
db_old=MySQLdb.connect("192.168.2.161","icgoov7","asdasd","icgoo-v721" )

cursor_new = db_new.cursor()
cursor_old = db_old.cursor()
cursor_new.execute('show tables')
new_table_list=list(cursor_new.fetchall())
cursor_old.execute('show tables')
old_table_list=list(cursor_old.fetchall())
equal_list=[]
no_equal = []
for i in new_table_list:
    if i in old_table_list:
        if cursor_old.execute('show columns from %s' %i) == cursor_new.execute('show columns from %s' %i) :

            equal_list.append(i)
        else:
            if i[0] != 'accounts_useraddressinfo':
                equal_list.append(i)


print  equal_list
print len(equal_list)


for  j in equal_list:
    if j[0]!='webconfig_webconfig':
        continue
    command='mysqldump -u chenweimeng -pcwmasdasd --add-drop-table icgoo-v721 %s | mysql  -u chenweimeng -pcwmasdasd  icgoo-v73' %j[0]
    print command
    status=os.system(command)
    if not status:
        print 'success %s' %j
    else:
        print 'wrong %s' %i
    if j[0]=='search_supplier':
        cursor_new.execute('alter table search_supplier add COLUMN  is_can_demand_pack tinyint(1) not null')
        cursor_new.execute('alter table  search_supplier add  COLUMN  not_added_dc_info tinyint(1) not null default 1')


db_new.close()
db_old.close()






