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

from lehoi_details import LeHoiDetails

from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .lehoi_dialog import LehoiDialog
from .diadiem_dialog import DiadiemDialog
from .goiylehoi_dialog import GoiyLehoiDialog
from .goiylehoi2_dialog import GoiyLehoiDialog2
from .dantoc_dialog import DantocDialog

class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: FlightBookingRecognizer, lehoi_dialog: LehoiDialog, diadiem_dialog: DiadiemDialog, dantoc_dialog:DantocDialog, goiylehoi_dialog: GoiyLehoiDialog, goiylehoi2_dialog: GoiyLehoiDialog2
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer
        self._lehoi_dialog_id = lehoi_dialog.id
        self._diadiem_dialog_id = diadiem_dialog.id
        self._dantoc_dialog_id = dantoc_dialog.id
        self._goiylehoi_dialog_id = goiylehoi_dialog.id
        self._goiylehoi2_dialog_id = goiylehoi2_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(lehoi_dialog)
        self.add_dialog(diadiem_dialog)
        self.add_dialog(dantoc_dialog)
        self.add_dialog(goiylehoi_dialog)
        self.add_dialog(goiylehoi2_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.option_step, self.act_step, self.final_step]
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

        reply = MessageFactory.text("Mời lựa chọn:")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(title="Tìm hiểu lễ hội Việt Nam", type=ActionTypes.im_back, value="Tìm hiểu lễ hội Việt Nam"),
                CardAction(title="Tìm kiếm các lễ hội", type=ActionTypes.im_back, value="Tìm kiếm các lễ hội"),
                CardAction(title="Gợi ý du lịch lễ hội", type=ActionTypes.im_back, value="Gợi ý du lịch lễ hội"),
            ]
        )

        # return await step_context.context.send_activity(reply)
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def option_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        a1="tìm hiểu lễ hội việt nam"
        a2="tìm kiếm các lễ hội"
        a3="gợi ý du lịch lễ hội"
            
        if(step_context.result==a1):
            return await step_context.begin_dialog(
                self._lehoi_dialog_id, LeHoiDetails()
            )

        if(step_context.result == a2):
            get_text = "Bạn có thể tìm kiếm các lễ hội theo địa điểm hoặc các thông tin khác liên quan đến lễ hội như dân tộc, mục đích, hoạt động trong lễ hội..."
            get_weather_message = MessageFactory.text(
                get_text, get_text, InputHints.expecting_input
            )
            # await step_context.context.send_activity(get_weather_message)
            return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=get_weather_message)
        )

        if(step_context.result==a3):
            get_text = "Bạn thích tham gia những hoạt động gì khi du lịch lễ hội?"
            get_weather_message = MessageFactory.text(
                get_text, get_text, InputHints.expecting_input
            )
            # await step_context.context.send_activity(get_weather_message)
            return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=get_weather_message)
        )
        else:
            didnt_understand_text = (
                "Xin lỗi, bạn có thể lựa chọn một trong các chức năng sau (@_@;)"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)
            return await step_context.next(None)

        # return await step_context.next(None)

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == Intent.TIMLEHOI.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._diadiem_dialog_id, luis_result)

        if intent == Intent.DANTOC.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._dantoc_dialog_id, luis_result)

        if intent == Intent.GOIYLEHOI.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._goiylehoi_dialog_id, luis_result)

        if intent == Intent.GOIYLEHOI2.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._goiylehoi2_dialog_id, luis_result)

        else:
            return await step_context.next(None)
        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result
            
        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)   

    
