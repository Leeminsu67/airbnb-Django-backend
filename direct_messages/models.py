from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):
    """ChattingRoom Model Definition"""

    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):
    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="message",
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="message",
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"
