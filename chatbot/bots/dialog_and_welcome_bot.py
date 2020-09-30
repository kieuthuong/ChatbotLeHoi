# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os.path

from typing import List
from botbuilder.core import (
    ConversationState,
    MessageFactory,
    UserState,
    TurnContext,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import Attachment, ChannelAccount, SuggestedActions, CardAction, ActionTypes
from helpers.dialog_helper import DialogHelper

from .dialog_bot import DialogBot


class DialogAndWelcomeBot(DialogBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        super(DialogAndWelcomeBot, self).__init__(
            conversation_state, user_state, dialog
        )
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
            if member.id != turn_context.activity.recipient.id:
                # welcome_card = self.create_adaptive_card_attachment()
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Chào mừng bạn đến với bot hỗ trợ du lịch lễ hội Việt Nam!"
                    )
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Chúng tôi sẽ giúp bạn tìm hiểu về các lễ hội tại Việt Nam và hỗ trợ tìm kiếm lễ hội mà bạn mong muốn."
                    )
                )

                await DialogHelper.run_dialog(
                    self.dialog,
                    turn_context,
                    self.conversation_state.create_property("DialogState"),
                )
         
    