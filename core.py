from collections import deque
import time
import re
import os

import requests
import vlivepy
import vlivepy.board
import vlivepy.parser
import vlivepy.variables
from vlivepy.parser import format_epoch
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import (
    message_dialog,
    input_dialog,
    button_dialog,
    progress_dialog,
    checkboxlist_dialog,
    clear,
)
import pyclip

ptk_session = PromptSession()
vlivepy.variables.override_gcc = "US"


def tool_format_creator(max_int):
    max_len = len(str(max_int))
    return "%%%dd/%%%dd" % (max_len, max_len)


def tool_remove_emoji(plain_text):
    emoji_regex = re.compile(
        r"(["
        "\U0001F1E0-\U0001F1FF"
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "])"
    )
    return emoji_regex.sub("_", plain_text)


def tool_regex_window_name(plain_text):
    # remove front space
    regex_front_space = re.compile(r"^(\s+)")
    regex_window_name = re.compile(r'[<>:"\\/|?*~]')

    safe_name = regex_window_name.sub("_", regex_front_space.sub("", plain_text))

    if len(safe_name) > 41:
        safe_name = safe_name[:38] + ".._"

    return safe_name


def tool_calc_percent(full, now):
    res = now / full * 100
    if res >= 100:
        res -= 1
    return res


def tool_download_file(url: str, location: str, filename: str = None):
    # parse extension
    ext_split = url.split("?")[0].rsplit(".", 1)

    # parse server filename
    if filename is None:
        filename = ext_split[0].rsplit("/", 1)[-1]

    # create dir
    os.makedirs(location, exist_ok=True)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"{location}/{filename}.{ext_split[-1]}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def tool_write_meta(
        location: str,
        post_id: str,
        title: str,
        content_type: str,
        author_nickname: str,
        created_at: float,
):

    # create dir
    os.makedirs(location, exist_ok=True)

    # format
    meta_text = (
        f"""========VLIVE-BACKUP-BOT========
TITLE: {title}
CONTENT-TYPE: {content_type}
AUTHOR: {author_nickname}
TIME: {vlivepy.parser.format_epoch(created_at, "%Y-%m-%d %H:%M:%S")}
BOT-SAVED: {vlivepy.parser.format_epoch(time.time(), "%Y-%m-%d %H:%M:%S")}
ORIGIN: https://www.vlive.tv/post/{post_id}

========VLIVE-BACKUP-BOT========

""")

    # write
    with open(f"{location}/[{post_id}] info.txt", encoding="utf8", mode="w") as f:
        f.write(meta_text)


def shutdown():
    result = button_dialog(
        title='VLIVE-BACKUP-BOT',
        text='모든 작업이 완료되었습니다\n엔터키를 누르면 프로그램을 종료합니다.',
        buttons=[
            ('종료', True),
        ],
    ).run()
    if result:
        # clear()
        print("VLIVE-BACKUP-BOT by @box_archived")
        exit()


def dialog_error_message(text):
    message_dialog(
        title="오류",
        text=text,
    ).run()


def dialog_yn(title, text):
    return button_dialog(
        title=title,
        text=text,
        buttons=[
            ('예', True),
            ('아니요', False),
        ],
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
    ).run():
        shutdown()


def query_workflow_select():
    return button_dialog(
        title='모드 선택',
        text="다운로드 모드를 선택하세요\n\n간편모드: 게시판 페이지의 모든 게시물을 저장합니다.\n고급모드: 다운로드 옵션을 지정합니다.",
        buttons=[
            ('간편모드', True),
            ('고급모드', False),
        ],
    ).run()


def query_download_url():
    url_rule = re.compile(r'((?<=vlive.tv/channel/).+(?=/board/))/board/(\d+)')
    target_url = ""
    while True:
        target_url = input_dialog(
            title="다운로드 URL 입력",
            text="다운받을 게시판의 주소를 입력하세요.\n(예: https://www.vlive.tv/channel/B039DF/board/6118 )",
            ok_text="확인",
            cancel_text="붙여넣기",
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
            with open("vlive-backup-bot.session", "rb") as f:
                loaded_email = vlivepy.loadSession(f).email
            if dialog_yn("로그인", "로그인 내역이 존재합니다.\n 기존 세션을 이용하시겠습니까?\n\n 계정정보: %s" % loaded_email):
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
                    with open("vlive-backup-bot.session", "wb") as f_sess:
                        vlivepy.dumpSession(sess, f_sess)

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


def proc_load_post_list(target_channel, target_board, target_amount, membership):
    post_list = deque()

    def callback_fn(report_progress, report_log):
        report_progress(0)
        nonlocal post_list
        kwargs = {}
        # Add latest option when amount specified
        if target_amount != 0:
            kwargs.update({"latest": True})

        # Add session when membership
        if membership:
            with open("vlive-backup-bot.session", "rb") as f:
                kwargs.update({"session": vlivepy.loadSession(f)})

        it = vlivepy.board.getBoardPostsIter(target_channel, target_board, **kwargs)

        cnt = 0
        page = 1
        for item in it:
            if cnt == 0:
                report_log("%03d 페이지를 로드합니다\n" % page)
                page += 1

            cnt += 1

            post_list.append(item)

            if cnt == 20:
                cnt = 0
            if len(post_list) == target_amount:
                break

        report_progress(100)

    progress_dialog(
        title="게시물 로드중...",
        text="게시물 리스트롤 로드합니다.\n 이 작업에는 시간이 걸립니다.",
        run_callback=callback_fn
    ).run()

    return post_list


def query_post_select(post_list: deque, opt_ovp, opt_post):
    def item_parser(post_item: vlivepy.board.BoardPostItem):
        description = "[%s] https://www.vlive.tv/post/%s" % (
            format_epoch(post_item.created_at, "%Y-%m-%d"), post_item.post_id
        )
        return post_item, description

    filtered_list = list()
    check_dialog = None
    check_result = None

    def parser_progress(report_progress, report_log):
        nonlocal filtered_list
        nonlocal post_list
        nonlocal check_dialog
        initial_len = len(post_list)
        cnt = 0

        report_log("목록을 읽는 중입니다...\n")
        while post_list:
            item: vlivepy.board.BoardPostItem = post_list.popleft()
            item_ovp = item.has_official_video
            if item_ovp and opt_ovp:
                filtered_list.append(item_parser(item))
            elif not item_ovp and opt_post:
                filtered_list.append(item_parser(item))

            cnt += 1
            report_progress(tool_calc_percent(initial_len, cnt))
            if len(filtered_list) == 0:
                report_progress(100)

        report_log("목록을 준비합니다.")
        check_dialog = checkboxlist_dialog(
            title="게시물 선택",
            text="다운로드 할 게시물을 선택하세요.",
            values=filtered_list,
            ok_text="확인",
            cancel_text="전체선택"
        )
        report_progress(100)

    progress_dialog("게시물 선택", None, parser_progress).run()

    if check_dialog is not None:
        check_result = check_dialog.run()
    if check_result is None:
        check_result = map(lambda x: x[0], filtered_list)

    return deque(check_result)


def proc_downloader(download_queue, channel_id, board_id):
    def callback_fn(report_progress, report_log):
        # set base dir
        base_dir = f"downloaded/{channel_id}_{board_id}"

        # set count of queue
        initial_length = len(download_queue)

        # download proc
        while download_queue:

            # report
            current_percent = tool_calc_percent(initial_length, initial_length - len(download_queue))
            report_progress(current_percent)
            current_target = download_queue.popleft()
            current_target: vlivepy.board.BoardPostItem
            log_format = "\n(%4.01f%%%%)(%s) [%s] 다운로드를 진행합니다......." % (
                current_percent, tool_format_creator(initial_length), current_target.post_id
            )
            report_log(log_format % (initial_length - len(download_queue), initial_length))

            current_location = "%s/[%s] %s" % (
                base_dir, format_epoch(current_target.created_at, "%Y-%m-%d"), current_target.post_id
            )

            # type OfficialVideoPost
            if current_target.has_official_video:
                ovp = current_target.to_object()

                # continue when live
                if ovp.official_video_type != "VOD":
                    report_log("건너뜀 (VOD 아님)")
                    continue

                # Generate OfficialVideoVOD object
                ovv = ovp.official_video()

                # Find max res source
                try:
                    max_source = vlivepy.parser.max_res_from_play_info(ovv.getVodPlayInfo())['source']
                except KeyError:
                    report_log("실패")
                    continue
                else:
                    # download
                    try:
                        tool_download_file(
                            url=max_source,
                            location=current_location,
                            filename=tool_regex_window_name(ovv.title)
                        )
                    except:
                        report_log("실패")
                        continue
                    else:
                        report_log("성공")
            else:
                report_log("성공")

            # Write meta
            tool_write_meta(
                location=current_location,
                post_id=current_target.post_id,
                title=current_target.title,
                content_type=current_target.content_type,
                author_nickname=current_target.author_nickname,
                created_at=current_target.created_at,
            )
            time.sleep(0.3)

        # Download End
        report_progress(100)

    progress_dialog(
        title="VLIVE 다운로드",
        text="VLIVE 게시판 백업이 진행중입니다.\n이 작업은 시간이 걸립니다.",
        run_callback=callback_fn
    ).run()


def main():
    clear()
    easy_mode = query_workflow_select()

    target_channel, target_board = query_download_url()

    membership = query_membership()

    # Select option on adv-mode
    if easy_mode:
        opt_ovp = True
        opt_post = True
        opt_amount = 0

    else:
        opt_ovp, opt_post, opt_amount = query_options()

        if not opt_ovp and not opt_post:
            return dialog_download_end()

    post_list = proc_load_post_list(
        target_channel=target_channel,
        target_board=target_board,
        target_amount=opt_amount,
        membership=membership,
    )

    # Post select dialog on adv-mode
    if not easy_mode:
        post_list = query_post_select(post_list, opt_ovp, opt_post)

    # Downloader Query
    proc_downloader(post_list, target_channel, target_board)

    return dialog_download_end()


if __name__ == '__main__':
    query_license_agreement()

    while True:
        if main():
            continue
        else:
            shutdown()
