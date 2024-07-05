# AetherDB
AetherDB is a simple lightweight db stored entirely inside json files and folders. AetherDB is document-like based db, but rather than storing each document as separate json it stores all documents inside json clusters. Data stored in following format:
```json
cluster_0.json
{
    "document_id": {
        "key1": "value1",
        "key2": "value2",
        ...
    }
}
```
Any data type supported by json can be stored.
## Installation
```
pip install aetherdb
```
## Usage
To open db you simply need to create db class instance, specifying path to your db folder. If folder (or folders) in path does not exists they will be created.
```python
from aetherdb import DB
db = DB("path_to_your_DB_folder")
```
After that you can do all kinds of operations on your DB by calling created class instance`s methods.
```python
# Open sub db (create if there is no such sub db)
db.open_sub_db("sub_db_name")
# Create sub db
db.create_sub_db("sub_db_name")
# Delete sub db
db.delete_sub_db("sub_db_name")
# Write butch of data
db.write({"document_id" : { some_data }})
# Read data by document id
db.read("document_id")
# Update data by id
db.update("document_id", { new_data })
# Delete data by id
db.delete("document_id")
# Backup db
db.backup("path_to_where_backup_should_be_stored")
# Make query request to db
db.query("query_text")
```
## Query syntax
Query supports a fixed list of requests:
- selectById{}
- selectByIdRegex{}
- selectWhere{}
- selectWhereRegex{}
- withDB{}
- createDB{}
- deleteSelection{}
- delete{}
- update{}
- insert{}
- withParentDB{}
- filter{}
- backup{}
- return{}
Requests can be chained using ".", for example:
```
selectById{"id"}.return{}
```
All requests should have {}, even if they dont need any data. Data needed for request can be passed inside {}. Each request require some set of data to function.
### Selectors
Selectors will select data from db by some specified data like document id. Selected data will be saved until query will be completed, but will not be returnd unless specified by other requests.
#### selectById
Requires string containig document id to search in db.
```python
selectById{"some_document_id"}
```
#### selectByIdRegex
Requires regular expression to match document ids and returns all data with document ids matching given regular expression.
```python
# This request will select every possible document
selectByIdRegex{".*"}
```
#### selectWhere
Requires comma separated key-value pairs in format `key=value` to search data with same key-value pairs.
```python
selectWhere{"key1=value1,key2=value2"}
```
#### selectWhereRegex
Requires comma separated key-value pairs in format `key=value` to search data with same key-value pairs. Values can be regular expressions to match.
```python
selectWhereRegex{"key1=.*,key2=value2"}
```
### withDB
Requires sub db name. Will open sub db and pass all requests after this request to sub db. Will return averything that sub db will return.
```python
withDB{"sub_db_name"}
```
### createDB
Requires sub db name. Will create sub db with specified name.
```python
createDB{"sub_db_name"}
```
### deleteSelection
Does not require any input. Will delete all data selected by previous requests from db.
```python
deleteSelection{}
```
### delete
Requires document id. Will delete document with specified id from db.
```python
delete{}
```
### update
Requires document id and data to write in document separated by comma. Will update data written in document with specified id to specified data.
```python
update{"document_id,{'key1':'value1','key2':'value2'}"}
```
### insert
Requires data to write to db. Data should be in following format:
```json
{
    "document_id": {
        "key1": "value1",
        "key2": "value2",
        ...
    }
}
```
Data will be added to db.
```python
insert{"{'document_id':{'key1':'value1','key2':'value2',...}}"}
```
### withParentDB
Does not require any input. Will open db in which this sub db is located  and pass all requests after this request to it. If used inside root db will do nothing (Will work only after `withDB`). Will return anything everything that opened db will return.
```python
withParentDB{}
```
### filter
Requires comma separated key-value pairs in format `key=value`. Will filter out all data selected by previous requests and leave in result only data that will match key-value pairs.
```python
filter{"key1=value1,key2=value2"}
```
### backup
Require optional path to where backup should be stored. Will create zip containing backup of current db at specified location. If path not specified backup will be created inside db in backup folder.
```python
backup{"path_to_backup_folder"}
```
### return
Does not require any input. Will return all data selected by previous requests. After this request query will finish, other requests after this will be ignored.
```python
return{}
```
## Contribution
Pull requests will be mostly ignored for now unless they fix some security issues. Please specify what and how your changes will fix.