# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class DantocDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(DantocDialog, self).__init__(dialog_id or DantocDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.destination_step,
                    # self.origin_step,
                    # self.travel_date_step,
                    self.confirm_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        dantoc_details = step_context.options
        if not dantoc_details.danToc:
            return await step_context.next(None)
        import rdfextras
        rdfextras.registerplugins()
        filename = "../../OntologyFile/fesivalVietNam.owl"
        import rdflib
        g = rdflib.Graph()
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
        ?x :cuaDanToc ?eth.
        ?eth :tenDanToc ?neth.
        FILTER( regex(?neth,"danToc","i")) 
        }

        """
        query=query.replace("danToc",dantoc_details.danToc)
        count = 0
        for row in g.query(query):
            fes="%s" % row
            loc=[]
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
            FILTER( regex(?name,"fes","i") ) 
            }

            """
            query1=query1.replace("fes",fes)
            get_text = fes+" tổ chức tại "
            for row in g.query(query1):
                a="%s" % row
                for x in loc:
                    if a==x:
                        break
                loc.append(a)
            for x in loc:
                get_text += x 
                get_text += " "
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
            loc.clear()
            count+=1
        if count==0:
            get_text = "Chưa tìm thấy lễ hội nào của người dân tộc " + dantoc_details.danToc
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                    )
            await step_context.context.send_activity(get_message)
            return await step_context.next(None)
            # return await step_context.next(next(dantoc_details.danToc))
        return await step_context.next(dantoc_details.danToc)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        dantoc_details = step_context.options

        # Capture the results of the previous step
        message_text = "Bạn muốn biết thêm thông về lề hội:"
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_message = step_context.result
        
        import rdfextras
        rdfextras.registerplugins()
        filename = "../../OntologyFile/fesivalVietNam.owl"
        import rdflib
        g = rdflib.Graph()
        result = g.parse(filename, format='xml')
        #query time
        data=[]
        count = 0
        get_text = ""
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?data
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :thoiGianToChuc ?data.
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",step_context.result)
        get_text = step_context.result +" tổ chức vào "
        for row in g.query(query):
            a="%s" % row
            for x in data:
                if a==x:
                    break
            data.append(a)
        for x in data:
            get_text += x 
            get_text += " "
        get_message = MessageFactory.text(
        get_text, get_text, InputHints.ignoring_input
            )
        await step_context.context.send_activity(get_message)
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0
        
        #query lich su
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?data
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :lichSu ?data.
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",step_context.result)
        get_text += step_context.result +" lịch sử lễ hội: "
        for row in g.query(query):
            a="%s" % row
            data.append(a)
        for x in data:
            get_text += x 
            get_text += " "
            count +=1
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0
        
        #query act
        query = """
         PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?act
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :coHoatDong ?a.
            ?a :tenHoatDong ?act.
            FILTER( regex(?name,"fes","i") ) 
            }
        """
        query=query.replace("fes",step_context.result)
        get_text += step_context.result +" có các hoạt động như: "
        for row in g.query(query):
            a="%s" % row
            data.append(a)
        for x in data:
            get_text += x 
            get_text += ", "
            count +=1
        get_text += "..."
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0

        
        return await step_context.next(None)

    def is_ambiguous(self, datax: str) -> bool:
        datax_property = datax(datax)
        return "definite" not in datax_property.types
