# -*- coding: utf-8 -*-
from collections import deque
import time
import re
import os
from webbrowser import open_new_tab

from bs4 import BeautifulSoup, element
import requests
import reqWrapper
import vlivepy
import vlivepy.board
import vlivepy.parser
import vlivepy.variables
from vlivepy.parser import format_epoch
from prompt_toolkit import (
    PromptSession,
)
from prompt_toolkit import Application
from prompt_toolkit.shortcuts import (
    set_title,
    message_dialog,
    input_dialog,
    button_dialog,
    progress_dialog,
    radiolist_dialog,
    checkboxlist_dialog,
    clear,
)
import pyperclip

__version__ = "0.3.1"

set_title("VLIVE-BACKUP-BOT")
ptk_session = PromptSession()
vlivepy.variables.override_gcc = "US"


class LocaleTemplate:
    checking_update = "Checking for updates"
    done_shutdown = "All operation has been completed.\nPress ENTER to exit the program."
    exit_btn = "Exit"
    download_end_title = "Download Complete"
    download_end_message = "Download has been complete.\nDo you want to download another board?"
    error = "Error"
    yn_yes = "Yes"
    yn_no = "No"
    oc_ok = "OK"
    oc_cancel = "Cancel"
    update = "Update"
    update_title = "Update Found"
    update_text = "New version has been found.\nDo you want to download update?\n\n[CAUTION] Do not exit the program " \
                  "during update "
    update_downloading = "Download patch files"
    update_validating = "Validate patch files"
    update_patching = "Apply patch files"
    update_cleanup = "Clean up patch files"
    update_success = "Update success!"
    update_success_text = "The update is complete.\nPlease re-launch the program to use new version"
    update_failed = "Update failed"
    update_failed_text = "Failed to update the program\nPlease download new version of the program from github."
    license_title = "License"
    license_text = 'This program is free software, licensed under GPL-3.0 License.\n' \
                   "Full text of the license can be found in github repo.\n\n" \
                   "The user is responsible for any problems with using the program.\n" \
                   "Sharing saved items with others may be a copyright infringement"
    license_accept = "Accept"
    license_decline = "Decline"
    select_mode_title = "Select Mode"
    select_mode_text = "Select download mode\n\n" \
                       "Simple: Download all items on the board\n" \
                       "Advanced: Manually select download items and settings"
    select_mode_simple = "Simple"
    select_mode_advanced = "Advanced"
    dn_url_title = "Enter Download URL"
    dn_url_text = "Enter the board URL to download.\n(e.g., https://www.vlive.tv/channel/B039DF/board/6118 )"
    dn_url_paste = "Paste"
    dn_url_verify_title = "Verify URL"
    dn_url_verify_text = "Is this entered information correct?\n\nChannel: %s\nBoard: %s"  # Must have 2 '%s'
    dn_url_verify_error = "Invalid board URL"
    membership_yn_title = "Select Membership"
    membership_yn_text = "Is it membership-only contents?"
    membership_login_title = "Log-In"
    membership_login_load_session = "Saved login session exists.\nDo you want to use the session?\n\nUser info: %s"
    membership_login_email = "Please enter vlive email account"
    membership_login_pw = "Please enter vlive email account password."
    membership_login_cancel = "Are you sure you want to cancel the login?"
    login_connecting = "Attempt to login."
    login_failed = "Failed to login."
    login_create_session = "Create a UserSession file."
    login_successful = "Login successful."
    login_error_dialog = "Login failed.\nPlease check your vlive account information."
    opt_title = "Download Options"
    opt_ovp_dialog = "Do you want to download official videos?"
    opt_post_dialog = "Do you want to download posts?"
    opt_amount_dialog = "Please enter the amount of items to load.\n" \
                        "The items will be loaded from the latest one\n\n" \
                        "(Enter 0 to load all items.)"
    opt_reset_btn = "Reset"
    opt_error_invalid_value = "Invalid value"
    opt_name_dialog = "Save downloaded files as original post title?\n\n" \
                      "YES to set filename as post title.\n" \
                      "NO to set filename as post-id."
    load_pages = "Load page #%03d"
    load_items_title = "Load items"
    load_items_text = "Load items from board... \nThis will takes a time"
    opt_load_history = "Download history has been found.\nDo you want to exclude downloaded items?"
    post_list_sorting = "Sorting list..."
    post_list_prepare = "Prepare list."
    post_list_title = "Select items"
    post_list_text = "Select items to download"
    post_list_select_all = "Select All"
    dn_done = "Done"
    dn_failed = "Failed"
    dn_downloading = "Downloading......."
    dn_star_comment = "Star Comments"
    dn_progress_tile = "Download in progress"
    dn_progress_text = "Now download the vlive posts\n\n" \
                       "Downloaded history is automatically saved, \n" \
                       "even if you exit the program during download."
    permission_error = "You don't have permission to load this board"
    no_post_error = "There are no posts to select."


class LocaleKo(LocaleTemplate):
    checking_update = "업데이트 확인중..."
    done_shutdown = "모든 작업이 완료되었습니다.\n엔터키를 누르면 프로그램을 종료합니다."
    exit_btn = "종료"
    download_end_title = "다운로드 완료"
    download_end_message = "다운로드가 완료되었습니다.\n다른 게시판을 추가로 다운로드 하겠습니까?"
    error = "오류"
    yn_yes = "예"
    yn_no = "아니오"
    oc_ok = "확인"
    oc_cancel = "취소"
    update = "업데이트"
    update_title = "업데이트 알림"
    update_text = "새로운 업데이트가 발견되었습니다\n업데이트를 다운로드 하시겠습니까?\n\n" \
                  "[주의] 업데이트 중에는 프로그램을 종료하지 마세요."
    update_downloading = "업데이트 파일을 받아옵니다."
    update_validating = "업데이트 파일을 확인합니다."
    update_patching = "업데이트를 적용합니다."
    update_cleanup = "받은 파일을 정리합니다."
    update_success = "업데이트 성공!"
    update_success_text = "업데이트가 완료되었습니다.\n적용을 위해 프로그램을 재실행 해주세요."
    update_failed = "업데이트 실패"
    update_failed_text = "업데이트에 실패했습니다.\n수동으로 업데이트를 진행해 주세요."
    license_title = "라이센스"
    license_text = '이 소프트웨어는 자유 소프트웨어로, GPL-3.0 License 를 따릅니다.\n' \
                   "라이센스의 전문은 깃헙 레포에서 확인할 수 있습니다.\n\n" \
                   "이 소프트웨어의 이용으로 인한 책임은 사용자에게 있으며,\n" \
                   "저장한 영상을 타인에게 공유할 시 저작권법 위반에 해당될 수 있습니다."
    license_accept = "동의"
    license_decline = "거부"
    select_mode_title = "모드 선택"
    select_mode_text = "다운로드 모드를 선택하세요\n\n" \
                       "간편모드: 게시판 페이지의 모든 게시물을 저장합니다.\n" \
                       "고급모드: 다운로드 옵션을 지정합니다."
    select_mode_simple = "간편모드"
    select_mode_advanced = "고급모드"
    dn_url_title = "다운로드 URL 입력"
    dn_url_text = "다운받을 게시판의 주소를 입력하세요.\n(예: https://www.vlive.tv/channel/B039DF/board/6118 )"
    dn_url_paste = "붙여넣기"
    dn_url_verify_title = "URL 확인"
    dn_url_verify_text = '입력하신 정보가 맞습니까?\n\n채널: %s\n게시판: %s'  # Must have 2 '%s'
    dn_url_verify_error = "유효하지 않은 URL 입니다!"
    membership_yn_title = "멤버십 선택"
    membership_yn_text = "멤버십(팬십) 컨텐츠입니까?"
    membership_login_title = "로그인"
    membership_login_load_session = "로그인 내역이 존재합니다.\n기존 세션을 이용하시겠습니까?\n\n계정정보: %s"
    membership_login_email = "VLIVE 이메일 아이디를 입력하세요."
    membership_login_pw = "VLIVE 비밀번호를 입력하세요."
    membership_login_cancel = "로그인을 취소하시겠습니까?"
    login_connecting = "로그인 시도중입니다."
    login_failed = "로그인에 실패했습니다."
    login_create_session = "세션파일을 생성합니다."
    login_successful = "로그인에 성공했습니다."
    login_error_dialog = "로그인에 실패했습니다.\n계정 정보를 확인 해 주세요."
    opt_title = "옵션"
    opt_ovp_dialog = "공식 비디오를 다운로드 하시겠습니까?"
    opt_post_dialog = "포스트를 다운로드 하시겠습니까?"
    opt_amount_dialog = "게시판에서 로드할 게시물 개수를 입력 해 주세요.\n" \
                        "게시물은 최신순으로 가져옵니다.\n\n" \
                        "(전체 다운로드 시 0 입력)"
    opt_reset_btn = "재설정"
    opt_error_invalid_value = "유효하지 않은 값입니다."
    opt_name_dialog = "저장되는 파일명으로 브이라이브 원본의 제목을 사용하시겠습니까?\n\n" \
                      "예: 포스트 제목으로 저장합니다.\n" \
                      "아니오: 게시물 번호로 저장합니다."
    load_pages = "%03d 페이지를 로드합니다"
    load_items_title = "게시물 로드중..."
    load_items_text = "게시물 리스트롤 로드합니다.\n 이 작업에는 시간이 걸립니다."
    opt_load_history = "게시판을 다운로드한 내역이 있습니다.\n기존에 받은 파일을 제외하시겠습니까?"
    post_list_sorting = "목록을 읽는 중입니다..."
    post_list_prepare = "목록을 준비합니다."
    post_list_title = "게시물 선택"
    post_list_text = "다운로드 할 게시물을 선택하세요."
    post_list_select_all = "전체선택"
    dn_done = "성공"
    dn_failed = "실패"
    dn_downloading = "다운로드를 진행합니다......."
    dn_star_comment = "스타 댓글"
    dn_progress_tile = "다운로드 진행중"
    dn_progress_text = "VLIVE 게시판 백업이 진행중입니다.\n" \
                       "중간에 종료하여도 진행상황은 저장됩니다."
    permission_error = "이 게시판을 로드할 권한이 없습니다."
    no_post_error = "선택할 포스트가 없습니다."


class LocaleEn(LocaleTemplate):
    pass


i18n: LocaleTemplate = LocaleTemplate()


def select_lang():
    global i18n
    dialog_result = radiolist_dialog(
        title="Language",
        values=[
            (LocaleKo(), "한국어"),
            (LocaleEn(), "English"),
        ]
    ).run()
    if dialog_result is None:
        exit()
    else:
        i18n = dialog_result


def dialog_splash():
    has_update = False
    zipball = None
    info_url = None

    def callback_fn(report_progress, report_log):
        nonlocal has_update
        nonlocal zipball
        nonlocal info_url
        report_progress(0)
        content = rf"""

██╗   ██╗██╗     ██╗██╗   ██╗███████╗            
██║   ██║██║     ██║██║   ██║██╔════╝            
██║   ██║██║     ██║██║   ██║█████╗              
╚██╗ ██╔╝██║     ██║╚██╗ ██╔╝██╔══╝              
 ╚████╔╝ ███████╗██║ ╚████╔╝ ███████╗            
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝  ╚══════╝            

██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗
██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝
██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝ 
██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║     
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     

██████╗  ██████╗ ████████╗                       
██╔══██╗██╔═══██╗╚══██╔══╝                       
██████╔╝██║   ██║   ██║                          
██╔══██╗██║   ██║   ██║                          
██████╔╝╚██████╔╝   ██║     VER {__version__}                 
╚═════╝  ╚═════╝    ╚═╝     by @box_archived                
"""
        report_log(content)

        time.sleep(1)

        report_progress(50)
        report_log(f"\n {i18n.checking_update}")
        sr = reqWrapper.get("https://api.github.com/repos/box-archived/vlive-backup-bot/releases/latest", status=[200])
        if sr.success:
            release_data = sr.response.json()
            latest = release_data['tag_name'][1:]
            if __version__ != latest:
                has_update = True
                zipball = release_data["zipball_url"]
                info_url = release_data["html_url"]

        time.sleep(1)
        report_progress(100)

    progress_dialog(
        title="VLIVE-BACKUP-BOT",
        text="",
        run_callback=callback_fn,
    ).run()

    return has_update, zipball, info_url


def tool_format_creator(max_int):
    max_len = len(str(max_int))
    return "%%%dd/%%%dd" % (max_len, max_len)


def tool_remove_emoji(plain_text, sub, allow_emoji=False):
    uni_emoji = ""
    if allow_emoji:
        uni_emoji = "\U0001F1E0-\U0001FAFF\U00002702-\U000027B0"
    emoji_regex = re.compile(
        r"([^"
        "\u0020-\u007e"  # 기본 문자
        # "\u0080-\u024f"  # 라틴 기본
        "\u1100-\u11ff"  # 한글 자모
        "\u3131-\u318f"  # 호환용 한글
        "\uac00-\ud7a3"  # 한글 음절
        "\u3040-\u309f"  # 히라가나
        "\u30a0-\u30ff"  # 가타카나
        "\u2e80-\u2eff"  # CJK 부수보충
        "\u4e00-\u9fbf"  # CJK 통합 한자
        "\u3400-\u4dbf"  # CJK 통합 한자 확장 - A
        f"{uni_emoji}"
        "])"
    )

    if allow_emoji:
        return emoji_regex.sub(sub, plain_text)
    else:
        return emoji_regex.sub(sub, plain_text).encode("cp949", "ignore").decode("cp949")


def tool_clip_text_length(plain_text, length):
    if len(plain_text) > length:
        plain_text = plain_text[:length - 3] + ".._"

    return plain_text


def tool_regex_window_name(plain_text):
    # remove front space
    regex_front_space = re.compile(r"^(\s+)")
    regex_window_name = re.compile(r'[<>:"\\/|?*~%]')

    safe_name = regex_window_name.sub("_", regex_front_space.sub("", plain_text))

    return safe_name


def tool_calc_percent(full, now):
    res = now / full * 100
    if res >= 100:
        res -= 1
    return res


def tool_parse_url(url: str):
    # pa`rse extension
    ext_split = url.split("?")[0].rsplit(".", 1)

    # parse server filename
    filename = ext_split[0].rsplit("/", 1)[-1]

    return ext_split[-1], filename


def tool_max_len_filename(location, filename, ext):
    avail_length = 255 - len(location) - len(ext) - 2
    return tool_clip_text_length(filename, avail_length)


def tool_download_file(url: str, location: str, filename: str = None, is_sub: bool = False):
    headers = {**vlivepy.variables.HeaderCommon}
    filename = tool_regex_window_name(filename)
    ext, name = tool_parse_url(url)

    if filename is None:
        filename = name

    alter = name

    def do_download():
        nonlocal url, location, filename, alter, headers, ext, is_sub

        filename = tool_max_len_filename(location, filename, ext)

        with requests.get(url, stream=True, headers=headers) as r:
            r.raise_for_status()
            with open(f"{location}/{filename}.{ext}", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        if is_sub:
            os.makedirs(f"{location.replace('/vtt-', '/srt-')}", exist_ok=True)
            tool_vtt_to_srt_converter(f"{location}/{filename}.{ext}")

        return True

    # create dir
    os.makedirs(location, exist_ok=True)
    try:
        return do_download()
    except OSError:
        filename = alter
        try:
            do_download()
        except:
            return False
    except:
        return False


def proc_redundant_download(url: str, location: str, filename: str = None, is_sub: bool = False):
    for item in range(5):
        if tool_download_file(
                url=url,
                location=location,
                filename=tool_remove_emoji(filename, "_", allow_emoji=True),
                is_sub=is_sub
        ):
            break
    else:
        return False

    return True


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

CONTENT-TYPE: {content_type}
TITLE: {title}
AUTHOR: {author_nickname}
TIME: {format_epoch(created_at, "%Y-%m-%d %H:%M:%S")}
ORIGIN: https://www.vlive.tv/post/{post_id}
BOT-SAVED: {vlivepy.parser.format_epoch(time.time(), "%Y-%m-%d %H:%M:%S")}

================================

""")
    current_date = "[%s]" % format_epoch(created_at, "%Y-%m-%d")
    # write
    with open(f"{location}/{current_date} {post_id}-info.txt", encoding="utf8", mode="w") as f:
        f.write(meta_text)


def tool_captions_parser(title: str, play_info: dict) -> list:
    result = []
    captions = play_info.get("captions", dict()).get("list", list())
    for c_item in captions:
        c_item: dict
        filename = title

        subtype = c_item.get("type", 'UNKNOWN')

        if subtype == "fan":
            filename += ".fanSub."
        elif subtype == "cp":
            filename += ".official."
        elif subtype == "auto":
            filename += ".autoSub."
        else:
            filename += f".{subtype}."

        filename += c_item.get('locale', 'UNKNOWN')

        result.append((c_item.get('source'), filename))

    return result


def tool_vtt_to_srt_converter(file):
    with open(file, "r", encoding="utf8") as f:
        vtt_text = f.read()

    srt_text = "1" + vtt_text.split("1", 1)[-1]
    srt_text = re.sub("(?<=\\d{2}:\\d{2}:\\d{2}).(?=\\d{3})", ",", srt_text)

    with open(f"{file.replace('/vtt-', '/srt-').rsplit('vtt', 1)[0]}srt", "w", encoding="utf8") as f:
        f.write(srt_text)


def shutdown():
    result = button_dialog(
        title='VLIVE-BACKUP-BOT',
        text=i18n.done_shutdown,
        buttons=[
            (i18n.exit_btn, True),
        ],
    ).run()
    if result:
        # clear()
        print("VLIVE-BACKUP-BOT by @box_archived")
        print()
        exit()


def dialog_error_message(text):
    message_dialog(
        title=i18n.error,
        text=text,
    ).run()


def dialog_yn(title, text):
    return button_dialog(
        title=title,
        text=text,
        buttons=[
            (i18n.yn_yes, True),
            (i18n.yn_no, False),
        ],
    ).run()


def dialog_download_end():
    return dialog_yn(i18n.download_end_title, i18n.download_end_message)


def query_update(result: tuple):
    if not result[0]:
        return False

    update = dialog_yn(
        title=i18n.update_title,
        text=i18n.update_text
    )

    update_success = False

    def callback_fn(report_progress, report_log):
        nonlocal result
        nonlocal update_success
        report_progress(0)
        report_log(f"{i18n.update_downloading}\n")
        sr = reqWrapper.get(result[1])
        if sr.success:
            try:
                # Overwrite path
                if os.path.isdir("_update"):
                    from shutil import rmtree
                    rmtree("_update")
                os.makedirs("_update", exist_ok=True)

                # Write update zip
                with open("_update/data.zip", "wb") as f:
                    f.write(sr.response.content)

                report_progress(35)
                report_log(f"{i18n.update_validating}\n")
                # extract
                from zipfile import ZipFile
                with ZipFile("_update/data.zip") as f:
                    f.extractall("_update")

                # find
                from glob import glob
                files = glob("_update/*")
                target = ''
                for item in files:
                    if "data.zip" not in item:
                        target = item

                report_progress(50)
                report_log(f"{i18n.update_patching}\n")
                # write
                for item in glob(f"{target}/*.*"):
                    filename = item.replace("\\", "/").rsplit("/", 1)[-1]

                    with open(item, "rb") as fi:
                        with open(filename, "wb") as fo:
                            fo.write(fi.read())

                report_progress(90)
                report_log(f"{i18n.update_cleanup}\n")
                # Clean up path
                if os.path.isdir("_update"):
                    from shutil import rmtree
                    rmtree("_update")

                    update_success = True
                report_progress(100)
            except:
                report_progress(100)
        report_progress(100)

    if update:
        progress_dialog(i18n.update, "", callback_fn).run()
        if update_success:
            message_dialog(i18n.update_success, i18n.update_success_text).run()
            exit()
            return True
        else:
            message_dialog(i18n.update_failed, i18n.update_failed_text).run()
            open_new_tab(result[2])
            return False

    return False


def query_license_agreement():
    if not button_dialog(
            title=i18n.license_title,
            text=i18n.license_text,
            buttons=[
                (i18n.license_accept, True),
                (i18n.license_decline, False),
            ],
    ).run():
        shutdown()


def query_workflow_select():
    return button_dialog(
        title=i18n.select_mode_title,
        text=i18n.select_mode_text,
        buttons=[
            (i18n.select_mode_simple, True),
            (i18n.select_mode_advanced, False),
        ],
    ).run()


def query_download_url():
    url_rule = re.compile(r'((?<=vlive.tv/channel/).+(?=/board/))/board/(\d+)')
    target_url = ""
    while True:
        target_url = input_dialog(
            title=i18n.dn_url_title,
            text=i18n.dn_url_text,
            ok_text=i18n.oc_ok,
            cancel_text=i18n.dn_url_paste,
        ).run()
        if target_url is None:
            try:
                target_url = pyperclip.paste()
            except:
                target_url = ""

        regex_result = url_rule.findall(target_url)
        if len(regex_result) == 1:
            if dialog_yn(
                    title=i18n.dn_url_verify_title,
                    text=i18n.dn_url_verify_text % (regex_result[0][0], regex_result[0][1]),
            ):
                return regex_result[0]
        else:
            dialog_error_message(i18n.dn_url_verify_error)


def query_membership():
    membership_yn = dialog_yn(
        title=i18n.membership_yn_title,
        text=i18n.membership_yn_text,
    )

    if membership_yn:
        # Session exist check
        if os.path.isfile("cache/vlive-backup-bot.session"):
            with open("cache/vlive-backup-bot.session", "rb") as f:
                loaded_email = vlivepy.loadSession(f).email
            if dialog_yn(i18n.membership_login_title, i18n.membership_login_load_session % loaded_email):
                return True

        # Login
        while True:

            user_email = ""
            while len(user_email) == 0:
                user_email = input_dialog(
                    title=i18n.membership_login_title,
                    text=i18n.membership_login_email,
                    ok_text=i18n.oc_ok,
                    cancel_text=i18n.oc_cancel,
                ).run()
                if user_email is None:
                    if dialog_yn(i18n.membership_login_title, i18n.membership_login_cancel):
                        return False
                    else:
                        user_email = ""
                        continue

            # password
            user_pwd = ""
            while len(user_pwd) == 0:
                user_pwd = input_dialog(
                    title=i18n.membership_login_title,
                    text=i18n.membership_login_pw,
                    ok_text=i18n.oc_ok,
                    cancel_text=i18n.oc_cancel,
                    password=True
                ).run()
                if user_pwd is None:
                    if dialog_yn(i18n.membership_login_title, i18n.membership_login_cancel):
                        return False
                    else:
                        user_pwd = ""
                        continue

            login_callback_result = False

            # try login
            def login_try(report_progress, report_log):
                nonlocal login_callback_result
                report_log(f"{i18n.login_connecting}\n")
                report_progress(50)
                try:
                    sess = vlivepy.UserSession(user_email, user_pwd)
                except vlivepy.exception.APISignInFailedError:
                    # break
                    report_log(f"{i18n.login_failed}\n")
                    login_callback_result = False
                    report_progress(100)
                else:
                    report_progress(75)
                    # dump session
                    report_log(f"{i18n.login_create_session}\n")
                    with open("cache/vlive-backup-bot.session", "wb") as f_sess:
                        vlivepy.dumpSession(sess, f_sess)

                    # break
                    report_log(f"{i18n.login_successful}\n")
                    time.sleep(1)
                    login_callback_result = True
                    report_progress(100)

            progress_dialog(i18n.membership_login_title, None, login_try).run()
            if login_callback_result:
                return True
            else:
                dialog_error_message(i18n.login_error_dialog)

    return membership_yn


def query_options():
    opt_ovp = dialog_yn(i18n.opt_title, i18n.opt_ovp_dialog)
    opt_post = dialog_yn(i18n.opt_title, i18n.opt_post_dialog)
    opt_amount = None
    while opt_amount is None:
        opt_amount = input_dialog(
            title=i18n.opt_title,
            text=i18n.opt_amount_dialog,
            ok_text=i18n.oc_ok,
            cancel_text=i18n.opt_reset_btn,
        ).run()
        try:
            opt_amount = int(opt_amount)
        except ValueError:
            dialog_error_message(i18n.opt_error_invalid_value)
            opt_amount = None
            continue
        except TypeError:
            opt_amount = None
            continue
        else:
            return opt_ovp, opt_post, opt_amount


def query_realname():
    return dialog_yn(
        title=i18n.opt_title,
        text=i18n.opt_name_dialog
    )


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
            with open("cache/vlive-backup-bot.session", "rb") as f:
                kwargs.update({"session": vlivepy.loadSession(f)})

        it = vlivepy.board.getBoardPostsIter(target_channel, target_board, **kwargs)
        cnt = 0
        page = 1
        try:
            for item in it:
                if cnt == 0:
                    report_log(f"{i18n.load_pages % page}\n")
                    page += 1

                cnt += 1

                post_list.append(item)

                if cnt == 20:
                    cnt = 0
                if len(post_list) == target_amount:
                    break

            report_progress(100)
        except vlivepy.exception.APIServerResponseError:
            post_list = None
            report_progress(100)

    progress_dialog(
        title=i18n.load_items_title,
        text=i18n.load_items_text,
        run_callback=callback_fn
    ).run()

    return post_list


def query_use_cache(channel_id, board_id, post_list: deque):
    cache_file_name = f"cache/{channel_id}_{board_id}.txt"
    if os.path.isfile(cache_file_name):
        opt_cache = dialog_yn(i18n.opt_title, i18n.opt_load_history)
        if opt_cache:
            with open(cache_file_name, "r") as f:
                cached_list = f.read().splitlines()
            new_list = deque()
            while post_list:
                item: vlivepy.board.BoardPostItem = post_list.popleft()
                if item.post_id not in cached_list:
                    new_list.append(item)
            return new_list
    return post_list


def query_post_select(post_list: deque, opt_ovp, opt_post):
    def item_parser(post_item: vlivepy.board.BoardPostItem):
        description = "[%s] %s" % (
            format_epoch(post_item.created_at, "%Y-%m-%d"),
            tool_clip_text_length(tool_remove_emoji(post_item.title, "?"), 50)
        )
        return post_item, description

    filtered_list = list()
    check_dialog: None = None
    check_result = None

    def parser_progress(report_progress, report_log):
        nonlocal filtered_list
        nonlocal post_list
        nonlocal check_dialog
        initial_len = len(post_list)
        cnt = 0

        report_log(f"{i18n.post_list_sorting}\n")
        while post_list:
            item: vlivepy.board.BoardPostItem = post_list.popleft()
            item_ovp = item.has_official_video
            if item_ovp and opt_ovp:
                filtered_list.append(item_parser(item))
            elif not item_ovp and opt_post:
                filtered_list.append(item_parser(item))

            cnt += 1
            report_progress(tool_calc_percent(initial_len, cnt))

        if len(filtered_list) != 0:
            report_log(i18n.post_list_prepare)
            check_dialog = checkboxlist_dialog(
                title=i18n.post_list_title,
                text=i18n.post_list_text,
                values=filtered_list,
                ok_text=i18n.oc_ok,
                cancel_text=i18n.post_list_select_all
            )
        report_progress(100)

    progress_dialog(i18n.post_list_title, None, parser_progress).run()

    if check_dialog is not None:
        check_dialog: Application
        check_result = check_dialog.run()
    if check_result is None:
        check_result = map(lambda x: x[0], filtered_list)

    return deque(check_result)


def proc_downloader(download_queue, channel_id, board_id, opt_realname):
    def callback_fn(report_progress, report_log):
        def report_fail(post_id):
            report_log(i18n.dn_failed)
            with open("failed.txt", encoding="utf8", mode="a") as f_report:
                f_report.write(f"https://www.vlive.tv/post/{post_id}\n")

        # set base dir
        channel_board_pair = f"{channel_id}_{board_id}"
        base_dir = f"downloaded/{channel_board_pair}"

        # set count of queue
        initial_length = len(download_queue)

        # download proc
        while download_queue:

            # report
            current_percent = tool_calc_percent(initial_length, initial_length - len(download_queue))
            report_progress(current_percent)
            current_target = download_queue.popleft()
            current_target: vlivepy.board.BoardPostItem
            log_format = f"\n(%4.01f%%%%)(%s) [%s] {i18n.dn_downloading}" % (
                current_percent, tool_format_creator(initial_length), current_target.post_id
            )
            report_log(log_format % (initial_length - len(download_queue), initial_length))

            current_date = "[%s]" % format_epoch(current_target.created_at, "%Y-%m-%d")

            current_location = "%s/%s %s" % (
                base_dir, current_date, current_target.post_id
            )

            if current_target.has_official_video:
                # type OfficialVideoPost

                try:
                    ovp = current_target.to_object()
                except:
                    report_fail(current_target.post_id)
                    continue

                # Pass when live
                if ovp.official_video_type != "VOD":
                    report_fail(current_target.post_id)
                    continue

                try:
                    ovv = ovp.official_video()
                except:
                    report_fail(current_target.post_id)
                    continue

                if ovv.vod_secure_status == "COMPLETE":
                    report_fail(current_target.post_id)
                    continue

                # Find max res source, captions
                try:
                    ovv_play_info = ovv.getVodPlayInfo()
                    max_source = vlivepy.parser.max_res_from_play_info(ovv_play_info)['source']
                except KeyError:
                    report_fail(current_target.post_id)
                    continue
                else:
                    if opt_realname:
                        ovp_filename = f"{current_date} {current_target.title}"
                    else:
                        ovp_filename = f"{current_date} {current_target.post_id}-video"
                    # download
                    captions = tool_captions_parser(ovp_filename, ovv_play_info)
                    if not proc_redundant_download(
                            url=max_source,
                            location=current_location,
                            filename=f"{ovp_filename}"
                    ):
                        report_fail(current_target.post_id)
                        continue
                    else:
                        for item in captions:
                            proc_redundant_download(
                                url=item[0],
                                location=f"{current_location}/vtt-subs",
                                filename=f"{item[1]}",
                                is_sub=True,
                            )
                        report_log(i18n.dn_done)
            else:
                # type Post
                post = current_target.to_object()

                html = post.formatted_body()

                soup = BeautifulSoup(html, 'html.parser')
                imgs = soup.find_all("img")
                img_cnt = 0

                # download image
                for item in imgs:
                    img_cnt += 1

                    item: element
                    dnld_image_name = "%s %s-img-%02d" % (current_date, current_target.post_id, img_cnt)
                    if not proc_redundant_download(
                            url=item['src'],
                            location=current_location,
                            filename=dnld_image_name
                    ):
                        report_fail(current_target.post_id)
                        continue
                    item['src'] = f"{dnld_image_name}.{tool_parse_url(item['src'])[0]}"

                # download video
                videos = soup.find_all("video")
                video_cnt = 0
                for item in videos:
                    item: element
                    video_cnt += 1

                    # Poster get
                    dnld_poster_name = "%s %s-poster-%02d" % (current_date, current_target.post_id, video_cnt)
                    if not proc_redundant_download(
                            url=item['poster'],
                            location=current_location,
                            filename=dnld_poster_name
                    ):
                        report_fail(current_target.post_id)
                        continue
                    item['poster'] = f"{dnld_poster_name}.{tool_parse_url(item['poster'])[0]}"

                    # Video get
                    dnld_video_name = "%s %s-video-%02d" % (current_date, current_target.post_id, video_cnt)
                    if not proc_redundant_download(
                            url=item['src'],
                            location=current_location,
                            filename=dnld_video_name
                    ):
                        report_fail(current_target.post_id)
                        continue
                    item['src'] = f"{dnld_video_name}.{tool_parse_url(item['src'])[0]}"

                # Get star-comment
                comment_html = f"""\n<div style="padding-top:5px"><h3>{i18n.dn_star_comment}</h3></div>"""

                for comment_item in post.getPostStarCommentsIter():
                    comment_html += '<div style="padding-top:5px;width:720px;border-top:1px solid #f2f2f2;border-bottom:1px solid #f2f2f2">'
                    comment_html += '<div style="margin: 15px 0 0 15px">'
                    comment_html += f'<span style="font-weight:700; font-size:13px; margin-right:10px">{comment_item.author_nickname}</span>'
                    comment_html += f'<span style="font-size:12px; color:#777;">{format_epoch(comment_item.created_at, "%Y-%m-%d %H:%M:%S")}</span>'
                    comment_html += '</div>'
                    comment_html += f'<div style="margin: 0 0 15px 15px; font-size:14px">{comment_item.body}</div>'
                    comment_html += '</div>'

                os.makedirs(current_location, exist_ok=True)
                post_filename = f"{current_location}/{current_date} {current_target.post_id}-post.html"
                if opt_realname:
                    filename_safe_title = tool_regex_window_name(tool_remove_emoji(current_target.title, "_", True))
                    max_len_name = tool_max_len_filename(
                        current_location,
                        f"{current_date} {filename_safe_title}",
                        "html"
                    )
                    post_real_name = f"{current_location}/{max_len_name}.html"
                    try:
                        open(post_real_name, "w").close()
                    except OSError:
                        pass
                    else:
                        post_filename = post_real_name

                with open(post_filename, encoding="utf8", mode="w") as f:
                    f.write(str(soup))
                    f.write(comment_html)

                report_log(i18n.dn_done)

            # Write meta
            tool_write_meta(
                location=current_location,
                post_id=current_target.post_id,
                title=current_target.title,
                content_type=current_target.content_type,
                author_nickname=current_target.author_nickname,
                created_at=current_target.created_at,
            )
            with open(f"cache/{channel_board_pair}.txt", encoding="utf8", mode="a") as f:
                f.write(f"{current_target.post_id}\n")
            time.sleep(0.2)

        # Download End
        report_progress(100)

    progress_dialog(
        title=i18n.dn_progress_tile,
        text=i18n.dn_progress_text,
        run_callback=callback_fn
    ).run()


def main():
    os.makedirs("downloaded", exist_ok=True)
    os.makedirs("cache", exist_ok=True)
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
    if post_list is None:
        dialog_error_message(i18n.permission_error)
        return dialog_download_end()

    post_list = query_use_cache(target_channel, target_board, post_list)

    # Post select dialog on adv-mode
    if not easy_mode:
        post_list = query_post_select(post_list, opt_ovp, opt_post)

    if len(post_list) == 0:
        message_dialog(i18n.post_list_title, i18n.no_post_error).run()

    else:
        opt_realname = query_realname()

        # Downloader Query
        proc_downloader(post_list, target_channel, target_board, opt_realname)

    return dialog_download_end()


if __name__ == '__main__':
    select_lang()
    query_update(dialog_splash())

    query_license_agreement()

    while True:
        if main():
            continue
        else:
            shutdown()
