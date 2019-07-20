

-- -----------------------------------------------------
-- Schema CAB_RIDES
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema CAB_RIDES
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Table `CAB_RIDES`.`VEHICLE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `VEHICLE` (
  `Vehicle_Name` VARCHAR(30) NOT NULL,
  `Type` VARCHAR(15) NULL,
  `Make` VARCHAR(30) NULL,
  PRIMARY KEY (`Vehicle_Name`));


-- -----------------------------------------------------
-- Table `CAB_RIDES`.`DRIVERS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DRIVERS` (
  `DriverId` INT NOT NULL AUTO_INCREMENT,
  `First_Name` VARCHAR(45) NOT NULL,
  `Last_Name` VARCHAR(45) NOT NULL,
  `Vehicle_No` VARCHAR(15) NOT NULL,
  `Vehicle` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`DriverId`),
  CONSTRAINT `Vehicle_Name`
    FOREIGN KEY (`Vehicle`)
    REFERENCES `VEHICLE` (`Vehicle_Name`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE);

CREATE UNIQUE INDEX `DriverId_uniq` ON `CAB_RIDES`.`DRIVERS` (`DriverId` ASC) VISIBLE;

CREATE INDEX `Vehicle_name_idx` ON `CAB_RIDES`.`DRIVERS` (`Vehicle` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `CAB_RIDES`.`RIDERS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS RIDERS (RiderId INT NOT NULL AUTO_INCREMENT,First_Name VARCHAR(45) NOT NULL,Last_Name VARCHAR(45) NOT NULL,Contact VARCHAR(10) NOT NULL,PRIMARY KEY (RiderId));

CREATE UNIQUE INDEX `RiderId_uniq` ON `CAB_RIDES`.`RIDERS` (`RiderId` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `CAB_RIDES`.`RIDES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS RIDES (RideId INT NOT NULL AUTO_INCREMENT,DriverId INT NOT NULL,RiderId INT NOT NULL,DateTime_start DATETIME NOT NULL,DateTime_end DATETIME NOT NULL,Pickup_loc VARCHAR(60) NOT NULL,Drop_loc VARCHAR(60) NOT NULL,Type VARCHAR(30) NULL,Fare INT NULL,PRIMARY KEY (RideId),CONSTRAINT DriverId FOREIGN KEY (DriverId) REFERENCES DRIVERS (DriverId) ON UPDATE CASCADE,CONSTRAINT RiderId FOREIGN KEY (RiderId) REFERENCES RIDERS (RiderId) ON UPDATE CASCADE);

CREATE UNIQUE INDEX `RideId_uniq` ON `CAB_RIDES`.`RIDES` (`RideId` ASC) VISIBLE;

CREATE UNIQUE INDEX `DateTime_start_uniq` ON `CAB_RIDES`.`RIDES` (`DateTime_start` ASC) VISIBLE;

CREATE UNIQUE INDEX `DateTime_end_uniq` ON `CAB_RIDES`.`RIDES` (`DateTime_end` ASC) VISIBLE;

CREATE UNIQUE INDEX `DriverId_uniq` ON `CAB_RIDES`.`RIDES` (`DriverId` ASC) VISIBLE;

CREATE UNIQUE INDEX `RiderId_uniq` ON `CAB_RIDES`.`RIDES` (`RiderId` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `CAB_RIDES`.`CANCELLED_RIDES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS CANCELLED_RIDES (RideId INT,RiderId INT,DriverId INT,Reason VARCHAR(100),PRIMARY KEY (RideId,RiderId,DriverId),CONSTRAINT RideId1 FOREIGN KEY (RideId) REFERENCES RIDES (RideId) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT RiderId1 FOREIGN KEY (RiderId)REFERENCES RIDERS (RiderId),CONSTRAINT DriverId1 FOREIGN KEY (DriverId) REFERENCES DRIVERS (DriverId));

CREATE UNIQUE INDEX `RideId_uniq` ON `CAB_RIDES`.`CANCELLED_RIDES` (`RideId` ASC) VISIBLE;

CREATE UNIQUE INDEX `RiderId_uniq` ON `CAB_RIDES`.`CANCELLED_RIDES` (`RiderId` ASC) VISIBLE;

CREATE UNIQUE INDEX `DriverId_uniq` ON `CAB_RIDES`.`CANCELLED_RIDES` (`DriverId` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `CAB_RIDES`.`RIDERS_has_CANCELLED_RIDES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `CAB_RIDES`.`RIDERS_has_CANCELLED_RIDES` (
  `RIDERS_RiderId` VARCHAR(25) NOT NULL,
  `CANCELLED_RIDES_RideId` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`RIDERS_RiderId`, `CANCELLED_RIDES_RideId`),
  CONSTRAINT `fk_RIDERS_has_CANCELLED_RIDES_RIDERS1`
    FOREIGN KEY (`RIDERS_RiderId`)
    REFERENCES `CAB_RIDES`.`RIDERS` (`RiderId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_RIDERS_has_CANCELLED_RIDES_CANCELLED_RIDES1`
    FOREIGN KEY (`CANCELLED_RIDES_RideId`)
    REFERENCES `CAB_RIDES`.`CANCELLED_RIDES` (`RideId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_RIDERS_has_CANCELLED_RIDES_CANCELLED_RIDES1_idx` ON `CAB_RIDES`.`RIDERS_has_CANCELLED_RIDES` (`CANCELLED_RIDES_RideId` ASC) VISIBLE;

CREATE INDEX `fk_RIDERS_has_CANCELLED_RIDES_RIDERS1_idx` ON `CAB_RIDES`.`RIDERS_has_CANCELLED_RIDES` (`RIDERS_RiderId` ASC) VISIBLE;

USE `CAB_RIDES`;

DELIMITER $$
CREATE TRIGGER `RIDES_FARE` BEFORE INSERT ON `RIDES` FOR EACH ROW
BEGIN
UPDATE RIDES
SET new.Fare = (TIMESTAMPDIFF(MINUTE,new.DateTime_start,new.DateTime_end)*3);
END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET uniq_CHECKS=@OLD_uniq_CHECKS;
