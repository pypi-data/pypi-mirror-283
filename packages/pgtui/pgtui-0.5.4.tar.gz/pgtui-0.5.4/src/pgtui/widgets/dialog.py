from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Label, Static

from pgtui.widgets.menu import Menu, MenuItem
from pgtui.widgets.modal import ModalScreen, ModalTitle


class MessageDialog(ModalScreen[None]):
    DEFAULT_CSS = """
    .dialog_button {
        height: 1;
        min-width: 1;
        border: none;
        border-top: none;
        border-bottom: none;
    }
    """

    def __init__(self, title: str, body: str | None, error: bool = False):
        self.message_title = title
        self.message_body = body
        self.error = error
        super().__init__()

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(self.message_title, error=self.error)
        if self.message_body:
            yield Static(self.message_body, markup=False)
        yield Button("[ OK ]", variant="default", classes="dialog_button")

    def on_button_pressed(self, message: Button.Pressed):
        self.dismiss()


class ConfirmationDialog(ModalScreen[bool]):
    def __init__(
        self,
        modal_title: str,
        *,
        modal_text: str | None = None,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel",
        show_status_bar: bool = False,
    ):
        self.modal_title = modal_title
        self.modal_text = modal_text
        self.confirm_label = confirm_label
        self.cancel_label = cancel_label
        self.show_status_bar = show_status_bar
        super().__init__()

    def compose_modal(self) -> ComposeResult:
        yield ModalTitle(self.modal_title)
        if self.modal_text:
            yield Label(self.modal_text)
        yield Menu(
            MenuItem("confirm", self.confirm_label),
            MenuItem("cancel", self.cancel_label),
        )
        hide_class = "" if self.show_status_bar else "hide"
        yield Label("", classes=f"dialog_status_bar {hide_class}")

    @on(Menu.ItemSelected)
    def _on_item_selected(self, message: Menu.ItemSelected):
        message.stop()

        match message.item.code:
            case "confirm":
                self.on_confirm()
            case "cancel":
                self.on_cancel()
            case _:
                pass

    def on_confirm(self) -> None:
        self.dismiss(True)

    def on_cancel(self) -> None:
        self.dismiss(False)

    def show_message(self, msg: str, style: str | None = None):
        msg = f"[{style}]{msg}[/]" if style else msg
        self.query_one(".dialog_status_bar", Label).update(msg)
