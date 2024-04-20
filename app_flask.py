from flask import Flask, render_template, request, Response
import xml.etree.ElementTree as ET
from lxml import etree 
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)


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
        publisher = request.form['publisher']  # Get publisher from form
        genre = request.form['genre']  # Get genre from form

        # Generate unique ID for the book
        book_id = str(uuid.uuid4())

        # Create XML element for the book
        book_element = ET.Element('book', attrib={'id': book_id})
        title_element = ET.SubElement(book_element, 'title')
        title_element.text = title
        author_element = ET.SubElement(book_element, 'author')
        author_element.text = author
        isbn_element = ET.SubElement(book_element, 'isbn')
        isbn_element.text = isbn
        publication_year_element = ET.SubElement(book_element, 'publication_year')
        publication_year_element.text = publication_year
        publisher_element = ET.SubElement(book_element, 'publisher')  # Add publisher element
        publisher_element.text = publisher  # Set text of publisher element
        genre_element = ET.SubElement(book_element, 'genre')  # Add genre element
        genre_element.text = genre  # Set text of genre element

        # Add reviews subchild
        reviews_element = ET.SubElement(book_element, 'reviews')
        review_element = ET.SubElement(reviews_element, 'review')
        rating_element = ET.SubElement(review_element, 'rating')
        rating_element.text = request.form['rating']
        comment_element = ET.SubElement(review_element, 'comment')
        comment_element.text = request.form['comment']

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
    return render_template('validate.html',message=None)
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
        with open(xml_file_path, 'r') as file:
            xml_content = file.read()

        # Remove the temporary XML file
        os.remove(xml_file_path)

        # Return XML content and message
        return render_template('validate.html', message=validation_result, xml_content=xml_content)
    

    except etree.XMLSyntaxError as e:
        validation_result = f'XML Syntax Error: {str(e)}'
   
    except etree.DocumentInvalid as e:
        validation_result = f'Document Invalid: {str(e)}'

    except Exception as e:
        validation_result = str(e)
    finally:
        if os.path.exists(xml_file_path):
            os.remove(xml_file_path)
            
    return render_template('validate.html',message=validation_result )
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
