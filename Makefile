# RUN
run:
	streamlit run app.py & uvicorn sql_app.main:app --reload