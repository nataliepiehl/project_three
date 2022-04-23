CREATE TABLE ratingsmix (id integer primary key, title text not null, year numeric, 
                         movie_id integer not null, rating real not null, votes integer not null);

insert into ratingsmix select movies.*, ratings.* from movies inner join ratings on movies.id=ratings.movie_id;

CREATE TABLE directorsmix (id integer primary key, name text , birth numeric, movie_id int not null, 
                           person_id int not null, foreign key(movie_id) references movies(id), foreign key(person_id)
                           references people(id));

insert into directorsmix select people.*, directors.* from people inner join directors on people.id=directors.person_id;

CREATE TABLE starsmix (id integer primary key, name text , birth numeric, movie_id int not null, 
                           person_id int not null, foreign key(movie_id) references movies(id), foreign key(person_id)
                           references people(id));

insert into starsmix select people.*, stars.* from people inner join stars on people.id=stars.person_id;  


select * from ratingsmix limit(5);
select * from directorsmix limit(5);
select * from starsmix limit(5);    
