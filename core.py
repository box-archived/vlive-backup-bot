import re
from prompt_toolkit.shortcuts import (
    message_dialog,
    input_dialog,
    button_dialog
)
from prompt_toolkit.styles import (
    Style,
)
import pyclip

ptk_dialog_style = Style.from_dict({
    'dialog': 'bg:#000000',
    'button': '#1ecfff',
    'dialog.body': 'bg:#000000 #1ecfff',
    'dialog shadow': 'bg:#000000',
    'frame.label': '#1ecfff',
    'dialog.body label': '#ffffff',
})

ptk_flat_style = Style.from_dict({
    'dialog': 'bg:#000000',
    'button': '#1ecfff',
    'dialog.body': 'bg:#000000 #000000',
    'dialog shadow': 'bg:#000000',
    'frame.label': '#1ecfff',
    'dialog.body label': '#ffffff',
})


def shutdown():
    result = button_dialog(
        title='VLIVE-BACKUP-BOT',
        text='모든 작업이 완료되었습니다\n엔터키를 누르면 프로그램을 종료합니다.',
        buttons=[
            ('종료', True),
        ],
        style=ptk_dialog_style
    ).run()
    if result:
        exit()


def dialog_error_message(message):
    message_dialog(
        title="오류",
        text=message,
        style=ptk_dialog_style
    ).run()


def query_license_agreement():
    lic = ""
    lic += '이 소프트웨어는 자유 소프트웨어로, GPL-3.0 License 를 따릅니다.\n'
    lic += "라이센스의 전문은 깃헙 레포에서 확인할 수 있습니다.\n\n"
    lic += "이 소프트웨어의 이용으로 인한 책임은 사용자에게 있으며,\n"
    lic += "저장한 영상을 타인에게 공유할 시 저작권법 위반에 해당될 수 있습니다."

    formatted_lic = "\n".join(map(lambda x: x.center(60), lic.split("\n")))

    if not button_dialog(
            title='라이선스',
            text=formatted_lic,
            buttons=[
                ('동의', True),
                ('거부', False),
            ],
            style=ptk_dialog_style
    ).run():
        shutdown()


def query_download_url():
    url_rule = re.compile('((?<=vlive.tv\/channel\/).+(?=\/board\/))\/board\/(\d+)')
    target_url = ""
    while True:
        target_url = input_dialog(
            title="다운로드 URL 입력",
            text="다운받을 게시판의 주소를 입력하세요.\n(예: https://www.vlive.tv/channel/B039DF/board/7192 )",
            ok_text="확인",
            cancel_text="붙여넣기",
            style=ptk_flat_style,
        ).run()
        if target_url is None:
            try:
                target_url = pyclip.paste().decode()
            except:
                target_url = ""

        regex_result = url_rule.findall(target_url)
        if len(regex_result) == 1:
            if button_dialog(
                title='확인',
                text='입력하신 정보가 맞습니까?\n\n채널: %s\n게시판: %s' % (regex_result[0][0], regex_result[0][1]),
                buttons=[
                    ('예', True),
                    ('아니요', False),
                ],
                style=ptk_dialog_style
            ).run():
                return regex_result[0]
        else:
            dialog_error_message("유효하지 않은 URL 입니다!")


def main():
    query_license_agreement()

    target_channel, target_board = query_download_url()

    result = button_dialog(
        title='멤버십 선택',
        text='멤버십(팬십) 컨텐츠입니까?',
        buttons=[
            ('예', True),
            ('아니요', False),
        ],
        style=ptk_dialog_style
    ).run()

    return shutdown()


if __name__ == '__main__':
    main()
