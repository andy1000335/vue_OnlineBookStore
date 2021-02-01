CREATE TABLE `ADMINISTRATOR` (
	`Name`        VARCHAR(20)    NOT NULL, 
    `Sex`         CHAR(1)        CHECK (`Sex`='M' OR `Sex`='F'), 
    `Phone`       CHAR(10)       CHECK (LENGTH(`Phone`)=10), 
    `Birthday`    DATE, 
	`Email`       TEXT           NOT NULL, 
    `Account`     VARCHAR(20)    NOT NULL    CHECK (LENGTH(`Account`) BETWEEN 5 AND 20), 
    `Password`    VARCHAR(20)    NOT NULL    CHECK (LENGTH(`Password`) BETWEEN 5 AND 20), 
    PRIMARY KEY (`Account`)
);

CREATE TABLE `MANAGER` (
	`Name`        VARCHAR(20)    NOT NULL, 
    `Sex`         CHAR(1)        CHECK (`Sex`='M' OR `Sex`='F'), 
    `Phone`       CHAR(10)       CHECK (LENGTH(`Phone`)=10), 
    `Birthday`    DATE, 
	`Email`       VARCHAR(30)    NOT NULL, 
    `Account`     VARCHAR(20)    NOT NULL    CHECK (LENGTH(`Account`) BETWEEN 5 AND 20), 
    `Password`    VARCHAR(20)    NOT NULL    CHECK (LENGTH(`Password`) BETWEEN 5 AND 20), 
    PRIMARY KEY (`Account`)
);

CREATE TABLE `CUSTOMER` (
	`Name`        VARCHAR(20)    NOT NULL, 
    `Sex`         CHAR(1)        CHECK (`Sex`='M' OR `Sex`='F'), 
    `Phone`       CHAR(10)       CHECK (LENGTH(`Phone`)=10), 
    `Birthday`    DATE, 
	`Email`       VARCHAR(30)    NOT NULL, 
    `Account`     VARCHAR(20)    NOT NULL    CHECK (LENGTH(`Account`) BETWEEN 5 AND 20), 
    `Password`    VARCHAR(20)    NOT NULL    CHECK (LENGTH(`Password`) BETWEEN 5 AND 20), 
    PRIMARY KEY (`Account`)
);

CREATE TABLE `BOOK` (
	`Name`         TEXT           NOT NULL, 
    `Image`        CHAR(21), 
    `ISBN`         CHAR(17)       NOT NULL, 
    `Content`      TEXT, 
    `Publisher`    VARCHAR(20), 
    `Price`        INT            NOT NULL    CHECK (`Price`>0), 
    `Date`         DATE           NOT NULL, 
    `Storage`      INT            NOT NULL    CHECK (`Storage`>=0), 
    PRIMARY KEY (`ISBN`)
);

CREATE TABLE `AUTHOR` (
	`ISBN`      CHAR(17)       NOT NULL, 
    `Author`    VARCHAR(20)    NOT NULL, 
    PRIMARY KEY (`ISBN`, `Author`), 
    FOREIGN KEY (`ISBN`) REFERENCES `BOOK`(`ISBN`) ON DELETE CASCADE
);

CREATE TABLE `COUPON` (
	`CNumber`       CHAR(10)    NOT NULL, 
    `Start_date`    DATE        NOT NULL, 
    `End_date`      DATE, 
    `Type`          INT         NOT NULL    CHECK (`Type`=1 OR `Type`=2),    -- Type=1：打？折 Type=2：折扣？元
    `Over`          INT         NOT NULL    CHECK (`Over`>=0), 
    `Discount`      INT         NOT NULL    CHECK (`Discount`>0), 
    `Storage`       INT         NOT NULL    CHECK (`Storage`>=0), 
    PRIMARY KEY (`CNumber`)
);

CREATE TABLE `ORDER` (
	`ONumber`      CHAR(10)       NOT NULL, 
    `Date`         DATE           NOT NULL, 
    `Address`      TEXT           NOT NULL, 
    `Status`       INT            NOT NULL    CHECK (`Status`>0 AND `Status`<4),    -- Status=1：訂單未處理 Status=2：訂單處理中 Status=3：訂單已完成
    `CNumber`      CHAR(10), 
    `OwnerAcc`     VARCHAR(20)    NOT NULL, 
    `UpdateAcc`    VARCHAR(20), 
    PRIMARY KEY (`ONumber`), 
    FOREIGN KEY (`CNumber`)   REFERENCES `COUPON`(`CNumber`), 
    FOREIGN KEY (`OwnerAcc`)  REFERENCES `CUSTOMER`(`Account`), 
    FOREIGN KEY (`UpdateAcc`) REFERENCES `MANAGER`(`Account`)
);

CREATE TABLE `SHOPPING_CART` (
	`Account`     VARCHAR(20)    NOT NULL, 
    `ISBN`        CHAR(17)    NOT NULL, 
    `Quantity`    INT         NOT NULL    CHECK (`Quantity`>0), 
    PRIMARY KEY (`Account`, `ISBN`), 
    FOREIGN KEY (`Account`) REFERENCES `CUSTOMER`(`Account`), 
    FOREIGN KEY (`ISBN`)    REFERENCES `BOOK`(`ISBN`)
);

CREATE TABLE `SCORE` (
	`Account`    VARCHAR(20)    NOT NULL, 
    `ISBN`       CHAR(17)    NOT NULL, 
    `Star`       FLOAT       NOT NULL    CHECK (`Star`>=0), 
    PRIMARY KEY (`Account`, `ISBN`), 
    FOREIGN KEY (`Account`) REFERENCES `CUSTOMER`(`Account`), 
    FOREIGN KEY (`ISBN`)    REFERENCES `BOOK`(`ISBN`)
);

CREATE TABLE `HAVE_PRODUCT` (
	`ONumber`     CHAR(10)    NOT NULL, 
    `ISBN`        CHAR(17)    NOT NULL, 
    `Quantity`    INT         NOT NULL    CHECK (`Quantity`>0), 
    PRIMARY KEY (`ONumber`, `ISBN`), 
    FOREIGN KEY (`ONumber`) REFERENCES `ORDER`(`ONumber`) ON DELETE CASCADE, 
    FOREIGN KEY (`ISBN`)    REFERENCES `BOOK`(`ISBN`)
);

CREATE TABLE `OWN` (
	`CNumber`     CHAR(10)       NOT NULL, 
    `OwnerAcc`    VARCHAR(20)    NOT NULL, 
    `Quantity`    INT            NOT NULL    CHECK (`Quantity`>0), 
    PRIMARY KEY (`CNumber`, `OwnerAcc`), 
    FOREIGN KEY (`CNumber`) REFERENCES `COUPON`(`CNumber`), 
    FOREIGN KEY (`OwnerAcc`) REFERENCES `CUSTOMER`(`Account`)
);