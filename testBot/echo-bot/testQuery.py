import rdfextras
rdfextras.registerplugins()
filename = "fesivalVietNam.owl" 
import rdflib
g = rdflib.Graph()

result = g.parse(filename, format='xml')
print(result)
query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>	
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>	
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>	
PREFIX xml: <http://www.w3.org/XML/1998/namespace>	
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 
SELECT ?name  ?nloc
WHERE 
{ 
?x :tenLeHoi ?name.
{
?x :toChucTai ?loc.
{
?loc :tenDiaDiem ?nloc
FILTER( regex(?nloc,"Nam Định","i") ) 
}
}
}
"""

for row in g.query(query):
	print(repr(row))
	print(type(row))
for row in g.query(query):
    print("%s tổ chức tại: %s" % row)
