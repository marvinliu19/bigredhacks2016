drop table if exists subscription;
create table subscription (
  id integer primary key autoincrement,
  phoneNumber text not null,
  crop not null
);
