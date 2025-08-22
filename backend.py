from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from building_data import SITE_FILE, URL, getData, extract_h3_content, build_final_list 

app = FastAPI(title="assignment demo")

@app.get("/getTimeStories", response_class=JSONResponse)

def get_time_stories(fetch: bool = True):
    try:
        if fetch:
            getData(URL, "site")


        h3_data = extract_h3_content(SITE_FILE)
        final_list = build_final_list(h3_data, limit=6)

        if len(final_list) < 6:
            return JSONResponse(status_code=502, content={"error": "extracted_less_than_6", "extracted": len(final_list), "stories": final_list})

        return JSONResponse(status_code=200, content=final_list)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))