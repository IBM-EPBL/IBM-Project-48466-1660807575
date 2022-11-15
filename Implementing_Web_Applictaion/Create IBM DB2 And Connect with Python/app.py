import ibm_db

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prm92612;PWD=aW3A18gUT3mCMGBh;", "", "")
    print("connected to DB")
except:
    print("connection failed")







