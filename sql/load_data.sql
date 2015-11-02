

INSERT INTO User (username, firstname, lastname, email, password)
VALUES ('sportslover','Paul','Walker','sportslover@hotmail.com', "5a18fcdb49a9ff416b67");

INSERT INTO User (username, firstname, lastname, email, password)
VALUES ('traveler','Rebecca','Travolta','rebt@explorer.org', "36de6c6506c1f726a510");

INSERT INTO User (username, firstname, lastname, email, password)
VALUES ('spacejunkie','Bob','Spacey','bspace@spacejunkies.net', "bd26da9a132f4aa3165a");



INSERT INTO Album (title, username, access) 
VALUES ('I love sports','sportslover', "public"),
       ('I love football','sportslover', "public"),
       ('Around The World','traveler', "public"),
       ('Cool Space Shots','spacejunkie', "private");


INSERT INTO Photo (picid, format, url) 
VALUES ('football_s1','jpg', 'pictures/football_s1.jpg'),
       ('football_s2','jpg', 'pictures/football_s2.jpg'),
       ('football_s3','jpg', 'pictures/football_s3.jpg'),
       ('football_s4','jpg', 'pictures/football_s4.jpg'),
       ('space_EagleNebula','jpg', 'pictures/space_EagleNebula.jpg'),
       ('space_GalaxyCollision','jpg', 'pictures/space_GalaxyCollision.jpg'),
       ('space_HelixNebula','jpg', 'pictures/space_HelixNebula.jpg'),
       ('space_MilkyWay','jpg', 'pictures/space_MilkyWay.jpg'),
       ('space_OrionNebula','jpg', 'pictures/space_OrionNebula.jpg'),
       ('sports_s1','jpg', 'pictures/sports_s1.jpg'),
       ('sports_s2','jpg', 'pictures/sports_s2.jpg'),
       ('sports_s3','jpg', 'pictures/sports_s3.jpg'),
       ('sports_s4','jpg', 'pictures/sports_s4.jpg'),
       ('sports_s5','jpg', 'pictures/sports_s5.jpg'),
       ('sports_s6','jpg', 'pictures/sports_s6.jpg'),
       ('sports_s7','jpg', 'pictures/sports_s7.jpg'),
       ('sports_s8','jpg', 'pictures/sports_s8.jpg'),
       ('world_EiffelTower','jpg', 'pictures/world_EiffelTower.jpg'),
       ('world_firenze','jpg', 'pictures/world_firenze.jpg'),
       ('world_GreatWall','jpg', 'pictures/world_GreatWall.jpg'),
       ('world_Isfahan','jpg', 'pictures/world_Isfahan.jpg'),
       ('world_Istanbul','jpg', 'pictures/world_Istanbul.jpg'),
       ('world_Persepolis','jpg', 'pictures/world_Persepolis.jpg'),
       ('world_Reykjavik','jpg', 'pictures/world_Reykjavik.jpg'),
       ('world_Seoul','jpg', 'pictures/world_Seoul.jpg'),
       ('world_Stonehenge','jpg', 'pictures/world_Stonehenge.jpg'),
       ('world_TajMahal','jpg', 'pictures/world_TajMahal.jpg'),
       ('world_TelAviv','jpg', 'pictures/world_TelAviv.jpg'),
       ('world_tokyo','jpg', 'pictures/world_tokyo.jpg'),
       ('world_WashingtonDC','jpg', 'pictures/world_WashingtonDC.jpg');


INSERT INTO Contain (picid, albumid) 
VALUES ('football_s1',2),
       ('football_s2',2),
       ('football_s3',2),
       ('football_s4',2),
       ('space_EagleNebula',4),
       ('space_GalaxyCollision',4),
       ('space_HelixNebula',4),
       ('space_MilkyWay',4),
       ('space_OrionNebula',4),
       ('sports_s1',1),
       ('sports_s2',1),
       ('sports_s3',1),
       ('sports_s4',1),
       ('sports_s5',1),
       ('sports_s6',1),
       ('sports_s7',1),
       ('sports_s8',1),
       ('world_EiffelTower',3),
       ('world_firenze',3),
       ('world_GreatWall',3),
       ('world_Isfahan',3),
       ('world_Istanbul',3),
       ('world_Persepolis',3),
       ('world_Reykjavik',3),
       ('world_Seoul',3),
       ('world_Stonehenge',3),
       ('world_TajMahal',3),
       ('world_TelAviv',3),
       ('world_tokyo',3),
       ('world_WashingtonDC',3);

INSERT INTO AlbumAccess (albumid, username) 
VALUES (4,'traveler');
