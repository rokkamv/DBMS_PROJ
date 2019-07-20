import mysql.connector

con = mysql.connector.connect(user='root', password='vaibhav99', host='localhost', database='cabrides')
c = con.cursor()
def create_table():

    c.execute('CREATE TABLE IF NOT EXISTS VEHICLE (Vehicle_Name VARCHAR(30) NOT NULL,Type VARCHAR(15) NULL,Make VARCHAR(30) NULL,PRIMARY KEY (Vehicle_Name))')
    c.execute('CREATE TABLE IF NOT EXISTS DRIVERS (DriverId INT NOT NULL AUTO_INCREMENT,First_Name VARCHAR(45) NOT NULL,Last_Name VARCHAR(45) NOT NULL,Vehicle_No VARCHAR(15) NOT NULL,Vehicle VARCHAR(30) NOT NULL,PRIMARY KEY (DriverId),CONSTRAINT Vehicle_Name FOREIGN KEY (Vehicle) REFERENCES VEHICLE(Vehicle_Name) ON UPDATE CASCADE)')
    #c.execute('CREATE TABLE IF NOT EXISTS DRIVERS (DriverId INT NOT NULL AUTO_INCREMENT,First_Name VARCHAR(45) NOT NULL,Last_Name VARCHAR(45) NOT NULL,Vehicle_No VARCHAR(15) NOT NULL,Vehicle VARCHAR(30) NOT NULL,PRIMARY KEY (DriverId),CONSTRAINT Vehicle_Name FOREIGN KEY (Vehicle) REFERENCES VEHICLE (Vehicle_Name) ON UPDATE CASCADE)')
    c.execute('CREATE TABLE IF NOT EXISTS RIDERS (RiderId INT NOT NULL AUTO_INCREMENT,First_Name VARCHAR(45) NOT NULL,Last_Name VARCHAR(45) NOT NULL,Contact VARCHAR(10) NOT NULL,PRIMARY KEY (RiderId))')
    c.execute('CREATE TABLE IF NOT EXISTS RIDES (RideId INT NOT NULL AUTO_INCREMENT,DriverId INT NOT NULL,RiderId INT NOT NULL,DateTime_start DATETIME NOT NULL,DateTime_end DATETIME NOT NULL,Pickup_loc VARCHAR(60) NOT NULL,Drop_loc VARCHAR(60) NOT NULL,Type VARCHAR(30) NULL,Fare INT NULL,PRIMARY KEY (RideId),CONSTRAINT DriverId FOREIGN KEY (DriverId) REFERENCES DRIVERS (DriverId) ON UPDATE CASCADE,CONSTRAINT RiderId FOREIGN KEY (RiderId) REFERENCES RIDERS (RiderId) ON UPDATE CASCADE)')
    c.execute('CREATE TABLE IF NOT EXISTS CANCELLED_RIDES (RideId INT,RiderId INT,DriverId INT,Reason VARCHAR(100),PRIMARY KEY (RideId,RiderId,DriverId),CONSTRAINT RideId1 FOREIGN KEY (RideId) REFERENCES RIDES (RideId) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT RiderId1 FOREIGN KEY (RiderId) REFERENCES RIDERS (RiderId),CONSTRAINT DriverId1 FOREIGN KEY (DriverId) REFERENCES DRIVERS (DriverId))')
    #c.execute('create trigger calculate_sp before insert on stock for each row begin set new.sell_price = new.cost_price*1.18*1.2 ; end')
    #c.execute('create  procedure `add_supplies`(in s_id varchar(20), in cycle_name varchar(50)) begin insert into supplies(s_id,cycle_name) values(s_id, cycle_name); end')
    c.execute('CREATE TRIGGER RIDES_FARE BEFORE INSERT ON RIDES FOR EACH ROW BEGIN SET new.Fare = TIMESTAMPDIFF(MINUTE,new.DateTime_start,new.DateTime_end)*3; END')
create_table()
