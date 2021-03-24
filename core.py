from collections import deque
import time
import re
import os

import vlivepy
import vlivepy.exception
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import (
    message_dialog,
    input_dialog,
    button_dialog,
    progress_dialog,
    clear,
)
from prompt_toolkit.styles import (
    Style,
)
import pyclip

ptk_session = PromptSession()
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


def dialog_error_message(text):
    message_dialog(
        title="오류",
        text=text,
        style=ptk_dialog_style
    ).run()


def dialog_yn(title, text):
    return button_dialog(
        title=title,
        text=text,
        buttons=[
            ('예', True),
            ('아니요', False),
        ],
        style=ptk_dialog_style
    ).run()


def dialog_download_end():
    return dialog_yn("다운로드 완료", "다운로드가 완료되었습니다.\n다른 게시판을 추가로 다운로드 하겠습니까?")


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
            if dialog_yn(
                title='확인',
                text='입력하신 정보가 맞습니까?\n\n채널: %s\n게시판: %s' % (regex_result[0][0], regex_result[0][1]),
            ):
                return regex_result[0]
        else:
            dialog_error_message("유효하지 않은 URL 입니다!")


def query_membership():
    membership_yn = dialog_yn(
        title='멤버십 선택',
        text='멤버십(팬십) 컨텐츠입니까?',
    )

    if membership_yn:
        # Session exist check
        if os.path.isfile("vlive-backup-bot.session"):
            if dialog_yn("로그인", "로그인 내역이 존재합니다.\n 기존 세션을 이용하시겠습니까?"):
                return True

        # Login
        while True:

            user_email = ""
            while len(user_email) == 0:
                user_email = input_dialog(
                    title="로그인",
                    text="VLIVE 이메일 아이디를 입력하세요.",
                    ok_text="확인",
                    cancel_text="취소",
                    style=ptk_flat_style,
                ).run()
                if user_email is None:
                    if dialog_yn("로그인", "로그인을 취소하시겠습니까?"):
                        return False
                    else:
                        user_email = ""
                        continue

            # password
            user_pwd = ""
            while len(user_pwd) == 0:
                user_pwd = input_dialog(
                    title="로그인",
                    text="VLIVE 비밀번호를 입력하세요.",
                    ok_text="확인",
                    cancel_text="취소",
                    style=ptk_flat_style,
                    password=True
                ).run()
                if user_pwd is None:
                    if dialog_yn("로그인", "로그인을 취소하시겠습니까?"):
                        return False
                    else:
                        user_pwd = ""
                        continue

            login_callback_result = False

            # try login
            def login_try(report_progress, report_log):
                nonlocal login_callback_result
                report_log("로그인 시도중입니다.\n")
                report_progress(50)
                try:
                    sess = vlivepy.UserSession(user_email, user_pwd)
                except vlivepy.exception.APISignInFailedError:
                    # break
                    report_log("로그인에 실패했습니다.\n")
                    login_callback_result = False
                    report_progress(100)
                else:
                    report_progress(75)
                    # dump session
                    report_log("세션파일을 생성합니다.\n")
                    with open("vlive-backup-bot.session", "wb") as f:
                        vlivepy.dumpSession(sess, f)

                    # break
                    report_log("로그인에 성공했습니다.\n")
                    time.sleep(1)
                    login_callback_result = True
                    report_progress(100)

            progress_dialog("로그인", None, login_try).run()
            if login_callback_result:
                return True
            else:
                dialog_error_message("로그인에 실패했습니다.\n계정 정보를 확인 해 주세요.")

    return membership_yn


def query_options():
    opt_ovp = dialog_yn("옵션", "공식 비디오를 다운로드 하시겠습니까?")
    opt_post = dialog_yn("옵션", "포스트를 다운로드 하시겠습니까?")
    opt_amount = None
    while opt_amount is None:
        opt_amount = input_dialog(
            title="옵션",
            text="다운로드 할 개수를 입력 해 주세요.\n게시물은 최신순으로 결정됩니다.\n\n(전체 다운로드 시 0 입력)",
            ok_text="확인",
            cancel_text="재설정",
            style=ptk_flat_style,
        ).run()
        try:
            opt_amount = int(opt_amount)
        except ValueError:
            dialog_error_message("유효하지 않은 값입니다.")
            opt_amount = None
            continue
        except TypeError:
            opt_amount = None
            continue
        else:
            return opt_ovp, opt_post, opt_amount


def main():
    clear()
    target_channel, target_board = query_download_url()

    membership = query_membership()

    opt_ovp, opt_post, opt_amount = query_options()

    if not opt_ovp and not opt_post:
        return dialog_download_end()

    return dialog_download_end()


if __name__ == '__main__':
    query_license_agreement()

    while True:
        if main():
            continue
        else:
            shutdown()
