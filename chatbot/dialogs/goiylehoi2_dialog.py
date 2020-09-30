# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class GoiyLehoiDialog2(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(GoiyLehoiDialog2, self).__init__(dialog_id or GoiyLehoiDialog2.__name__)

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
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        goiylehoi_details = step_context.options
        if goiylehoi_details.mucDich is None:
            return await step_context.end_dialog()
        else:
            if goiylehoi_details.diaDiem is None:
                message_text = "Bạn dự định du lịch lễ hội ở tỉnh nào của Việt Nam ?"
                prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.expecting_input
                )
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )
            return await step_context.next(goiylehoi_details.diaDiem)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        count = 0
        goiylehoi_details = step_context.options
        goiylehoi_details.diaDiem = step_context.result
        import rdfextras
        rdfextras.registerplugins()
        # filename = "fesivalVietNam.owl" 
        filename = "fesivalVietNam.owl"
        import rdflib
        g = rdflib.Graph()

        result = g.parse(filename, format='xml')
        # print(result)
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
        ?x :nhamHuongDen ?act.
        ?x :toChucTai ?loc.
        ?act rdfs:label ?l.
        ?act :noiDungMucDich ?nact.
        ?loc :tenDiaDiem ?nloc.
        FILTER( regex(?nloc,"diaDiem","i") ) 
        FILTER( regex(?l,"mucDich","i") ) 
        }

        """
        query=query.replace("diaDiem",goiylehoi_details.diaDiem)
        query=query.replace("mucDich",goiylehoi_details.mucDich)
        for row in g.query(query):
            fes="%s" % row
            count+=1
            data=[]
            query1 = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?nact
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :nhamHuongDen ?act.
            ?act rdfs:label ?l.
            ?act :noiDungMucDich ?nact.
            FILTER( regex(?name,"fes","i") ) 
            FILTER( regex(?l,"mucDich","i") ) 
            }

            """
            if count==1:    
                get_text = "Bạn có thể tham khảo các lễ hội sau:"
                get_message = MessageFactory.text(
                get_text, get_text, InputHints.ignoring_input
                    )
                await step_context.context.send_activity(get_message)
            query1=query1.replace("fes",fes)
            query1=query1.replace("mucDich",goiylehoi_details.mucDich)
            get_text = fes+" với mục đích "
            for row in g.query(query1):
                a="%s" % row
                for x in data:
                    if a==x:
                        break
                data.append(a)
            for x in data:
                get_text += x 
                get_text += ", "
            get_text += "..."
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
            data.clear()
            get_text = ""
        
        if count == 0:
            get_text = "Hiện tại chưa tìm được lễ hội bạn mong muốn ở "+goiylehoi_details.diaDiem+". Bạn có thể tham khảo 1 vài lễ hội ở các địa phương khác như:"
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                    )
            await step_context.context.send_activity(get_message)
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
            ?x :nhamHuongDen ?act.
            ?act rdfs:label ?l.
            ?act :noiDungMucDich ?nact.
            FILTER( regex(?l,"mucDich","i") ) 
            }

            """
            query=query.replace("mucDich",goiylehoi_details.mucDich)
            for row in g.query(query):
                fes="%s" % row
                count+=1
                if count==6:
                    break
                data=[]
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
                get_text = fes+" tổ chức tại: "
                for row in g.query(query1):
                    a="%s" % row
                    data.append(a)
                for x in data:
                    get_text += x 
                    get_text += " "
                get_message = MessageFactory.text(
                get_text, get_text, InputHints.ignoring_input
                    )
                await step_context.context.send_activity(get_message)
                data.clear()

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            goiylehoi_details = step_context.options

            return await step_context.end_dialog(goiylehoi_details)
        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
