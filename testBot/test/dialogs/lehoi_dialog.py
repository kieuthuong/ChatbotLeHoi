# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class LehoiDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(LehoiDialog, self).__init__(dialog_id or LehoiDialog.__name__)

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
                    # self.confirm_step,
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
        # booking_details = step_context.options

        message_text = "Bạn muốn biết thêm thông về lề hội:"
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        ten_le_hoi = step_context.result
        # print(ten_le_hoi)
        import rdfextras
        rdfextras.registerplugins()
        filename = "fesivalVietNam.owl"
        import rdflib
        g = rdflib.Graph()
        result = g.parse(filename, format='xml')
        
        count_ten_le_hoi=0
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
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",step_context.result)
        for row in g.query(query):
            count_ten_le_hoi+=1

        #tìm lễ hội thông qua tên khác
        test=0
        if count_ten_le_hoi==0:
            pass
            count_ten_khac=0
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
                ?x :tenKhac ?a.
                FILTER( regex(?a,"fes","i") ) 
                }

                """
            query=query.replace("fes",step_context.result)
            cac_le_hoi=[]
            for row in g.query(query):
                a="%s" % row
                cac_le_hoi.append(a)
                count_ten_khac+=1
            
            if count_ten_khac==0:
                get_text = "Không tìm thấy lễ hội này"
                get_message = MessageFactory.text(
                get_text, get_text, InputHints.ignoring_input
                    )
                await step_context.context.send_activity(get_message)
                return await step_context.next(None)

            if count_ten_khac==1:
                test=1
                for x in cac_le_hoi:
                    get_text=step_context.result
                    ten_le_hoi=x
                get_text+=" là tên khác của " + ten_le_hoi
                get_message = MessageFactory.text(
                get_text, get_text, InputHints.ignoring_input
                    )
                await step_context.context.send_activity(get_message)
            
            if count_ten_khac>1:
                get_text = ten_le_hoi+" là tên khác của: "
                for x in cac_le_hoi:
                    get_text += x
                    get_text += ", "
                get_text+="... Bạn hãy nhập tên 1 trong các lễ hội kể trên để tìm kiếm thêm thông tin."
                get_message = MessageFactory.text(
                get_text, get_text, InputHints.ignoring_input
                    )
                await step_context.context.send_activity(get_message)
                return await step_context.next(None)
        
        #các thông tin về lễ hội
        #query loc
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
            ?x :toChucTai ?loc.
            ?loc :tenDiaDiem ?data.
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",ten_le_hoi)
        get_text += "Tổ chức tại "
        for row in g.query(query):
            a="%s" % row
            for x in data:
                if a==x:
                    break
            data.append(a)
        for x in data:
            get_text += x
            get_text += " "
            count +=1
        get_text += "."
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0

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
        query=query.replace("fes",ten_le_hoi)
        get_text += "Tổ chức vào "
        for row in g.query(query):
            a="%s" % row
            for x in data:
                if a==x:
                    break
            data.append(a)
        for x in data:
            get_text += x.lower()
            get_text += " "
            count +=1
        get_text += "."
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0

        #query ten khac
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
            ?x :tenKhac ?data.
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",ten_le_hoi)
        if test==0:
            get_text += "Còn có tên gọi khác là: "
            for row in g.query(query):
                a="%s" % row
                for x in data:
                    if a==x:
                        break
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
        query=query.replace("fes",ten_le_hoi)
        get_text += "Lịch sử: "
        for row in g.query(query):
            a="%s" % row
            data.append(a)
        for x in data:
            get_text += x.lower()
            get_text += " "
            count +=1
        get_text += "."
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0
        
         #query ton giao
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?data ?t
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :cuaTonGiao ?data.
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",ten_le_hoi)
        for row in g.query(query):
            get_text +="%s là lễ hội của %s " % row
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

            SELECT DISTINCT ?data
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :coHoatDong ?a.
            ?a :tenHoatDong ?data.
            FILTER( regex(?name,"fes","i") ) 
            }
        """
        query=query.replace("fes",ten_le_hoi)
        get_text += "Trong lễ hội có các hoạt động như: "
        for row in g.query(query):
            a="%s" % row
            data.append(a)
        for x in data:
            get_text += x.lower() 
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

        #query muc dich
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
            ?x :nhamHuongDen ?a.
            ?a :noiDungMucDich ?data.
            FILTER( regex(?name,"fes","i") ) 
            }
        """
        query=query.replace("fes",ten_le_hoi)
        get_text += " Mục đích của lễ hội là: "
        for row in g.query(query):
            a="%s" % row
            data.append(a)
        for x in data:
            get_text += x.lower() 
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

        #query danh hieu
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?d3 ?d1 
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :duocCongNhan ?d.
            ?d :tenDanhHieu ?d1.
            ?d :congNhanBoi ?d2.
            ?d2 :tenToChuc ?d3
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",ten_le_hoi)
        get_text += "Lễ hội được "
        for row in g.query(query):
            get_text +="%s công nhận %s" % row
            get_text += "; "
            count +=1
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0

        #query link
        query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 

            SELECT DISTINCT ?link
            WHERE 
            { 
            ?x :tenLeHoi ?name.
            ?x :linkChiTiet ?link
            FILTER( regex(?name,"fes","i") ) 
            }

            """
        query=query.replace("fes",ten_le_hoi)
        get_text += "Bạn có thể tham khảo chi tiết thông tin về " + step_context.result + " trong link bài viết sau: "
        for row in g.query(query):
            get_text +="%s" % row
            count +=1
        if count != 0:
            get_message = MessageFactory.text(
            get_text, get_text, InputHints.ignoring_input
                )
            await step_context.context.send_activity(get_message)
        data.clear()
        get_text = ""
        count=0
        
        return await step_context.next(None)

