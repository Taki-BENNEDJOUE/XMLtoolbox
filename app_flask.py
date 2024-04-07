from flask import Flask, render_template, request, Response
import xml.etree.ElementTree as ET
from lxml import etree 
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

def parse_xml_content(xml_content):
    try:
        # Find the index of each tag and extract the content between them
        title_start = xml_content.find('<title>') + len('<title>')
        title_end = xml_content.find('</title>')
        title = xml_content[title_start:title_end].strip()

        author_start = xml_content.find('<author>') + len('<author>')
        author_end = xml_content.find('</author>')
        author = xml_content[author_start:author_end].strip()

        isbn_start = xml_content.find('<isbn>') + len('<isbn>')
        isbn_end = xml_content.find('</isbn>')
        isbn = xml_content[isbn_start:isbn_end].strip()

        pub_year_start = xml_content.find('<publication_year>') + len('<publication_year>')
        pub_year_end = xml_content.find('</publication_year>')
        pub_year = xml_content[pub_year_start:pub_year_end].strip()

        return {'title': title, 'author': author, 'isbn': isbn, 'publication_year': pub_year}
    except Exception as e:
        print(str(e))
        return None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_xml' , methods=['GET', 'POST'])
def create_xml():
    if request.method == 'POST':  
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']

        # Create XML element for the book
        book_element = ET.Element('book')
        title_element = ET.SubElement(book_element, 'title')
        title_element.text = title
        author_element = ET.SubElement(book_element, 'author')
        author_element.text = author
        isbn_element = ET.SubElement(book_element, 'isbn')
        isbn_element.text = isbn
        publication_year_element = ET.SubElement(book_element, 'publication_year')
        publication_year_element.text = publication_year

        # Load existing XML file or create a new one
        root = ET.Element('library')
        try:
            tree = ET.parse('library.xml')
            root = tree.getroot()
        except FileNotFoundError:
            pass

        # Add the new book element to the XML
        root.append(book_element)

        # Save the modified XML back to the file
        tree = ET.ElementTree(root)
        tree.write('library.xml')

        return render_template('create.html')
    return render_template('create.html')

@app.route('/validate_xml')
def validate_xml():
    return render_template('validate.html',message=None, parsed_content=None)

@app.route('/validate_xml', methods=['POST'])
def validate():
    # Get uploaded XML file and validation method from the form
    xml_file = request.files['xml_file']
    validation_method = request.form['validation_method']

    # Save the XML file temporarily
    xml_file_path = 'temp.xml'
    xml_file.save(xml_file_path)

    try:
        # Validate the XML file based on the chosen method
        xml_tree = etree.parse(xml_file_path)
        if validation_method == 'xsd':
            schema_file_path = os.path.join(app.root_path, 'static', 'library.xsd')
            schema = etree.XMLSchema(etree.parse(schema_file_path))
         
        elif validation_method == 'dtd':
            schema_file_path = os.path.join(app.root_path, 'static', 'library.dtd')
            schema = etree.DTD(open(schema_file_path))
            
          

        # Validate the XML file against the schema
        schema.assertValid(xml_tree)
        validation_result = 'XML file is valid.'
        with open(xml_file_path, 'r') as f:
            xml_content = f.read()
        parsed_content = parse_xml_content(xml_content)
    except etree.XMLSyntaxError as e:
        validation_result = f'XML Syntax Error: {str(e)}'
        parsed_content = None
    except etree.DocumentInvalid as e:
        validation_result = f'Document Invalid: {str(e)}'
        parsed_content = None
    except Exception as e:
        validation_result = str(e)
        parsed_content = None
    finally:
    # Remove the temporary XML file
        os.remove(xml_file_path)

    return render_template('validate.html',message=validation_result, xml_content = parsed_content)

@app.route('/download')
def download():
    try:
        # Serve XML file for download
        with open('library.xml', 'rb') as xml_file:
            xml_content = xml_file.read()

        # Delete the XML file after downloading
        os.remove('library.xml')

        return Response(xml_content, mimetype='application/xml', headers={'Content-Disposition': 'attachment;filename=library.xml'})
    except FileNotFoundError:
        return "No data available."

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
