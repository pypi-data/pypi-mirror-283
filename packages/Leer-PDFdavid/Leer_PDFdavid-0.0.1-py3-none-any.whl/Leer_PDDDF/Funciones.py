import fitz #librería pymupdf

def leer_pdfdavid(path):
    try:
        with fitz.open(path) as file:
            text = ''
            for page in file:
                text += page.getText()
        print(text)
    except:
        pass