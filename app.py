import google.generativeai as genai
import getpass
import os
import sqlite3

gemini_api_key = "AIzaSyDYfQmz7AHGbtvY4l5UJGVCa8JJgJrDjaQ"
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

memory=[]

prompt=input("enter the prompt")


def Generate_SQL_Query(question, memory, schema):
    print("\n\ngenerating query\n\n")
    print(question)
    print(memory)
    data="""you have to generate sql query for the given question using the given this schema: {schema} and this is the memory of the question{memory}
    give only query as answer 
    EXAMPLE: SELECT * FROM DATA

    Assistant:```sql
    """.format(schema=schema,memory=memory)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        [question,data],
        generation_config=genai.types.GenerationConfig(
            temperature=0)
    )
    return response.text


def Ask_Math_Question_To_LLM(question, memory):
    print("\n\ndoing math\n\n")
    print(question)
    print(memory)
    data="""you are a calculator you have to do claculations required for the given question and show them and this is the memory of the question {memory}""".format(schema=schema,memory=memory)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        [question,data],
        generation_config=genai.types.GenerationConfig(
            temperature=0)
    )
    return response.text


def Agent(question,memory):
    print(question)
    print(memory)
    mem=""
    for i in memory:
        mem+=str(i)+"\n\n"
    data="""<s> [INST]You are an agent capable of using a variety of TOOLS to answer a data analytics question.
    Always use MEMORY to help select the TOOLS to be used.
    you have access to all the data and data bases you have to specify the tools needed
    
    MEMORY
    """+mem+"""

    TOOLS
    - Generate Final Answer: Use if answer to User's question can be given with MEMORY
    - Calculator: Use this tool to solve mathematical problems.
    - Query_Database: Write an SQL Query to query the Database.
 
    ANSWER FORMAT
    ```json
    {
        "tool_name": "Calculator"
    }
    ```
    [/INST]
    User: """+question+"""
 
    Assistant: ```json
    {
        "tool_name": """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        data,
        generation_config=genai.types.GenerationConfig(
            temperature=0)
    )
    tool_selection=response.text
    print(tool_selection)
    if "Query_Database" in tool_selection:
        schema=""" TABLE: "SUPPLIER"
                        (
                            "SUPPLIER_ID" CHAR(6) NOT NULL PRIMARY KEY,
                            "SUPPLIER_NAME" CHAR(40),
                            "SUPPLIER_ADDRESS" CHAR(35),
                            "SUPPLIER_CONTACT" CHAR(15)
                            );
                            
                   TABLE: "PRODUCT"
                        (	"PRODUCT_ID" VARCHAR2(6) NOT NULL PRIMARY KEY,
                            "PRODUCT_NAME" VARCHAR2(40) NOT NULL,
                            "PRODUCT_DESCRIPTION" CHAR(35),
                            "PRODUCT_PRICE" FLOAT,
                            "SUPPLIER_ID" CHAR(6) NOT NULL REFERENCES SUPPLIER
                        );    
                            
                   TABLE: "INVENTORY"
                        (
                            "INVENTORY_ID" NUMBER(6,0) NOT NULL PRIMARY KEY,
                            "PRODUCT_ID" VARCHAR2(6) NOT NULL REFERENCES PRODUCT,
                            "QUANTITY" NUMBER(6,0) NOT NULL,
                            "MIN_STOCK" NUMBER(6,0) NOT NULL
                        );    
                            
                """
        query=Generate_SQL_Query(question, memory, schema)
        if "```" in query  and "sql" in query :
            query=query[6:]
            query=query[:-3]
        print("\n\n"+query+"\n\n")
        database_file_path = './sql_lite_database.db'
        conn = sqlite3.connect(database_file_path)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        memory.append({question:str(data)})
        print(question)
        print(memory)
        Agent(question, memory)
    
    if "Calculator" in tool_selection:
        memory.append({question:Ask_Math_Question_To_LLM(question, memory)})
        print(question)
        print(memory)
        Agent(question, memory)

    if "Generate Final Answer" in tool_selection:
        print("\n\ngenerating final answer\n\n")
        mem=""
        for i in memory:
            mem+=str(i)+"\n\n"
        model = genai.GenerativeModel('gemini-pro')
        Final_Output= model.generate_content(
        question+"give answer base on the memory given"+"memory :"+mem,
        generation_config=genai.types.GenerationConfig(
            temperature=0)
        )
        return Final_Output.text

print(Agent(prompt,memory))
