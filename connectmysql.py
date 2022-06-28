import mysql.connector
import hashlib as hasher



class connectMysql():
    
    def __init__(self,user = "root",password ="",host = "localhost",database = ""):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
        # CREATING CONNECTION
        self.cnx = mysql.connector.connect(user = self.user,password = self.password,database = self.database)

    def __str__(self):
        return "This Modul provides to connect Mysql from python projects easier"
    
    #DEFINE FOUR BASIC FUNCTIONS(SELECT,INSERT,UPDATE,DELETE)
    def selectValue(self,allDistinct = "NONE",columns = ["*"],table = "",
                    joinTables = [],joinType = ["INNER" or "LEFT","RIGHT"],joinColumns = [],joinValues = [],
                    whereColumns = [],whereSigns = [],whereValues = [],
                    groupBy = [],havingColumns = [],havingSigns = [],havingValues = [],
                    orderBy = [],ascDesc = ["ASC","DESC"]):
        query = "SELECT "
        if allDistinct != "NONE":
            query += allDistinct
        i = 0
        while (i<=len(columns)-1):
            query += columns[i]
            if i !=len(columns)-1:
                query += ","
            i+=1
        query +=" FROM "+table 

        if len(joinColumns)>0 and len(joinColumns) == len(joinValues):
            i=0
            while(i<=len(joinTables)-1):
                query += " "+joinType[0]+" JOIN "+joinTables[i]+" on "+joinColumns[i] +" = "+str(joinValues[i])
                i+=1
        if len(whereColumns)>0 and len(whereColumns)==len(whereValues):
            query+= " WHERE "
            i=0
            while (i <= len(whereColumns)-1):
                if len(whereSigns) != 0 :
                    query += whereColumns[i] + whereSigns[i]+"'"+str(whereValues[i])+"'"
                else:
                    query += whereColumns[i] +" = '"+str(whereValues[i])+"'"
                if(i != len(whereColumns)-1):
                    query+= " AND " 
                i+=1
        if (len(groupBy)>0):
            query+= " GROUP BY "
            i=0
            while (i<=len(groupBy)-1):
                query+=groupBy[i]
                if (i != len(groupBy)-1):
                    query+=","
                i+=1
        if len(havingColumns)>0 and len(havingColumns)==len(havingValues) and len(groupBy)>0:
            query+=" HAVING "
            i=0
            while(i<=len(havingColumns)-1):
                if len(havingSigns) != 0 :
                    query+= havingColumns[i]+havingSigns[i]+str(havingValues[i])
                else:
                    query+= havingColumns[i]+" = "+str(havingValues[i])
                if i !=len(havingColumns)-1:
                    query += " AND "
                i+=1
        if len(orderBy)>0 and len(orderBy) == len(ascDesc):
            query+= " ORDER BY "
            i=0
            while (i <= len(orderBy)-1):
                query+= orderBy[i]+" "+ascDesc[i]
                if (i !=len(orderBy)-1):
                    query+=","
                i+=1
        
        try:
            cursor = self.cnx.cursor()
            cursor.execute(query)
            results = []
            
            for result in cursor:
                results.append(result)
            self.cnx.commit()
            cursor.close()
            self.cnx.close()
            
            return(results)
        
        except BaseException:
            raise("error creating cursor")   
                 
    def insertValue(self,columns = [],values = [],table = ""):
        if ((len(columns) == len(values)) and (len(columns)>0)):
            i=0
            Columns=""
            Values=""
            while (i<=len(columns)-1):
                Columns +=  " "+columns[i]
                Values += " '"+str(values[i])+"'"
                if i != len(columns)-1:
                    Columns= Columns +", "
                    Values = Values +", "
                i+=1
            
            query = "INSERT INTO "+ table +"( "+Columns+") VALUES ("+Values+" )"
            return self.executeQuery(query)
        else:
            raise ("len column not equal to len values or len column have to bigger than zero")
        


    def updateValue(self,changeColumnsName = [],changeValuesName = [],columns = [],values = [],table = ""):
        if(len(changeColumnsName) == len(changeValuesName) and len(changeColumnsName) > 0
           and len(columns) == len(values) and len(columns) > 0):
            query = "UPDATE "+table+" SET "
            i = 0
            while (i<=len(changeColumnsName)-1):
                query += "`"+changeColumnsName[i]+"` = '"+str(changeValuesName[i])+"'"
                
                if i != len(changeColumnsName)-1:
                    query +=" , "
                i+=1
            query += " WHERE "
            j = 0
            while (j <= len(columns)-1):
                query+= "`"+columns[j] + "` = '"+ str(values[j])+"'"
                
                if j != len(columns)-1:
                    query += " and "
                j+=1

            return self.executeQuery(query)
        else:
            return False   

         
    def deleteValue(self,params = [],values = [],table = ""):
        
        query = "DELETE FROM "+table
        
        if len(params) > 1 and len(params) == len(values):
            i=0
            query = query + "  where "
            while i<=len(params)-1:
                a = params[i] + " = '"+ str(values[i]) +"' "
                query +=a
                if i !=len(params)-1:
                    query +=" and "
                i+=1
        elif len(params) == 1 :
            query = query +" WHERE "+ params[0]+ " = '"+str(values[0])+"'"    

        return self.executeQuery(query)
    
    # THIS FUNCTION CREATED TO USE IN ANOTHER BASIC FUNCTIONS 
    # AND WHEN WE WANT TO RUN QUERY WITHOUT PARAMETERS
    def executeQuery(self,query):
        try:
            cursor = self.cnx.cursor()
            cursor.execute(query)
            self.cnx.commit()
            cursor.close()
            self.cnx.close()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True


class Functions():
    
    def __init__(self):
        pass

    def __str__(self):
        return "This Modul provides simple functions to shorten your code lines"
        
    def changeName(self,file,name,number = 1):
        return str(name)+"."+file.split(".")[number]


    def searchForbiddenCharacters(self,args,forbiddenCharacters = [";","-",".","'"]):
        i = 0
        while(i<=len(args)-1):
            if(args[i] in forbiddenCharacters):
                return True
            else:
                i+=1
        return False

    def passwordEncrypt(self,password,characters = "utf-8"):
        encryption = hasher.sha256()
        encryption.update(password.encode(characters))
        hash = encryption.hexdigest()

        return hash



