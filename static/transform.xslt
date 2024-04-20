<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Template to match the root element -->
  <xsl:template match="/">
    <html>
      <head>
        <title>Library Catalog</title>
        <style>
          table {
            border-collapse: collapse;
            width: 100%;
          }
          th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
          }
          th {
            background-color: #f2f2f2;
          }
        </style>
      </head>
      <body>
        <h1>Library Catalog</h1>
        <!-- Apply the template for each book -->
        <xsl:apply-templates select="library/book"/>
      </body>
    </html>
  </xsl:template>

  <!-- Template to match each book -->
  <xsl:template match="book">
    <div class="book">
      <h2>Book Details</h2>
      <table>
        <tr>
          <th>ID</th>
          <td><xsl:value-of select="@id"/></td>
        </tr>
        <tr>
          <th>Title</th>
          <td><xsl:value-of select="title"/></td>
        </tr>
        <tr>
          <th>Author</th>
          <td><xsl:value-of select="author"/></td>
        </tr>
        <tr>
          <th>ISBN</th>
          <td><xsl:value-of select="isbn"/></td>
        </tr>
        <tr>
          <th>Publication Year</th>
          <td><xsl:value-of select="publication_year"/></td>
        </tr>
        <tr>
          <th>Publisher</th>
          <td><xsl:value-of select="publisher"/></td>
        </tr>
        <tr>
          <th>Genre</th>
          <td><xsl:value-of select="genre"/></td>
        </tr>
        <tr>
          <th>Reviews</th>
          <td>
            <xsl:apply-templates select="reviews/review"/>
          </td>
        </tr>
      </table>
    </div>
    <br/>
  </xsl:template>

  <!-- Template to match each review -->
  <xsl:template match="review">
    <p><strong>Rating:</strong> <xsl:value-of select="rating"/> - <strong>Comment:</strong> <xsl:value-of select="comment"/></p>
  </xsl:template>

</xsl:stylesheet>
