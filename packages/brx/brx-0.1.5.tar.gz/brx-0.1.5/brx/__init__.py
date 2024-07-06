import websocket
from random import randint
import json
import time
import asyncio
import requests

def apply_dict_to_if(input_dict, input_fields):
    """
    Applies a given dictionary to input_fields so that you can directly send a dictionary to BRX
    """
    for index, field in enumerate(input_fields):
        for dict_key in input_dict.keys():
            if field["name"] == dict_key:
                input_fields[index]["value"] = input_dict[dict_key]
    return input_fields

def sftoq(schema):
    if type(schema) == str:
        schema = json.loads(schema)

    # print(json.dumps(schema, indent=4))

    query = {
        "userSchemaInteract": {
            "mainBrxId": schema["schemas"]["mainBrxId"],
            "schemas": {}
        }
    }

    input_fields = []

    for sub_schema in schema["schemas"]["schemas"]["data"]:
        schema_key = sub_schema[0]
        schema_value = sub_schema[1]
        schema_fields = {}

        for input_data in schema_value["schemaFields"]["data"]: # converting the list of [key, value] to {key: value} within schema_fields
            input_key = input_data[0]
            input_value = input_data[1]
            schema_fields[input_key] = input_value
            schema_fields[input_key]["fieldValue"] = ""

            input_fields.append({
                "type": schema_fields[input_key]["fieldValueDataType"],
                "name": input_key,
                "entry_key": schema_key,
                "value": ""
            })

        query["userSchemaInteract"]["schemas"][schema_key] = {
            "brxId": schema_value["brxId"],
            "brxName": schema_value["brxName"],
            "schemaFields": schema_fields
        }

    return {"brx_query": query, "input_fields": input_fields}

def uif(input_fields, brx_query):
    for input_field in input_fields:
        schema = brx_query["userSchemaInteract"]["schemas"][input_field["entry_key"]]
        schema["schemaFields"][input_field["name"]]["fieldValue"] = input_field["value"]
        brx_query["userSchemaInteract"]["schemas"][input_field["entry_key"]] = schema
    return {"brx_query": brx_query}
    
def query_to_json(query):
    reformatted = {
        "userSchemaInteract": {
            "mainBrxId": query["userSchemaInteract"]["mainBrxId"],
            "schemas": {
                "_isMap": True,
                "data": []
            }
        }
    }

    for schema_key in query["userSchemaInteract"]["schemas"]: # iterating through each {key: value} and converting it back to [key, value]
        schema_value = query["userSchemaInteract"]["schemas"][schema_key]
        reformatted_schema = {
            "brxId": schema_value["brxId"],
            "brxName": schema_value["brxName"],
            "schemaFields": {"_isMap": True, "data": []}
        }

        for field_key in schema_value["schemaFields"]:
            field_value = schema_value["schemaFields"][field_key]
            reformatted_schema["schemaFields"]["data"].append(
                [field_key, field_value]
            )

        reformatted["userSchemaInteract"]["schemas"]["data"].append([schema_key, reformatted_schema])

    return json.dumps(reformatted)


class BRX:
    def __init__(self, access_token, verbose=True, send_local=False):
        self.verbose = verbose
        self.access_token = access_token
        self.base_url = 'http://localhost:8080/' if send_local else 'https://api.brx.ai/'

    def call_brk(self, schema, data):
        query_rebuild = brx.sftoq(schema)
        output_object = query_rebuild["brx_query"]
        input_fields = query_rebuild["input_fields"]
        input_fields = apply_dict_to_if(data, input_fields)
        updated_query = brx.uif(input_fields, output_object)
        result = self.execute(updated_query["brx_query"])
        result = json.loads(result[0])
        try:
            result = result["brxRes"]["output"]
            return {"brxError": False, "output": result}
        except Exception as e:
            print(e)
            print("Result: ", result)
            return {"brxError": True}


    def run_sfid_with_dict(self, schema_id, dct, use_schema_id=True):
        schema = ""
        if use_schema_id:
            schema = self.sfid(schema_id)
        else:
            schema = schema_id
        query_rebuild = sftoq(schema)
        output_object = query_rebuild["brx_query"]
        input_fields = query_rebuild["input_fields"]
        input_fields = apply_dict_to_if(dct, input_fields)
        updated_query = uif(input_fields, output_object)
        result = self.execute(updated_query["brx_query"])
        return result

    def get(self, schema_name):
        return BRK(self, self.sfid(schema_name))

    def sfid(self, schema_name):
        try:
            r = requests.post(f"{self.base_url}schema_from_id", headers={
                "key": self.access_token,
                "Content-Type": "application/json"
            }, json={
                "brxId": schema_name
            })
            json_schema = r.json()["httpResponse"]
            # print()
            print("Obtained response: ", json.dumps(json_schema["brkObject"], indent=4))
            json_schema = json_schema["brkObject"]
            return json_schema
        except Exception as err:
            print("Error: ", err)
            print("There was an error finding your id!")
            return
        pass

    def call_brk_messages(self, messages):
        query_rebuild = brx.sftoq(messages[0]["content"])
        output_object = query_rebuild["brx_query"]
        input_fields = query_rebuild["input_fields"]
        input_fields = apply_dict_to_if(messages[1]["content"], input_fields)
        updated_query = brx.uif(input_fields, output_object)
        result = self.execute(updated_query["brx_query"])
        result = json.loads(result[0])
        result = result["brxRes"]["output"]
        return {"role": "assistant", "content": json.dumps(result)}

    async def a_execute(self, query):
        if(self.verbose):
            print("Starting async execute")
            print("Using access token: ", self.access_token)

        ws = websocket.WebSocket()
        ws.connect("wss://api.brx.ai/query_stream", header={"key": self.access_token})

        if(self.verbose):
            print("===Socket Debug===")
            print("-=-=-=-=-=-=-=-")
            print("Websocket initialized")
        
        await asyncio.sleep(1)
        
        brx = []
        response_length = len(query["userSchemaInteract"]["schemas"])
        
        if(self.verbose):
            print("Response length set to: ", response_length)

        ws.send(query_to_json(query))

        while len(brx) < response_length: 
            message = await asyncio.get_event_loop().run_in_executor(None, ws.recv)
            brx.append(message)
            if self.verbose:
                print("Received message: ", message)

        ws.close()
        
        return brx

    def execute(self, query):
        if(self.verbose):
            print("Starting execute")
            print("Using access token: ", self.access_token)

        ws = websocket.WebSocket()
        ws.connect("wss://api.brx.ai/query_stream", header={"key": self.access_token})

        if(self.verbose):
            print("===Socket Debug===")
            print("-=-=-=-=-=-=-=-")
            print("Websocket initialized")
        
        time.sleep(1)
        
        brx = []
        response_length = len(query["userSchemaInteract"]["schemas"])
        
        if(self.verbose):
            print("Response length set to: ", response_length)

        ws.send(query_to_json(query))

        while len(brx) < response_length: 
            message = ws.recv()
            brx.append(message)
            if self.verbose:
                print("Received message: ", message)

        ws.close()
        
        return brx
    
    def modify():
        print("Modify function not implemented it")
        pass

class BRK:
    def __init__(self, brx: BRX, schema: any, verbose=True, send_local=False):
        self.verbose = verbose
        self.brx = brx
        self.schema = schema
        self.input = {}
        input_fields = sftoq(schema)["input_fields"]
        for index, field in enumerate(input_fields):
            self.input[field["name"]] = ""

    def run(self):
        return self.brx.run_sfid_with_dict(self.schema, self.input, use_schema_id=False)

    def __str__(self):
        return json.dumps(self.schema, indent=4) + "\n With inputs: " + json.dumps(self.input, indent=4)