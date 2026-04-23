import pytest
from library import DataLoader, DataLoadError
import os
import tempfile

def test_load_students():
    loader = DataLoader()
    # Crear un archivo CSV temporal para la prueba
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,name,email,phone,birthdate,faculty,year_level\n")
        f.write("1,Nate Bustamante,nate@example.com,1234567890,2000-01-01,Engineering,3\n")
        f.write("2,Alice Smith,alice@example.com,0987654321,1999-05-15,Science,2\n")
        temp_file = f.name

    members = loader.load_students(temp_file)
    assert len(members) == 2
    os.unlink(temp_file)

def test_load_books():
    loader = DataLoader()
    # Crear un archivo CSV temporal para la prueba
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,title,author,faculty,year,copies\n")
        f.write("1,Python Basics,Guido van Rossum,Engineering,2020,5\n")
        f.write("2,Clean Code,Robert C. Martin,Science,2008,3\n")
        temp_file = f.name

    items = loader.load_books(temp_file)
    assert len(items) == 2
    os.unlink(temp_file)

def test_load_history():
    loader = DataLoader()
    # Crear un archivo CSV temporal para la prueba
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,member_id,item_id,borrow_date,due_date,return_date\n")
        f.write("1,1,1,2023-01-01,2023-01-15,\n")
        f.write("2,2,2,2023-02-01,2023-02-15,2023-02-10\n")
        temp_file = f.name

    transactions = loader.load_history(temp_file)
    assert len(transactions) == 2
    os.unlink(temp_file)

def test_missing_file():
    loader = DataLoader()
    with pytest.raises(DataLoadError):
        loader.load_students("nonexistent_file.csv")

def test_missing_column():
    loader = DataLoader()
    # Crear un archivo CSV temporal sin una columna
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,name,email,phone,birthdate\n")  # Falta faculty y year_level
        f.write("1,Nate Bustamante,nate@example.com,1234567890,2000-01-01\n")
        temp_file = f.name

    with pytest.raises(DataLoadError):
        loader.load_students(temp_file)
    os.unlink(temp_file)

def test_malformed_row():
    loader = DataLoader()
    # Crear un archivo CSV temporal con una fila malformada
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,name,email,phone,birthdate,faculty,year_level\n")
        f.write("1,Nate Bustamante,nate@example.com,1234567890,2000-01-01,Engineering,3\n")
        f.write("2,Alice Smith,alice@example.com,0987654321,1999-05-15,Science,not_a_number\n")  # year_level no es numérico
        temp_file = f.name

    members = loader.load_students(temp_file)
    assert len(members) == 1  # Solo se carga la primera fila
    os.unlink(temp_file)
