FROM python:3.9
WORKDIR /Maths_problem
COPY . /Maths_problem
EXPOSE 8501 8000
RUN pip install -r requirements.txt
CMD ["bash", "-c", "uvicorn src.ui.fastapi:app --host 0.0.0.0 --port 8000 & streamlit run src/ui/app.py --server.port 8501"]