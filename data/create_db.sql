/* database creation */

drop table if exists notices;
drop table if exists member;

create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table notices(
     notices_id integer primary key autoincrement not null,
     title text not null unique,
     content text not null unique,
     noticedate date not null,
     member_id integer not null,
     foreign key(member_id) references member(member_id)
);

insert into member( name, email, password, authorisation)
values ('Mike', 'm@g.com', 'temp', 0);
insert into member( name, email, password, authorisation)
values ('Vannesa', 'v@g.com', 'temp', 0);
insert into member( name, email, password, authorisation)
values ('Olivia', 'o@g.com', 'temp', 1);
insert into member( name, email, password, authorisation)
values ('Suzie', 's@g.com', 'temp', 1);

insert into notices(title, content, noticedate, member_id)
values('Cancelled!',
       'All netball games played outside are cancelled due to rain',
       '2023-03-04 20:30:00',
       (select member_id from member where name='Mike')
);

insert into notices(title, content, noticedate, member_id)
values('Congrats!',
       'Congratulations to our teams who all won their games',
       '2023-03-12 17:45:00',
       (select member_id from member where name='Vannesa')
);


insert into notices(title, content, noticedate, member_id)
values('Training!',
       'Training cancelled on Thursday, due to coach being sick',
       '2023-03-14 12:38:00',
       (select member_id from member where name='Vannesa')
);