cd ../
python -m venv env-pymongo-fastapi-crud
call env-pymongo-fastapi-crud/Scripts/activate.bat

cd pymongo-fastapi-crud
python -m uvicorn main:app --reload