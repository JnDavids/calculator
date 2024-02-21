CREATE TABLE IF NOT EXISTS calculations_tb (
    id INT NOT NULL AUTO_INCREMENT,
    operation VARCHAR(20) NOT NULL,
    value_1 INT NOT NULL,
    value_2 INT NOT NULL,
    result FLOAT NOT NULL,
    date DATETIME NOT NULL,
    PRIMARY KEY (id)
);