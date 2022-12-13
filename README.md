# Mind Map
![MindMap](学生管理系统%20Qt%20版本.png)
# Create sql table
## users
```sql
create table if not exists users(
    stuNumber varchar(20) primary key,
    password varchar(18),
    realname varchar(8),
    phonenumber varchar(11)
)
```
## loginUsers
```sql
create table if not exists loginUsers(
    stuNumber varchar(20) primary key
)
```