import json
import pandas as pd


def create_csv(json_blob, path_for_csv):
    # with open(json_blob.name) as file:
    #data = json.load(file)
    json_string = json_blob.download_as_string()
    data = json.loads(json_string)

    # dicts where Im gonna save the info for the csv, key = page-number, value = list of attributes
    dict_id = {}
    dict_text = {}
    dict_chars = {}
    dict_chars_height = {}
    dict_para_height = {}
    dict_para_width = {}
    dict_para_area = {}
    dict_para_pos1_x = {}
    dict_para_pos1_y = {}
    dict_para_pos2_x = {}
    dict_para_pos2_y = {}

    # loop file responses
    for response in data['responses']:
        page = response['context']['pageNumber']
        # lists for dicts
        #word_for_line = ''
        line = ''
        list_text = []
        list_chars_height = []
        list_para_height = []
        list_para_width = []
        list_para_area = []
        list_para_pos1_x = []
        list_para_pos1_y = []
        list_para_pos2_x = []
        list_para_pos2_y = []
        # to check if row changed
        row_changed = False
        first_row = True
        # list of coords
        x_list_para = []
        y_list_para = []
        x_list_word = []
        y_list_word = []
        for page_ in response['fullTextAnnotation']['pages']:
            for block in page_['blocks']:
                for para in block['paragraphs']:
                    if row_changed == True or first_row == True:
                        # clear old values
                        x_list_para.clear()
                        y_list_para.clear()
                        # save new values
                        for v in para['boundingBox']['normalizedVertices']:
                            x_list_para.append(v['x'])
                            y_list_para.append(v['y'])
                    for word in para['words']:
                        if row_changed == True or first_row == True:
                            # clear old values
                            x_list_word.clear()
                            y_list_word.clear()
                            # save new values
                            for v in word['boundingBox']['normalizedVertices']:
                                x_list_word.append(v['x'])
                                y_list_word.append(v['y'])
                        for symbol in word['symbols']:
                            # create word
                            #word_for_line += symbol['text']
                            line += symbol['text']
                            try:
                                if symbol['property'].get('detectedBreak'):
                                    if symbol['property'].get('detectedBreak').get('type') == 'LINE_BREAK' or symbol['property'].get('detectedBreak').get('type') == 'HYPHEN' or symbol['property'].get('detectedBreak').get('type') == 'EOL_SURE_SPACE':
                                        line = line.rstrip(' ')
                                        # add space if is line break
                                        if symbol['property'].get('detectedBreak').get('type') == 'LINE_BREAK' or symbol['property'].get('detectedBreak').get('type') == 'EOL_SURE_SPACE':
                                            line += ' '
                                        row_changed = True
                                        first_row = False
                                        # create a register in lists for dicts
                                        # list_text
                                        list_text.append(line)
                                        line = ''
                                        # list_chars_height
                                        list_chars_height.append(round(
                                            max(y_list_word) - min(y_list_word), 5))
                                        # list_para_height
                                        list_para_height.append(round(
                                            max(y_list_para) - min(y_list_para), 5))
                                        # list_para_width
                                        list_para_width.append(round(
                                            max(x_list_para) - min(x_list_para), 5))
                                        # list_para_area
                                        list_para_area.append(round(
                                            (max(y_list_para) - min(y_list_para))*(max(x_list_para) - min(x_list_para)), 5))
                                        # list_para_pos1_x
                                        list_para_pos1_x.append(
                                            round(min(x_list_para), 5))
                                        # list_para_pos1_y
                                        list_para_pos1_y.append(
                                            round(min(y_list_para), 5))
                                        # list_para_pos2_x
                                        list_para_pos2_x.append(
                                            round(max(x_list_para), 5))
                                        # list_para_pos2_y
                                        list_para_pos2_y.append(
                                            round(max(y_list_para), 5))
                                        # reset row
                                        #row_changed = False
                            except KeyError:
                                row_changed = False

                            # check for space add word to line and start new word
                            try:
                                if symbol['property'].get('detectedBreak'):
                                    if symbol['property'].get('detectedBreak').get('type') == 'SPACE' or symbol['property'].get('detectedBreak').get('type') == 'SURE_SPACE':
                                        #line += word_for_line
                                        line += ' '
                                        #word_for_line = ''
                            except KeyError:
                                pass

        # register page in dicts
        dict_text[page] = list_text
        # fill dict_text
        #text = response['fullTextAnnotation']['text']
        #text_list = text.split('\n')
        #dict_text[page] = text_list
        # try:
        #    dict_text[page].remove('')
        # except ValueError:
        #    pass
        # fill dict_id
        id_list_str = ['{}.{}'.format(page, i)
                       for i, v in enumerate(dict_text[page])]
        id_list = [float(string) for string in id_list_str]
        dict_id[page] = id_list
        # fill dict_chars
        for key, value in dict_text.items():
            char_list = []
            for string in value:
                char_list.append(len(string))
            dict_chars[key] = char_list
        dict_chars_height[page] = list_chars_height
        dict_para_height[page] = list_para_height
        dict_para_width[page] = list_para_width
        dict_para_area[page] = list_para_area
        dict_para_pos1_x[page] = list_para_pos1_x
        dict_para_pos1_y[page] = list_para_pos1_y
        dict_para_pos2_x[page] = list_para_pos2_x
        dict_para_pos2_y[page] = list_para_pos2_y

    # join pages into a single list
    final_list_id = []
    for value in dict_id.values():
        final_list_id += value
    final_list_text = []
    for value in dict_text.values():
        final_list_text += value
    final_list_chars = []
    for value in dict_chars.values():
        final_list_chars += value
    final_list_chars_height = []
    for value in dict_chars_height.values():
        final_list_chars_height += value
    final_list_para_height = []
    for value in dict_para_height.values():
        final_list_para_height += value
    final_list_para_width = []
    for value in dict_para_width.values():
        final_list_para_width += value
    final_list_para_area = []
    for value in dict_para_area.values():
        final_list_para_area += value
    final_list_para_pos1_x = []
    for value in dict_para_pos1_x.values():
        final_list_para_pos1_x += value
    final_list_para_pos1_y = []
    for value in dict_para_pos1_y.values():
        final_list_para_pos1_y += value
    final_list_para_pos2_x = []
    for value in dict_para_pos2_x.values():
        final_list_para_pos2_x += value
    final_list_para_pos2_y = []
    for value in dict_para_pos2_y.values():
        final_list_para_pos2_y += value

    # make dataframe
    df = pd.DataFrame({
        'id': final_list_id,
        'text': final_list_text,
        'chars': final_list_chars,
        'chars_height': final_list_chars_height,
        'para_height': final_list_para_height,
        'para_width': final_list_para_width,
        'para_area': final_list_para_area,
        'para_pos1_x': final_list_para_pos1_x,
        'para_pos1_y': final_list_para_pos1_y,
        'para_pos2_x': final_list_para_pos2_x,
        'para_pos2_y': final_list_para_pos2_y
    })

    if path_for_csv.endswith('/'):
        path = '{}{}.csv'.format(path_for_csv, json_blob.name.rstrip('.json'))
    else:
        path = '{}/{}.csv'.format(path_for_csv, json_blob.name.rstrip('.json'))
    df.to_csv(path, index=False)


def create_dataframe(json_blob):
    # with open(json_blob.name) as file:
    #data = json.load(file)
    json_string = json_blob.download_as_string()
    data = json.loads(json_string)

    # dicts where Im gonna save the info for the csv, key = page-number, value = list of attributes
    dict_id = {}
    dict_text = {}
    dict_chars = {}
    dict_chars_height = {}
    dict_para_height = {}
    dict_para_width = {}
    dict_para_area = {}
    dict_para_pos1_x = {}
    dict_para_pos1_y = {}
    dict_para_pos2_x = {}
    dict_para_pos2_y = {}

    # loop file responses
    for response in data['responses']:
        page = response['context']['pageNumber']
        # lists for dicts
        #word_for_line = ''
        line = ''
        list_text = []
        list_chars_height = []
        list_para_height = []
        list_para_width = []
        list_para_area = []
        list_para_pos1_x = []
        list_para_pos1_y = []
        list_para_pos2_x = []
        list_para_pos2_y = []
        # to check if row changed
        row_changed = False
        first_row = True
        # list of coords
        x_list_para = []
        y_list_para = []
        x_list_word = []
        y_list_word = []
        for page_ in response['fullTextAnnotation']['pages']:
            for block in page_['blocks']:
                for para in block['paragraphs']:
                    if row_changed == True or first_row == True:
                        # clear old values
                        x_list_para.clear()
                        y_list_para.clear()
                        # save new values
                        for v in para['boundingBox']['normalizedVertices']:
                            x_list_para.append(v['x'])
                            y_list_para.append(v['y'])
                    for word in para['words']:
                        if row_changed == True or first_row == True:
                            # clear old values
                            x_list_word.clear()
                            y_list_word.clear()
                            # save new values
                            for v in word['boundingBox']['normalizedVertices']:
                                x_list_word.append(v['x'])
                                y_list_word.append(v['y'])
                        for symbol in word['symbols']:
                            # create word
                            #word_for_line += symbol['text']
                            line += symbol['text']
                            try:
                                if symbol['property'].get('detectedBreak'):
                                    if symbol['property'].get('detectedBreak').get('type') == 'LINE_BREAK' or symbol['property'].get('detectedBreak').get('type') == 'HYPHEN' or symbol['property'].get('detectedBreak').get('type') == 'EOL_SURE_SPACE':
                                        row_changed = True
                                        first_row = False
                                        # create a register in lists for dicts
                                        # list_text
                                        list_text.append(line.rstrip(' '))
                                        line = ''
                                        # list_chars_height
                                        list_chars_height.append(round(
                                            max(y_list_word) - min(y_list_word), 5))
                                        # list_para_height
                                        list_para_height.append(round(
                                            max(y_list_para) - min(y_list_para), 5))
                                        # list_para_width
                                        list_para_width.append(round(
                                            max(x_list_para) - min(x_list_para), 5))
                                        # list_para_area
                                        list_para_area.append(round(
                                            (max(y_list_para) - min(y_list_para))*(max(x_list_para) - min(x_list_para)), 5))
                                        # list_para_pos1_x
                                        list_para_pos1_x.append(
                                            round(min(x_list_para), 5))
                                        # list_para_pos1_y
                                        list_para_pos1_y.append(
                                            round(min(y_list_para), 5))
                                        # list_para_pos2_x
                                        list_para_pos2_x.append(
                                            round(max(x_list_para), 5))
                                        # list_para_pos2_y
                                        list_para_pos2_y.append(
                                            round(max(y_list_para), 5))
                                        # reset row
                                        #row_changed = False
                            except KeyError:
                                row_changed = False

                            # check for space add word to line and start new word
                            try:
                                if symbol['property'].get('detectedBreak'):
                                    if symbol['property'].get('detectedBreak').get('type') == 'SPACE' or symbol['property'].get('detectedBreak').get('type') == 'SURE_SPACE':
                                        #line += word_for_line
                                        line += ' '
                                        #word_for_line = ''
                            except KeyError:
                                pass

        # register page in dicts
        dict_text[page] = list_text
        # fill dict_text
        #text = response['fullTextAnnotation']['text']
        #text_list = text.split('\n')
        #dict_text[page] = text_list
        # try:
        #    dict_text[page].remove('')
        # except ValueError:
        #    pass
        # fill dict_id
        id_list_str = ['{}.{}'.format(page, i)
                       for i, v in enumerate(dict_text[page])]
        id_list = [float(string) for string in id_list_str]
        dict_id[page] = id_list
        # fill dict_chars
        for key, value in dict_text.items():
            char_list = []
            for string in value:
                char_list.append(len(string))
            dict_chars[key] = char_list
        dict_chars_height[page] = list_chars_height
        dict_para_height[page] = list_para_height
        dict_para_width[page] = list_para_width
        dict_para_area[page] = list_para_area
        dict_para_pos1_x[page] = list_para_pos1_x
        dict_para_pos1_y[page] = list_para_pos1_y
        dict_para_pos2_x[page] = list_para_pos2_x
        dict_para_pos2_y[page] = list_para_pos2_y

    # join pages into a single list
    final_list_id = []
    for value in dict_id.values():
        final_list_id += value
    final_list_text = []
    for value in dict_text.values():
        final_list_text += value
    final_list_chars = []
    for value in dict_chars.values():
        final_list_chars += value
    final_list_chars_height = []
    for value in dict_chars_height.values():
        final_list_chars_height += value
    final_list_para_height = []
    for value in dict_para_height.values():
        final_list_para_height += value
    final_list_para_width = []
    for value in dict_para_width.values():
        final_list_para_width += value
    final_list_para_area = []
    for value in dict_para_area.values():
        final_list_para_area += value
    final_list_para_pos1_x = []
    for value in dict_para_pos1_x.values():
        final_list_para_pos1_x += value
    final_list_para_pos1_y = []
    for value in dict_para_pos1_y.values():
        final_list_para_pos1_y += value
    final_list_para_pos2_x = []
    for value in dict_para_pos2_x.values():
        final_list_para_pos2_x += value
    final_list_para_pos2_y = []
    for value in dict_para_pos2_y.values():
        final_list_para_pos2_y += value

    # make dataframe
    df = pd.DataFrame({
        'id': final_list_id,
        'text': final_list_text,
        'chars': final_list_chars,
        'chars_height': final_list_chars_height,
        'para_height': final_list_para_height,
        'para_width': final_list_para_width,
        'para_area': final_list_para_area,
        'para_pos1_x': final_list_para_pos1_x,
        'para_pos1_y': final_list_para_pos1_y,
        'para_pos2_x': final_list_para_pos2_x,
        'para_pos2_y': final_list_para_pos2_y
    })

    return df
