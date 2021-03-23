from prompt_toolkit import Application
from prompt_toolkit.shortcuts import yes_no_dialog

app = Application(full_screen=True)

result = yes_no_dialog(
    title='멤버십 선택',
    text='멤버십(팬십) 컨텐츠입니까?').run()
