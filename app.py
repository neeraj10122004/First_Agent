import google.generativeai as genai
import getpass
import os
import sqlite3

gemini_api_key = "GEMINI_API_KEY"
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

memory=[]
database_file_path = './sql_lite_database.db'
if os.path.exists(database_file_path):
    os.remove(database_file_path)
    message = "File 'sql_lite_database.db' found and deleted."
else:
    message = "File 'sql_lite_database.db' does not exist."
conn = sqlite3.connect(database_file_path)
cursor = conn.cursor()

prompt=input("enter the prompt")


def Generate_SQL_Query(question, memory, schema):
    print(question)
    print(memory)
    data="""you have to generate sql query for the given question using the given this schema: {schema} and this is the memory of the question{memory}
    give only query as answer 
    EXAMPLE: SELECT * FROM DATA
    """.format(schema=schema,memory=memory)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        [question,data],
        generation_config=genai.types.GenerationConfig(
            temperature=0)
    )
    return response.text


def Ask_Math_Question_To_LLM(question, memory):
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
        mem+=i+"\n\n"
    data="""You are an agent capable of using a variety of TOOLS to answer a data analytics question.
    Always use MEMORY to help select the TOOLS to be used.
    you have access to all the data and data bases you have to soecify the tools needed
 
    MEMORY
    {memory}
 
    TOOLS
    - Generate Final Answer: Use if answer to User's question can be given with MEMORY
    - Calculator: Use this tool to solve mathematical problems.
    - Query_Database: Write an SQL Query to query the Database.
 
    ANSWER FORMAT
    "json
    "
        "tool_name": "Calculator"
    ""

    User: {prompt}
 
    Assistant: ```json
    "
        "tool_name": """.format(memory=mem,prompt=question)
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
        cursor.execute(query)
        data = cursor.fetchall()
        memory.append(data)
        print(question)
        print(memory)
        Agent(question, memory)
    
    if "Calculator" in tool_selection:
        Ask_Math_Question_To_LLM(question, memory)
        print(question)
        print(memory)
        Agent(question, memory)

    if "Generate Final Answer" in tool_selection:
        mem=""
        for i in memory:
            mem+=i+"\n\n"
        model = genai.GenerativeModel('gemini-pro')
        Final_Output= model.generate_content(
        [question,mem],
        generation_config=genai.types.GenerationConfig(
            temperature=0)
        )
        return Final_Output.text

print(Agent(prompt,memory))
