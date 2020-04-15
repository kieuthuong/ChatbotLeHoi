# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext, ActivityHandler
from botbuilder.schema import InputHints, ChannelAccount, CardAction, ActionTypes, SuggestedActions 

from booking_details import BookingDetails, LeHoiDetails
from lehoi_details import GoiyLehoiDetails

from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .booking_dialog import BookingDialog
from .lehoi_dialog import LehoiDialog
from .goiylehoi_dialog import GoiyLehoiDialog

class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: FlightBookingRecognizer, booking_dialog: BookingDialog, lehoi_dialog: LehoiDialog, goiylehoi_dialog: GoiyLehoiDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer
        self._booking_dialog_id = booking_dialog.id
        self._lehoi_dialog_id = lehoi_dialog.id
        self._goiylehoi_dialog_id = goiylehoi_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(booking_dialog)
        self.add_dialog(lehoi_dialog)
        self.add_dialog(goiylehoi_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"
        

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )

        reply = MessageFactory.text("What is your favorite color?")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(title="Booking", type=ActionTypes.im_back, value="Booking"),
                CardAction(title="Tìm hiểu lễ hội Việt Nam", type=ActionTypes.im_back, value="2"),
                CardAction(title="Gợi ý du lịch lễ hội", type=ActionTypes.im_back, value="3"),
            ]
        )

        # return await step_context.context.send_activity(reply)
        
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )


    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._booking_dialog_id, BookingDetails()
            )

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )
        
        if intent == Intent.BOOK_FLIGHT.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )
             # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)

        # if intent == Intent.TIMLEHOI.value and luis_result:
        #     # Run the BookingDialog giving it whatever details we have from the LUIS call.
        #     return await step_context.begin_dialog(self._lehoi_dialog_id, luis_result)

        if intent == Intent.GOIYLEHOI.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._goiylehoi_dialog_id, luis_result)

        if intent == Intent.GET_WEATHER.value:
            get_weather_text = "TODO: get weather flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)

        # if intent == Intent.TIMLEHOI.value:
            
        #     import rdfextras
        #     rdfextras.registerplugins()
        #     filename = "fesivalVietNam.owl" 
        #     import rdflib
        #     g = rdflib.Graph()

        #     result = g.parse(filename, format='xml')
        #     print(result)
        #     query = """
        #     PREFIX owl: <http://www.w3.org/2002/07/owl#>    
        #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
        #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
        #     PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
        #     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        #     PREFIX :<http://www.semanticweb.org/admin/ontologies/2020/2/untitled-ontology-5#> 
        #     SELECT ?name  ?nloc
        #     WHERE 
        #     { 
        #     ?x :tenLeHoi ?name.
        #     {
        #     ?x :toChucTai ?loc.
        #     {
        #     ?loc :tenDiaDiem ?nloc
        #     FILTER( regex(?nloc,"abc","i") ) 
        #     }
        #     }
        #     }
        #     """
        #     query=query.replace("abc",luis_result.diaDiem)
        #     get_weather_text = " "
        #     for row in g.query(query):
        #         print(repr(row))
        #         print(type(row))
        #     for row in g.query(query):
        #         print("%s tổ chức tại: %s" % row)
        #         get_weather_text = "%s tổ chức tại: %s" % row+'\n'
        #         get_weather_message = MessageFactory.text(
        #             get_weather_text, get_weather_text, InputHints.ignoring_input
        #         )
        #         await step_context.context.send_activity(get_weather_message)

        if step_context.result=='Booking':
            get_weather_text = "diem xuat phat"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.expecting_input
            )
            # await step_context.context.send_activity(get_weather_message)
            return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=get_weather_message)
        )

        if step_context.result=='2':
            print(step_context.result)
            print(type(step_context.result))
            get_weather_text = "le hoi o"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.expecting_input
            )
            # await step_context.context.send_activity(get_weather_message)
            return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=get_weather_message)
        )

        if step_context.result=='3':
            # print(step_context.result)
            # print(type(step_context.result))
            get_weather_text = "Bạn thích tham gia những hoạt động gì khi du lịch lễ hội?"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.expecting_input
            )
            # await step_context.context.send_activity(get_weather_message)
            return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=get_weather_message)
        )

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        # if step_context.result is not None:
        #     result = step_context.result

        #     # Now we have all the booking details call the booking service.

        #     # If the call to the booking service was successful tell the user.
        #     # time_property = Timex(result.travel_date)
        #     # travel_date_msg = time_property.to_natural_language(datetime.now())
        #     msg_txt = f"I have you booked to {result.destination} from {result.origin} on {result.travel_date}"
        #     message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
        #     await step_context.context.send_activity(message)

        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)

    @staticmethod
    async def _show_warning_for_unsupported_cities(
        context: TurnContext, luis_result: BookingDetails
    ) -> None:
        if luis_result.unsupported_airports:
            message_text = (
                f"Sorry but the following airports are not supported:"
                f" {', '.join(luis_result.unsupported_airports)}"
            )
            message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await context.send_activity(message)
