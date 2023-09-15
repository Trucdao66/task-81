import pandas as pd
import io,json
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
import os
import numpy as np
from scipy.stats import norm

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "hello"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1]
    if ext != ".txt":
        raise HTTPException(status_code=400, detail="Only txt files are allowed")
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents), sep='\t')
    results = []
    for column in df.columns:
        result = {"x": df[column].tolist()}
        results.append(result)
    results=json.dumps(results)
    return results

@app.post("/uploadfile1/")
async def upload_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1]
    if ext != ".txt":
        raise HTTPException(status_code=400, detail="Only txt files are allowed")
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents), sep='\t')
    results = []
    for column in df.columns:
        df[column] = df[column].astype(float)
        density = norm.pdf(df[column].values, np.mean(df[column].values), np.std(df[column].values))
        result = {"x": df[column].tolist(), "f(x)": density.tolist()}
        results.append(result)    
    results=json.dumps(results)
    return results

@app.post("/uploadfile2/")
async def upload_file(file: UploadFile,cantren:int,canduoi:int):
    ext = os.path.splitext(file.filename)[1]
    if ext != ".txt":
        raise HTTPException(status_code=400, detail="Only txt files are allowed")
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents), sep='\t')
    results = []
    for column in df.columns:
        so = df[column].iloc[cantren-1:canduoi].astype(float)
        density = norm.pdf(so.values, np.mean(so.values), np.std(so.values))
        result = {"x": so.tolist(), "f(x)": density.tolist()}
        results.append(result)    
    results=json.dumps(results)
    return results


@app.post('/uploadMuptiFiles/')
async def upload_mupti_file(files: list[UploadFile],cantren:int,canduoi:int):
    if len(files)>10:
        raise HTTPException(status_code=400, detail="max 10 files")
    all=[]
    deatails=[]
    for file in files:
        ext = os.path.splitext(file.filename)[1]
        if ext != ".txt":
            raise HTTPException(status_code=400, detail="Only txt files are allowed")
        
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), sep='\t')
        deatail={"tenfile":file.filename,"function fill":"gauss"}
        file=[]
        for column in df.columns:
            so = df[column].iloc[cantren-1:canduoi].astype(float)
            density = norm.pdf(so.values, np.mean(so.values), np.std(so.values))
            infor = {"mean":np.mean(so.values),"sigma" : np.std(so.values),"area" : sum(density)}
            columnname = so.name
            deatail [columnname] = infor
            result = {"x": so.tolist(), "f(x)": density.tolist()}
            file.append(result)    
        all.append(file)
        deatails.append(deatail)
    all = json.dumps(all)
    deatails = json.dumps(deatails)
    return deatails,all