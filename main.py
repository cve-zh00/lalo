from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis

app = FastAPI()

# A      adiendo middleware para CORS
origins = [
    "*"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.post("/set_hash/")

async def set_hash(data: dict):
    key_value = data.pop("key", None)
    


    if not key_value:
        raise HTTPException(status_code=400, detail="The 'key' is required in the JSON body.")

    if not data:
        raise HTTPException(status_code=400, detail="The body should have more than just the 'key'.")

    if "productos" in key_value:
        print("entro")
        rut = key_value.replace("productos","").replace(" ","")
        redis_client.rpush(f"productos:{rut}",data["numeroPoliza"])
        #comprobamos si no existe la poliza
        if not redis_client.exists(f"poliza:{data['numeroPoliza']}"):

            redis_client.hmset(f"poliza:{data['numeroPoliza']}",data)
    else:
        redis_client.hmset(key_value, data)

    return {"message": "Data saved successfully!"}

@app.post("/get_hash/")
async def get_hash(data: dict):
    key_value = data.get("key")

    if not key_value:
        raise HTTPException(status_code=400, detail="The 'key' is required in the JSON body.")
    if "productos" in key_value:
        rut = key_value.replace("productos","").replace(" ","")
        result = redis_client.lrange(f"productos:{rut}",0,-1)
        #traemos todos los hashers de las polizas
        result_str = [x.decode('utf-8') for x in result]
        #traemos los datos de cada poliza
        result_str = [redis_client.hgetall(f"poliza:{x}") for x in result_str]
        print(result_str)


        return result_str
        
    else:
        result = redis_client.hgetall(key_value)

        if not result:
            raise HTTPException(status_code=404, detail=f"No hash found for key: {key_value}")
    
        result_str = {k.decode('utf-8'): v.decode('utf-8') for k, v in result.items()}

        return result_str

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

