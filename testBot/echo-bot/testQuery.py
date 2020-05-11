import rdfextras
rdfextras.registerplugins()
filename = "../../OntologyFile/fesivalVietNam.owl" 
import rdflib
g = rdflib.Graph()
g1 = rdflib.Graph()
result = g.parse(filename, format='xml')
query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>    
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

SELECT DISTINCT ?name
WHERE 
{ 
?x :tenLeHoi ?name.
?x :coHoatDong ?act.
?x :toChucTai ?loc.
?act rdfs:label ?l.
?act :tenHoatDong ?nact.
?loc :tenDiaDiem ?nloc.
FILTER( regex(?nloc,"hà nội","i") ) 
FILTER( regex(?l,"hoạt động vui chơi","i") ) 
}

"""
for row in g.query(query):
    a="%s" % row
    lista=[]
    query1 = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>    
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
    PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

    SELECT DISTINCT ?nloc
    WHERE 
    { 
    ?x :tenLeHoi ?name.
    ?x :toChucTai ?loc.
    ?loc :tenDiaDiem ?nloc.
    FILTER( regex(?name,"abc","i") ) 
    }

    """
    query1=query1.replace("abc",a)
    print(a + ' tổ chức tại', end=': ')
    for row in g.query(query1):
        b="%s" % row
        # for x in lista:
        #     if b==x:
        #         break
        lista.append(b)
        for x in lista:
            print(x,end=' ')
        lista.clear()
    print('\n')
    # lista.clear()
# list = []
# for row in g.query(query):
#   list.append()
# for row in g.query(query):
#   print(repr(row))
#   print(type(row))

