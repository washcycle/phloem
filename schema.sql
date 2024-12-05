CREATE TABLE peers(   
   id INTEGER     PRIMARY KEY NOT NULL,
   ip_address     TEXT     NOT NULL,
   user_id        CHAR(50) NOT NULL,
   device         CHAR(50) NOT NULL,
   public_key     CHAR(50) NOT NULL,
   create_date    TIMESTAMP NOT NULL,
   update_date    TIMESTAMP
);

