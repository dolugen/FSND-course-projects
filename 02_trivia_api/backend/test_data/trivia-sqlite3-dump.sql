PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	type VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO categories VALUES(1,'Science');
INSERT INTO categories VALUES(2,'Art');
INSERT INTO categories VALUES(3,'Geography');
INSERT INTO categories VALUES(4,'History');
INSERT INTO categories VALUES(5,'Entertainment');
INSERT INTO categories VALUES(6,'Sports');
CREATE TABLE questions (
	id INTEGER NOT NULL, 
	question VARCHAR, 
	answer VARCHAR, 
	category INTEGER, 
	difficulty INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category) REFERENCES categories (id)
);
INSERT INTO questions VALUES(1,'Whose autobiography is entitled ''I Know Why the Caged Bird Sings''?','Maya Angelou',2,4);
INSERT INTO questions VALUES(2,'What boxer''s original name is Cassius Clay?','Muhammad Ali',1,4);
INSERT INTO questions VALUES(3,'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?','Apollo 13',4,5);
INSERT INTO questions VALUES(4,'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?','Tom Cruise',4,5);
INSERT INTO questions VALUES(5,'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?','Edward Scissorhands',3,5);
INSERT INTO questions VALUES(6,'Which is the only team to play in every soccer World Cup tournament?','Brazil',3,6);
INSERT INTO questions VALUES(7,'Which country won the first ever soccer World Cup in 1930?','Uruguay',4,6);
INSERT INTO questions VALUES(8,'Who invented Peanut Butter?','George Washington Carver',2,4);
INSERT INTO questions VALUES(9,'What is the largest lake in Africa?','Lake Victoria',2,3);
INSERT INTO questions VALUES(10,'In which royal palace would you find the Hall of Mirrors?','The Palace of Versailles',3,3);
INSERT INTO questions VALUES(11,'The Taj Mahal is located in which Indian city?','Agra',2,3);
INSERT INTO questions VALUES(12,'Which Dutch graphic artist–initials M C was a creator of optical illusions?','Escher',1,2);
INSERT INTO questions VALUES(13,'La Giaconda is better known as what?','Mona Lisa',3,2);
INSERT INTO questions VALUES(14,'How many paintings did Van Gogh sell in his lifetime?','One',4,2);
INSERT INTO questions VALUES(15,'Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?','Jackson Pollock',2,2);
INSERT INTO questions VALUES(16,'What is the heaviest organ in the human body?','The Liver',4,1);
INSERT INTO questions VALUES(17,'Who discovered penicillin?','Alexander Fleming',3,1);
INSERT INTO questions VALUES(18,'Hematology is a branch of medicine involving the study of what?','Blood',4,1);
INSERT INTO questions VALUES(19,'Which dung beetle was worshipped by the ancient Egyptians?','Scarab',4,4);
COMMIT;
