/*
Chris Collier, Vincent Crabtree, Daniel Kobold
ECE 59500 Database Management Systems 
Final Project
*/

CREATE TABLE movie(
	mid integer NOT NULL PRIMARY KEY,
	mname varchar(40) NOT NULL,
	mdir varchar(20),
	myr integer,
	mgen varchar(15)
);

ALTER TABLE movie
ADD imlink varchar(500);

CREATE TABLE usr(
	usid integer NOT NULL PRIMARY KEY,
	usname varchar(20) NOT NULL
);

ALTER TABLE usr
ADD uspass varchar(20);

CREATE TABLE critic(
	cid integer NOT NULL PRIMARY KEY,
	cname varchar(20) NOT NULL,
	cemp varchar(15)
);

ALTER TABLE critic
ADD cpass varchar(20);

CREATE TABLE review(
	r_mid integer REFERENCES movie(mid),
	r_uid integer REFERENCES usr(usid),
	r_score integer NOT NULL,
	r_notes varchar(1000)
);

CREATE TABLE critic_review(
	c_mid integer REFERENCES movie(mid),
	c_cid integer REFERENCES critic(cid),
	c_score integer NOT NULL,
	c_notes varchar(1000)
);

INSERT INTO movie
	(mid, mname, mdir, myr, mgen)
values
	(1, 'Snow White and the Seven Dwarfs', 'David Hand', 1937, 'Fantasy'),
	(2, 'Pinocchio', 'Ben Sharpsteen', 1940, 'Fantasy'),
	(3, 'Fantasia', 'Samuel Armstrong', 1940, 'Anthology'),
	(4, 'Dumbo', 'Ben Sharpsteen', 1941, 'Fantasy'),
	(5, 'Bambi', 'David Hand', 1942, 'Fantasy');

INSERT INTO movie
	(mid, mname, mdir, myr, mgen)
values
	(6, 'Cinderella', 'Clyde Geronimi', 1950, 'Fantasy'),
	(7, 'Alice in Wonderland', 'Clyde Geronimi', 1951, 'Fantasy'),
	(8, 'Peter Pan', 'Clyde Geronimi', 1953, 'Fantasy'),
	(9, 'Lady and the Tramp', 'Clyde Geronimi', 1955, 'Adventure'),
	(10, 'Sleeping Beauty', 'Clyde Geronimi', 1959, 'Fantasy');

INSERT INTO movie
	(mid, mname, mdir, myr, mgen)
values
	(11, 'One Hundred and One Dalmatians', 'Wolfgang Reitherman', 1961, 'Adventure'),
	(12, 'The Sword in the Stone', 'Wolfgang Reitherman', 1963, 'Fantasy'),
	(13, 'The Jungle Book', 'Wolfgang Reitherman', 1967, 'Fantasy'),
	(14, 'The Aristocats', 'Wolfgang Reitherman', 1970, 'Comedy'),
	(15, 'Robin Hood', 'Wolfgang Reitherman', 1973, 'Comedy'),
	(16, 'The Many Adventures of Winnie the Pooh', 'John Lounsbery', 1977, 'Anthology'),
	(17, 'The Rescuers', 'Wolfgang Reitherman', 1977, 'Adventure'),
	(18, 'Petes Dragon', 'Don Chaffey', 1977, 'Fantasy'),
	(19, 'The Fox and the Hound', 'Ted Berman', 1981, 'Drama'),
	(20, 'Tron', 'Steven Lisberger', 1982, 'Sci-Fi');

INSERT INTO usr
	(usid, usname)
values
	(1, 'Chris Collier'),
	(2, 'Vincent Crabtree'),
	(3, 'Daniel Kobold');

UPDATE usr
SET uspass = 'ccollier'
WHERE usid = 1;

UPDATE usr
SET uspass = 'vcrabtree'
WHERE usid = 2;

UPDATE usr
SET uspass = 'dkobold'
WHERE usid = 3;

INSERT INTO review	
	(r_mid, r_uid, r_score)
values
	(5, 3, 2);

INSERT INTO critic
	(cid,cname,cpass)
values
	(1,'Paul Strict','pstrict');

	/*
UPDATE movie
SET imlink = 'https://is4-ssl.mzstatic.com/image/thumb/Video69/v4/37/a3/61/37a361bf-99d4-0283-65d6-39bb0b66fce0/Snow-White-And-The-Seven-Dwarfs_Walt_sig_Keystone_2000x3000.jpg/268x0w.jpg'
WHERE mid = 1;*/
