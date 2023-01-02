create database real_estate;
use real_estate;
create table admin(

AdminID INT PRIMARY KEY AUTO_INCREMENT,
AdminNAME varchar(50) NOT NULL,
AdminEMAIL varchar(50) UNIQUE KEY,
AdminMobileNum varchar(10) UNIQUE KEY,
AdminAge INT NOT NULL,
Password varchar(50)
);

select * from admin;

create table broker(

BrokerID INT PRIMARY KEY AUTO_INCREMENT,
BrokerNAME varchar(50) NOT NULL,
BrokerEMAIL varchar(50) UNIQUE KEY,
BrokerMobileNum varchar(10) UNIQUE KEY,
BrokerEXP INT NOT NULL,
BrokerCOMM INT NOT NULL,
BrokerSTAT BIT

);
select * from broker;

create table property(
PropertyID INT PRIMARY KEY AUTO_INCREMENT,
PropertyNAME varchar(50) NOT NULL,
PropertyOwnerNAME varchar(50),
PropertyOwernMobileNum varchar(10) UNIQUE KEY,
PropertyADD varchar(250),
PropertyCITY varchar(50),
ProperyCODE varchar(6),
PropertyKind varchar(50),
PropertyAREA varchar(50),
PropertyVAL float,
PropertySTAT BIT,
BrokerID INT,
foreign key (BrokerID) references broker(BrokerID) on delete SET NULL
);

select * from property;
alter table broker add password varchar(50);
select * from broker;

insert into 
admin (AdminNAME,AdminEMAIL,AdminMobileNum,AdminAge,Password) values
('vasanth dumpati','mems200005014@iiti.ac.in','8555874554',20,'vasanth');

select * from admin;
alter table property drop PropertyNAME;

select * from property;

insert into 
property(PropertyOwnerNAME,PropertyOwernMobileNum,PropertyADD,PropertyCITY,ProperyCODE,PropertyKind,PropertyAREA,PropertyVAL,PropertySTAT ) values
('Anuhya','9014324624','ashok colony','siddipet','502013','kind1',250,507.90,1);

select * from property;

insert into 
property(PropertyOwnerNAME,PropertyOwernMobileNum,PropertyADD,PropertyCITY,ProperyCODE,PropertyKind,PropertyAREA,PropertyVAL,PropertySTAT ) values
('Bhavna','7993801099','walter','vizag','500020','kind1',400,1200.34,1),
('Raana','9493998765','kaachiguda','Hyderabad','503007','kind2',250,800.75,0),
('Tharun','9391758790','Jubileepura','khammam','507003','kindspecial',290,1500.00,1),
('Yaswanth','8328355730','hanuman street','ananthapur','502015','kind1',NULL,NULL,1),
('Jhansi','9391134917','benz circle','vijayawada','502007','kind1',130,200.90,1);

update property set PropertyID=PropertyID-5 where PropertyID>6;
alter table broker add password varchar(30);
select * from broker;

show create table property;
alter table property drop foreign key property_ibfk_1 ;

alter table property drop BrokerID;

create table relation(
   BrokerID INT,
   PropertyID INT,
   foreign key(BrokerID) references broker(BrokerID) on delete cascade,
   foreign key(PropertyID) references property(PropertyID) on delete cascade,
   primary key (BrokerID,PropertyID)
);

select * from relation;
insert into relation value(20,3);
delete from broker where BrokerID=20;
update broker set BrokerID=BrokerID-3 where BrokerID>1;

select * from property where PropertyID in (select propertyID from relations where BrokerID=1);
select * from property where PropertyID not in (select PropertyID from relations where BrokerID=1);
update broker set BrokerSTAT=1 where BrokerID=1;
alter table broker modify column BrokerSTAT INT;
alter table property modify column PropertySTAT INT;

truncate table relations;
drop table relations;