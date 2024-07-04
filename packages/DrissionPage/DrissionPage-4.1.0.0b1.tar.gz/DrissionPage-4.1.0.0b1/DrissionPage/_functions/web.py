# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from html import unescape
from os.path import sep
from pathlib import Path
from re import sub
from urllib.parse import urlparse, urljoin, urlunparse

from DataRecorder.tools import make_valid_name


def get_ele_txt(e):
    """获取元素内所有文本
    :param e: 元素对象
    :return: 元素内所有文本
    """
    # 前面无须换行的元素
    nowrap_list = ('br', 'sub', 'sup', 'em', 'strong', 'a', 'font', 'b', 'span', 's', 'i', 'del', 'ins', 'img', 'td',
                   'th', 'abbr', 'bdi', 'bdo', 'cite', 'code', 'data', 'dfn', 'kbd', 'mark', 'q', 'rp', 'rt', 'ruby',
                   'samp', 'small', 'time', 'u', 'var', 'wbr', 'button', 'slot', 'content')
    # 后面添加换行的元素
    wrap_after_list = ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'li', 'blockquote', 'header',
                       'footer', 'address' 'article', 'aside', 'main', 'nav', 'section', 'figcaption', 'summary')
    # 不获取文本的元素
    noText_list = ('script', 'style', 'video', 'audio', 'iframe', 'embed', 'noscript', 'canvas', 'template')
    # 用/t分隔的元素
    tab_list = ('td', 'th')

    if e.tag in noText_list:
        return e.raw_text

    def get_node_txt(ele, pre: bool = False):
        tag = ele.tag
        if tag == 'br':
            return [True]
        if not pre and tag == 'pre':
            pre = True

        str_list = []
        if tag in noText_list and not pre:  # 标签内的文本不返回
            return str_list

        nodes = ele.eles('xpath:./text() | *')
        prev_ele = ''
        for el in nodes:
            if isinstance(el, str):  # 字符节点
                if pre:
                    str_list.append(el)

                else:
                    if sub('[ \n\t\r]', '', el) != '':  # 字符除了回车和空格还有其它内容
                        txt = el
                        if not pre:
                            txt = txt.replace('\r\n', ' ').replace('\n', ' ').strip(' ')
                            txt = sub(r' {2,}', ' ', txt)
                        str_list.append(txt)

            else:  # 元素节点
                if el.tag not in nowrap_list and str_list and str_list[-1] != '\n':  # 元素间换行的情况
                    str_list.append('\n')
                if el.tag in tab_list and prev_ele in tab_list:  # 表格的行
                    str_list.append('\t')

                str_list.extend(get_node_txt(el, pre))
                prev_ele = el.tag

        if tag in wrap_after_list and str_list and str_list[-1] not in ('\n', True):  # 有些元素后面要添加回车
            str_list.append('\n')

        return str_list

    re_str = get_node_txt(e)
    if re_str and re_str[-1] == '\n':
        re_str.pop()
    re_str = ''.join([i if i is not True else '\n' for i in re_str])
    return format_html(re_str)


def format_html(text):
    """处理html编码字符
    :param text: html文本
    :return: 格式化后的html文本
    """
    return unescape(text).replace('\xa0', ' ') if text else text


def location_in_viewport(page, loc_x, loc_y):
    """判断给定的坐标是否在视口中          |n
    :param page: ChromePage对象
    :param loc_x: 页面绝对坐标x
    :param loc_y: 页面绝对坐标y
    :return: bool
    """
    js = f'''function(){{let x = {loc_x}; let y = {loc_y};
    const scrollLeft = document.documentElement.scrollLeft;
    const scrollTop = document.documentElement.scrollTop;
    const vWidth = document.documentElement.clientWidth;
    const vHeight = document.documentElement.clientHeight;
    if (x< scrollLeft || y < scrollTop || x > vWidth + scrollLeft || y > vHeight + scrollTop){{return false;}}
    return true;}}'''
    return page._run_js(js)


def offset_scroll(ele, offset_x, offset_y):
    """接收元素及偏移坐标，把坐标滚动到页面中间，返回该点在视口中的坐标
    有偏移量时以元素左上角坐标为基准，没有时以click_point为基准
    :param ele: 元素对象
    :param offset_x: 偏移量x
    :param offset_y: 偏移量y
    :return: 视口中的坐标
    """
    loc_x, loc_y = ele.rect.location
    cp_x, cp_y = ele.rect.click_point
    lx = loc_x + offset_x if offset_x else cp_x
    ly = loc_y + offset_y if offset_y else cp_y
    if not location_in_viewport(ele.owner, lx, ly):
        clientWidth = ele.owner._run_js('return document.body.clientWidth;')
        clientHeight = ele.owner._run_js('return document.body.clientHeight;')
        ele.owner.scroll.to_location(lx - clientWidth // 2, ly - clientHeight // 2)
    cl_x, cl_y = ele.rect.viewport_location
    ccp_x, ccp_y = ele.rect.viewport_click_point
    cx = cl_x + offset_x if offset_x else ccp_x
    cy = cl_y + offset_y if offset_y else ccp_y
    return cx, cy


def make_absolute_link(link, baseURI=None):
    """获取绝对url
    :param link: 超链接
    :param baseURI: 页面或iframe的url
    :return: 绝对链接
    """
    if not link:
        return link

    link = link.strip().replace('\\', '/')
    parsed = urlparse(link)._asdict()
    if baseURI:
        if link.startswith('./'):
            baseURI = baseURI[:baseURI.rfind('/') + 1]
        else:
            p = urlparse(baseURI)._asdict()
            baseURI = f'{p["scheme"]}://{p["netloc"]}'

    # 是相对路径，与页面url拼接并返回
    if not parsed['netloc']:
        return urljoin(baseURI, link) if baseURI else link

    # 是绝对路径但缺少协议，从页面url获取协议并修复
    if not parsed['scheme'] and baseURI:
        parsed['scheme'] = urlparse(baseURI).scheme
        parsed = tuple(v for v in parsed.values())
        return urlunparse(parsed)

    # 绝对路径且不缺协议，直接返回
    return link


def is_js_func(func):
    """检查文本是否js函数"""
    func = func.strip()
    if (func.startswith('function') or func.startswith('async ')) and func.endswith('}'):
        return True
    # elif '=>' in func:
    #     return True
    return False


def get_blob(page, url, as_bytes=True):
    """获取知道blob资源
    :param page: 资源所在页面对象
    :param url: 资源url
    :param as_bytes: 是否以字节形式返回
    :return: 资源内容
    """
    if not url.startswith('blob'):
        raise TypeError('该链接非blob类型。')
    js = """
       function fetchData(url) {
      return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();
        xhr.responseType = 'blob';
        xhr.onload = function() {
          let reader  = new FileReader();
          reader.onloadend = function(){resolve(reader.result);}
          reader.readAsDataURL(xhr.response);
        };
        xhr.open('GET', url, true);
        xhr.send();
      });
    }
"""
    try:
        result = page._run_js(js, url)
    except:
        raise RuntimeError('无法获取该资源。')
    if as_bytes:
        from base64 import b64decode
        return b64decode(result.split(',', 1)[-1])
    else:
        return result


def save_page(tab, path=None, name=None, as_pdf=False, kwargs=None):
    """把当前页面保存为文件，如果path和name参数都为None，只返回文本
    :param tab: Tab或Page对象
    :param path: 保存路径，为None且name不为None时保存在当前路径
    :param name: 文件名，为None且path不为None时用title属性值
    :param as_pdf: 为Ture保存为pdf，否则为mhtml且忽略kwargs参数
    :param kwargs: pdf生成参数
    :return: as_pdf为True时返回bytes，否则返回文件文本
    """
    if name:
        if name.endswith('.pdf'):
            name = name[:-4]
            as_pdf = True
        elif name.endswith('.mhtml'):
            name = name[:-6]
            as_pdf = False

    if path:
        path = Path(path)
        if path.suffix.lower() == '.mhtml':
            name = path.stem
            path = path.parent
            as_pdf = False
        elif path.suffix.lower() == '.pdf':
            name = path.stem
            path = path.parent
            as_pdf = True

    return get_pdf(tab, path, name, kwargs) if as_pdf else get_mhtml(tab, path, name)


def get_mhtml(page, path=None, name=None):
    """把当前页面保存为mhtml文件，如果path和name参数都为None，只返回mhtml文本
    :param page: 要保存的页面对象
    :param path: 保存路径，为None且name不为None时保存在当前路径
    :param name: 文件名，为None且path不为None时用title属性值
    :return: mhtml文本
    """
    r = page._run_cdp('Page.captureSnapshot')['data']
    if path is None and name is None:
        return r

    path = path or '.'
    Path(path).mkdir(parents=True, exist_ok=True)
    name = make_valid_name(name or page.title)
    with open(f'{path}{sep}{name}.mhtml', 'w', encoding='utf-8') as f:
        f.write(r.replace('\r\n', '\n'))
    return r


def get_pdf(page, path=None, name=None, kwargs=None):
    """把当前页面保存为pdf文件，如果path和name参数都为None，只返回字节
    :param page: 要保存的页面对象
    :param path: 保存路径，为None且name不为None时保存在当前路径
    :param name: 文件名，为None且path不为None时用title属性值
    :param kwargs: pdf生成参数
    :return: pdf文本
    """
    if not kwargs:
        kwargs = {}
    kwargs['transferMode'] = 'ReturnAsBase64'
    if 'printBackground' not in kwargs:
        kwargs['printBackground'] = True
    try:
        r = page._run_cdp('Page.printToPDF', **kwargs)['data']
    except:
        raise RuntimeError('保存失败，可能浏览器版本不支持。')
    from base64 import b64decode
    r = b64decode(r)
    if path is None and name is None:
        return r

    path = path or '.'
    Path(path).mkdir(parents=True, exist_ok=True)
    name = make_valid_name(name or page.title)
    with open(f'{path}{sep}{name}.pdf', 'wb') as f:
        f.write(r)
    return r


def tree(ele_or_page, text=False, show_js=False, show_css=False):
    """把页面或元素对象DOM结构打印出来
    :param ele_or_page: 页面或元素对象
    :param text: 是否打印文本，输入数字可指定打印文本长度上线
    :param show_js: 打印文本时是否包含<script>内文本，text参数为False时无效
    :param show_css: 打印文本时是否包含<style>内文本，text参数为False时无效
    :return: None
    """

    def _tree(obj, last_one=True, body=''):
        list_ele = obj.children()
        length = len(list_ele)
        body_unit = '    ' if last_one else '│   '
        tail = '├───'
        new_body = body + body_unit

        if length > 0:
            new_last_one = False
            for i in range(length):
                if i == length - 1:
                    tail = '└───'
                    new_last_one = True
                e = list_ele[i]

                attrs = ' '.join([f"{k}='{v}'" for k, v in e.attrs.items()])
                show_text = f'{new_body}{tail}<{e.tag} {attrs}>'.replace('\n', ' ')
                if text:
                    t = e('x:/text()')
                    if t:
                        t = t.replace('\n', ' ')
                        if (e.tag not in ('script', 'style') or (e.tag == 'script' and show_js)
                                or (e.tag == 'style' and show_css)):
                            if text is not True:
                                t = t[:text]
                            show_text = f'{show_text} {t}'
                print(show_text)

                _tree(e, new_last_one, new_body)

    ele = ele_or_page.s_ele()
    attrs = ' '.join([f"{k}='{v}'" for k, v in ele.attrs.items()])
    show_text = f'<{ele.tag} {attrs}>'.replace('\n', ' ')
    if text:
        t = ele('x:/text()')
        if t:
            t = t.replace('\n', ' ')
            if (ele.tag not in ('script', 'style') or (ele.tag == 'script' and show_js)
                    or (ele.tag == 'style' and show_css)):
                if text is not True:
                    t = t[:text]
                show_text = f'{show_text} {t}'
    print(show_text)
    _tree(ele)


def format_headers(txt):
    """从浏览器复制的文本生成dict格式headers，文本用换行分隔
    :param txt: 从浏览器复制的原始文本格式headers
    :return: dict格式headers
    """
    if not isinstance(txt, str):
        return txt
    headers = {}
    for header in txt.split('\n'):
        if header:
            name, value = header.split(': ', maxsplit=1)
            headers[name] = value
    return headers
