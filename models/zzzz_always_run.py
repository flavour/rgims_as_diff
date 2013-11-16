# -*- coding: utf-8 -*-

# always running script

tblname = "inv_inv_item"

# load the inv_inv_item table
# inventory table
table = s3db[tblname]

# check if inventory db table
# has already been created
# then update all expired items
# and near expired items

if tblname in db.tables:
    invtable = db.inv_inv_item
    
    query = ((invtable.expiry_date != None) &
        (invtable.deleted == False))
    
    # change to near expired (7)
    time_near_ex = current.request.now + datetime.timedelta(days=90)
    
    task = db(query &
        (invtable.expiry_date <= time_near_ex) &
        (invtable.expiry_date > current.request.now))
        
    if task.count():
        task.update(status=7)
    
    # change to expired (6)
    task = db(query &
        (invtable.expiry_date <= current.request.now))
        
    if task.count():
        task.update(status=6)
    
