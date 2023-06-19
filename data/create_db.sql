/* database creation */

drop table if exists notices;
drop table if exists member;
drop table if exists team;
drop table if exists game;
drop table if exists results;


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

create table team(
     team_name text not null
);

create table game(
     game_id integer primary key autoincrement not null,
     gamedate date not null,
     location text not null,
     team1 text not null ,
     team2 text not null
);

create table results(
     result_id integer primary key autoincrement not null,
     resultdate date not null,
     team1 text not null ,
     score1 integer,
     team2 text not null,
     score2 integer
);

insert into member( name, email, password, authorisation)
values ('Dave', 'Dave_coach@g.com', 'temp', 0);
insert into member( name, email, password, authorisation)
values ('Vanessa', 'Vannessa_coach@g.com', 'temp', 0);
insert into member( name, email, password, authorisation)
values ('Olivia', 'o@g.com', 'temp', 1);
insert into member( name, email, password, authorisation)
values ('Suzie', 's@g.com', 'temp', 1);

insert into notices(title, content, noticedate, member_id)
values('Cancelled!',
       'All netball games played outside are cancelled due to rain',
       '2023-03-04 20:30:00',
       (select member_id from member where name='Dave')
);

insert into notices(title, content, noticedate, member_id)
values('Congrats!',
       'Congratulations to our teams who all won their games',
       '2023-03-12 17:45:00',
       (select member_id from member where name='Vanessa')
);


insert into notices(title, content, noticedate, member_id)
values('Training!',
       'Training cancelled on Thursday, due to coach being sick',
       '2023-03-14 12:38:00',
       (select member_id from member where name='Vanessa')
);

insert into team( team_name)
values ('Hot Shots 2');
insert into team( team_name)
values ('Hot Shots 3');
insert into team( team_name)
values ('Hot Shots 1');
insert into team( team_name)
values ('Marsden');
insert into team( team_name)
values ('WEGC');
insert into team( team_name)
values ('East 2');
insert into team( team_name)
values ('Vic Uni 2');
insert into team( team_name)
values ('St Marys 2');
insert into team( team_name)
values ('Vic Uni 1');
insert into team( team_name)
values ('WGC');
insert into team( team_name)
values ('St Marys 1');
insert into team( team_name)
values ('East');
insert into team( team_name)
values ('Onslow');
insert into team( team_name)
values ('Scots');
insert into team( team_name)
values ('Ories');
insert into team( team_name)
values ('Newlands');

insert into game( gamedate, location, team1, team2)
values ('2023-04-08 08:00:00', 'ASB', 'Hot Shots 1', 'Marsden' );
insert into game( gamedate, location, team1, team2)
values ('2023-04-08 09:05:00', 'ASB', 'Vic Uni 1', 'Hot Shots 3' );
insert into game( gamedate, location, team1, team2)
values ('2023-04-08 11:15:00', 'ASB', 'Hot Shots 2', 'Onslow' );

insert into game( gamedate, location, team1, team2)
values ('2023-03-15 08:00:00', 'ASB', 'Hot Shots 2', 'WGC' );
insert into game( gamedate, location, team1, team2)
values ('2023-03-15 10:10:00', 'ASB', 'Vic Uni 2', 'Hot Shots 1' );
insert into game( gamedate, location, team1, team2)
values ('2023-03-15 12:25:00', 'ASB', 'Hot Shots 3', 'St Marys 1' );

insert into game( gamedate, location, team1, team2)
values ('2023-03-22 08:00:00', 'ASB', 'Hot Shots 3', 'Ories' );
insert into game( gamedate, location, team1, team2)
values ('2023-03-22 10:10:00', 'ASB', 'Scots', 'Hot Shots 1');
insert into game( gamedate, location, team1, team2)
values ('2023-03-22 12:25:00', 'ASB', 'Hot Shots 2', 'St Marys 1' );


insert into results( resultdate, team1, score1, team2, score2)
values ('2023-03-08', 'Hot Shots 3','31', 'Marsden','16' );
insert into results( resultdate, team1, score1, team2, score2)
values ('2023-03-08', 'Newlands','48', 'Hot Shots 1','52' );
insert into results( resultdate, team1, score1, team2, score2)
values ('2023-03-08', 'Hot Shots 2','12', 'St Marys 2','24' );

insert into results( resultdate, team1, score1, team2, score2)
values ('2023-03-01', 'Hot Shots 1','24', 'WEGC','24' );
insert into results( resultdate, team1, score1, team2, score2)
values ('2023-03-01', 'Scots','57', 'Hot Shots 3','58' );
insert into results( resultdate, team1, score1, team2, score2)
values ('2023-03-01', 'Hot Shots 2','12', 'Vic Uni 1','18' );

insert into results( resultdate, team1, score1, team2, score2)
values ('2023-02-22', 'Hot Shots 2','24', 'WGC','24' );
insert into results( resultdate, team1, score1, team2, score2)
values ('2023-02-22', 'Onslow','57', 'Hot Shots 2','58' );
insert into results( resultdate, team1, score1, team2, score2)
values ('2023-02-22', 'Hot Shots 1','12', 'Vic Uni 2','18' );


