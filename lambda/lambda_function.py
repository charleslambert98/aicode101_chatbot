import sys
CURR_PATH = "/mnt/efs"
sys.path.append(CURR_PATH)

import json
import logging
import pandas as pd
import knowledge_graph as kg

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" Helper Functions: Intent Response Functions """


def close(session_attributes, msg, card=None):
    print(card)
    if card:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                },
                "responseCard": card
            }
        }
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                    "contentType": "PlainText",
                    "content": msg
            }
        }
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, msg, card=None):
    if card:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitSlot",
                "intentName": intent_name,
                "slots": slots,
                "slotToElicit": slot_to_elicit,
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                },
                "responseCard": card
            }
        }

    return {
        "session_attributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": {
                    "contentType": "PlainText",
                    "content": msg
            }
        }
    }


def delegate(session_attributes, slots):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Delegate",
            "slots": slots
        }
    }


def elicit_intent(session_attributes, msg, card=None):
    if card:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                },
                "responseCard": card
            }
        }
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitIntent",
            "message": {
                    "contentType": "PlainText",
                    "content": msg
            }
        }
    }


def confirm_intent(session_attributes, intent_name, slots, msg, card=None):
    if card:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ConfirmIntent",
                "intentName": intent_name,
                "slots": slots,
                "message": {
                    "contentType": "PlainText",
                    "content": msg
                },
                "responseCard": card
            }
        }

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ConfirmIntent",
            "intentName": intent_name,
            "slots": slots,
            "message": {
                    "contentType": "PlainText",
                    "content": msg
            }
        }
    }


""" Helper Functions: Response Builders """


def build_response_card(title, subtitle, imageUrl, AttachmentLinkUrl, buttons=None):
    choices = []
    if buttons is not None:
        if len(buttons) > 5:
            pass  # Insert multiple cards
        else:
            for button in range(len(buttons)):
                choices.append(buttons[button])

        return {
            "version": 1.0,
            "contentType": "application/vnd.amazonaws.card.generic",
            "genericAttachments": [
                {
                    "title": title,
                    "subTitle": subtitle,
                    "imageUrl": imageUrl,
                    "attachmentLinkUrl": AttachmentLinkUrl,
                    "buttons": choices
                }
            ]
        }
    return {
        "version": 1.0,
        "contentType": "application/vnd.amazonaws.card.generic",
        "genericAttachments": [
            {
                "title": title,
                "subTitle": subtitle,
                "imageUrl": imageUrl,
                "attachmentLinkUrl": AttachmentLinkUrl
            }
        ]
    }


def build_multiple_response_cards(items):
    cards = []

    for key, item in items.items():
        title = item["title"]
        imageUrl = item["imageUrl"]
        subTitle = item["subtitle"]
        attachmentLinkUrl = item["attachmentLinkUrl"]
        if 'buttons' in item:
            buttons = item["buttons"]
            cards += [{'title': title, 'imageUrl': imageUrl, 'subTitle': subTitle,
                       'attachmentLinkUrl': attachmentLinkUrl, 'buttons': buttons}]
        else:
            cards += [{'title': title, 'imageUrl': imageUrl, 'subTitle': subTitle,
                       'attachmentLinkUrl': attachmentLinkUrl}]

    response_card = {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': cards
    }

    return response_card


def get_lesson(intent_request):
    source = intent_request['invocationSource']
    session_attributes = []
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
    slots = intent_request['currentIntent']['slots']
    category_json_path = CURR_PATH + "/courses/categories.json"
    category_json_content = pd.read_json(category_json_path)
    course_json_path = CURR_PATH + "/courses/courses.json"
    course_json_content = pd.read_json(course_json_path)

    if source == "DialogCodeHook":
        if slots['lesson'] is None:
            msg = "Which category would you like to look at?"
            cards = []
            cards = build_multiple_response_cards(category_json_content)
            return elicit_slot(session_attributes, "Tutorials", slots, "lesson", msg, cards)

    parsed_input = intent_request['currentIntent']['slots']['lesson'].replace(
        ' ', '-').lower()
    print(parsed_input)

    for key, item in course_json_content.items():
        if key in parsed_input:
            session_attributes['projectName'] = parsed_input
            session_attributes['stepNumber'] = 0
            slots['lesson'] = session_attributes['projectName']
            
            return get_lesson_overview(session_attributes, intent_request)

    num_similar = 0
    results = {}

    for key, item in course_json_content.items():
        #print(item)
        if parsed_input in key or parsed_input in item['category']:
            results[key] = item
            num_similar += 1

    if num_similar >= 1:
        cards = build_multiple_response_cards(results)
        msg = "Which %s lesson would you like to do?" % parsed_input
        return close(session_attributes, msg, cards)

    return close(session_attributes, "We can't find that project!")


def get_lesson_overview(session_attributes, intent_request):
    lesson_name = session_attributes['projectName']
    step_number = int(session_attributes['stepNumber'])
    
    json_path = CURR_PATH + "/courses/{}/{}.json".format(lesson_name, lesson_name)
    json_content = pd.read_json(json_path)
    title = json_content[step_number]['title']
    subtitle = json_content[step_number]['subtitle']
    imageUrl = json_content[step_number]['image_url']
    attachmentLinkUrl = json_content[step_number]['link']
    buttons = json_content[step_number]['buttons']
    msg = json_content[step_number]['description']
    
    data = kg.load_file(json_content)
    nlp = kg.perform_nlp(data)
    results = kg.gather_similarity(nlp)
    session_attributes["nlpResults"] = str(results)
    
    if len(buttons) > 5:
        cards = {}
        for button in buttons:
            title = button["text"]
            button_step = [int(num)
                           for num in button["value"].split() if num.isdigit()]
            button = [{"text": button["text"],
                       "value": button["value"]}]
            cards[title] = {
                "title": title,
                "subtitle": subtitle,
                "imageUrl": json_content[(button_step[0])]['image_url'],
                "attachmentLinkUrl": attachmentLinkUrl,
                "buttons": button
            }

        choice_cards = build_multiple_response_cards(cards)
        return close(session_attributes, msg, choice_cards)

    card = build_response_card(
        title, subtitle, imageUrl, attachmentLinkUrl, buttons)
    return close(session_attributes, msg, card)


def get_next_step(intent_request):
    session_attributes = {}
    if intent_request['sessionAttributes']:
        session_attributes = intent_request['sessionAttributes']
    nlp_results = eval(session_attributes['nlpResults'])
    lesson_name = session_attributes['projectName']
    step_number = int(session_attributes['stepNumber'])
    step_number = (int(step_number) + 1)
    session_attributes.pop('stepNumber')
    session_attributes['stepNumber'] = step_number

    json_path = CURR_PATH + "/courses/{}/{}.json".format(lesson_name, lesson_name)
    json_content = pd.read_json(json_path)
    title = json_content[step_number]['title']
    subtitle = json_content[step_number]['subtitle']
    imageUrl = json_content[step_number]['image_url']
    attachmentLinkUrl = json_content[step_number]['link']
    buttons = json_content[step_number]['buttons']
    if step_number in nlp_results:
        buttons.append({'text': nlp_results[step_number][0][2], 'value': nlp_results[step_number][0][0]})
    msg = json_content[step_number]['description']
    card = build_response_card(
        title, subtitle, imageUrl, attachmentLinkUrl, buttons)

    return close(session_attributes, msg, card)


def get_prev_step(intent_request):
    session_attributes = {}
    if intent_request['sessionAttributes']:
        session_attributes = intent_request['sessionAttributes']
    nlp_results = eval(session_attributes['nlpResults'])
    lesson_name = session_attributes['projectName']
    step_number = int(session_attributes['stepNumber'])
    step_number = (int(step_number) - 1)
    session_attributes.pop('stepNumber')
    session_attributes['stepNumber'] = step_number

    json_path = CURR_PATH + "/courses/{}/{}.json".format(lesson_name, lesson_name)
    json_content = pd.read_json(json_path)
    title = json_content[step_number]['title']
    subtitle = json_content[step_number]['subtitle']
    imageUrl = json_content[step_number]['image_url']
    attachmentLinkUrl = json_content[step_number]['link']
    buttons = json_content[step_number]['buttons']
    if step_number in nlp_results:
        buttons.append({'text': nlp_results[step_number][0][2], 'value': nlp_results[step_number][0][0]})
    msg = json_content[step_number]['description']
    card = build_response_card(
        title, subtitle, imageUrl, attachmentLinkUrl, buttons)

    return close(session_attributes, msg, card)


def get_step(intent_request):
    source = intent_request['invocationSource']
    session_attributes = {}
    if intent_request['sessionAttributes']:
        session_attributes = intent_request['sessionAttributes']
    nlp_results = eval(session_attributes['nlpResults'])
    lesson_name = session_attributes['projectName']
    json_path = CURR_PATH + '/courses/{}/{}.json'.format(lesson_name, lesson_name)
    json_content = pd.read_json(json_path)

    slots = intent_request['currentIntent']['slots']
    if source == "DialogCodeHook":
        if slots['step'] is None:
            msg = "Which {} step would you like to do?".format(lesson_name)
            overview_img = json_content['0']['image_url']
            overview_subtitle = json_content['0']['subtitle']
            overview_link = json_content['0']['link']
            card = build_response_card(
                "Project Steps", overview_subtitle, overview_img, overview_link)
            return elicit_slot(session_attributes, "GetStep", slots, "step", msg, card)

    input_content = slots['step']
    session_attributes.pop('stepNumber')
    session_attributes['stepNumber'] = int(input_content)
    if session_attributes['stepNumber'] == '0':
        step_number = 0
        msg = json_content[step_number]['description']
        title = json_content[step_number]['title']
        subtitle = json_content[step_number]['subtitle']
        imageUrl = json_content[step_number]['image_url']
        attachmentLinkUrl = json_content[step_number]['link']
        buttons = json_content[step_number]['buttons']
        if step_number in nlp_results:
            buttons.append({'text': nlp_results[step_number][0][2], 'value': nlp_results[step_number][0][0]})
        if len(buttons) > 5:
            cards = {}
            cards[title] = {
                "title": title,
                "subtitle": subtitle,
                "imageUrl": imageUrl,
                "attachmentLinkUrl": attachmentLinkUrl
            }
            for button in buttons:
                title = button["text"]
                button_step = [int(num)
                               for num in button["value"].split() if num.isdigit()]
                button = [{"text": button["text"],
                           "value": button["value"]}]
                cards[title] = {
                    "title": title,
                    "subtitle": subtitle,
                    "imageUrl": json_content[(button_step[0])]['image_url'],
                    "attachmentLinkUrl": attachmentLinkUrl,
                    "buttons": button
                }
            #print(cards)
            choice_cards = build_multiple_response_cards(cards)
            return close(session_attributes, msg, choice_cards)

        card = build_response_card(
            title, subtitle, imageUrl, attachmentLinkUrl, buttons)
        return close(session_attributes, msg, card)

    else:
        parsed_input = input_content
        print(parsed_input)
        for key in json_content:
            if str(key) == parsed_input:
                step_number = int(parsed_input)
                msg = json_content[step_number]['description']
                title = json_content[step_number]['title']
                subtitle = json_content[step_number]['subtitle']
                imageUrl = json_content[step_number]['image_url']
                attachmentLinkUrl = json_content[step_number]['link']
                buttons = json_content[step_number]['buttons']
                if step_number in nlp_results:
                    buttons.append({'text': nlp_results[step_number][0][2], 'value': nlp_results[step_number][0][0]})
                if len(buttons) > 5:
                    cards = {}
                    cards[title] = {
                        "title": title,
                        "subtitle": subtitle,
                        "imageUrl": imageUrl,
                        "attachmentLinkUrl": attachmentLinkUrl
                    }
                    for button in buttons:
                        title = button["text"]
                        button_step = [int(num)
                                       for num in button["value"].split() if num.isdigit()]
                        button = [{"text": button["text"],
                                   "value": button["value"]}]
                        cards[title] = {
                            "title": title,
                            "subtitle": subtitle,
                            "imageUrl": json_content[(button_step[0])]['image_url'],
                            "attachmentLinkUrl": attachmentLinkUrl,
                            "buttons": button
                        }
                    #print(cards)
                    choice_cards = build_multiple_response_cards(cards)
                    return close(session_attributes, msg, choice_cards)

                card = build_response_card(
                    title, subtitle, imageUrl, attachmentLinkUrl, buttons)
                return close(session_attributes, msg, card)


""" Lambda Handlers """


def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    
    if intent_name == "Tutorials":
        return get_lesson(intent_request)
    elif intent_name == "NextStep":
        return get_next_step(intent_request)
    elif intent_name == "PrevStep":
        return get_prev_step(intent_request)
    elif intent_name == "GetStep":
        return get_step(intent_request)
        
    raise Exception("Intent with name {} not supported".format(intent_name))


def lambda_handler(event, context):
    logger.debug(event)
    return dispatch(event)